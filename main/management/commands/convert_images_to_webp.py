import re
from django.core.management.base import BaseCommand
from main.models import Product, CompleteProject


class Command(BaseCommand):
    help = 'Update image paths in DB from .png/.jpg to .webp'

    def handle(self, *args, **options):
        pattern = re.compile(r'\.(png|jpg|jpeg)$', re.I)

        updated = 0
        for p in Product.objects.all():
            content = p.content
            changed = False
            if 'images' in content:
                for img in content['images']:
                    for key in ('src', 'thumbnail'):
                        if key in img and pattern.search(img[key]):
                            img[key] = pattern.sub('.webp', img[key])
                            changed = True
            if changed:
                p.content = content
                p.save(update_fields=['content'])
                updated += 1
                self.stdout.write(f'  Product: {p.title}')

        cp_updated = 0
        for cp in CompleteProject.objects.all():
            if pattern.search(cp.image_path):
                cp.image_path = pattern.sub('.webp', cp.image_path)
                cp.save(update_fields=['image_path'])
                cp_updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Products: {updated}, CompleteProjects: {cp_updated}'
        ))
