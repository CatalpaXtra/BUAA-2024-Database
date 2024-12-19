import os
from django.core.management.base import BaseCommand
from myblog.models import BlogCategory

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def handle(self, *args, **kwargs):
        directory = kwargs['directory']
        self.import_categories(directory)

    def import_categories(self, directory):
        file_path = os.path.join(directory, 'blog_categories.txt')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    name = line.strip()
                    category = BlogCategory(name=name)
                    category.save()
        else:
            print('File not found.')
