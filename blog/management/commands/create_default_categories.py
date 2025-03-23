from django.core.management.base import BaseCommand
from blog.models import Category

class Command(BaseCommand):
    help = 'Creates default categories for the blog'

    def handle(self, *args, **kwargs):
        default_categories = [
            'Technology',
            'Lifestyle',
            'Travel',
            'Food',
            'Health',
            'Business',
            'Education',
            'Entertainment'
        ]
        
        for category_name in default_categories:
            Category.objects.get_or_create(
                name=category_name,
                defaults={'description': f'Posts related to {category_name.lower()}'}
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully created default categories')) 