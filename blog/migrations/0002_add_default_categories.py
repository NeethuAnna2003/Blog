from django.db import migrations

def add_default_categories(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    default_categories = [
        {'name': 'Technology', 'description': 'Posts about technology and innovation'},
        {'name': 'Healthcare', 'description': 'Posts about health and medical topics'},
        {'name': 'Cloud Computing', 'description': 'Posts about cloud computing and services'},
    ]
    for category_data in default_categories:
        Category.objects.get_or_create(
            name=category_data['name'],
            defaults={'description': category_data['description']}
        )

def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    Category.objects.filter(name__in=['Technology', 'Healthcare', 'Cloud Computing']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_categories, remove_default_categories),
    ] 