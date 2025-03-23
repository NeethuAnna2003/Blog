from django.core.management.base import BaseCommand
from blog.models import BlogPost

class Command(BaseCommand):
    help = 'Check blog posts in the database'

    def handle(self, *args, **kwargs):
        posts = BlogPost.objects.all()
        self.stdout.write(f'Total posts in database: {posts.count()}')
        
        if posts.exists():
            self.stdout.write('\nLatest posts:')
            for post in posts.order_by('-created_at')[:5]:
                self.stdout.write(f'- {post.title} (by {post.author.username}) - Created: {post.created_at}')
        else:
            self.stdout.write(self.style.WARNING('No posts found in the database!')) 