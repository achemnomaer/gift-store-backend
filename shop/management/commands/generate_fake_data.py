# yourapp/management/commands/generate_fake_data.py

from django.core.management.base import BaseCommand
from faker import Faker

from shop.models import (Image, Occasion, Product,  # Import your models
                         RecipientType, Subcategory)


class Command(BaseCommand):
    help = 'Generate fake data for your ecommerce website'

    def handle(self, *args, **options):
        fake = Faker()

        subcategories = Subcategory.objects.all()
        occasions = Occasion.objects.all()
        recipient_types = RecipientType.objects.all()

        for _ in range(20):
            product = Product.objects.create(
                subcategory=fake.random_element(subcategories),
                name=fake.word(),
                slug=fake.slug(),
                description=fake.text(),
                details=fake.text(),
                price=fake.random_number(digits=2),
                discounted_price=fake.random_number(digits=2) if fake.boolean(
                    chance_of_getting_true=50) else None,
                stock_quantity=fake.random_number(digits=3),
                featured=fake.boolean(),
                is_available=fake.boolean(),
                primary_image=fake.image_url(),
            )

            product.occasions.set(fake.random_elements(
                occasions, length=fake.random_int(min=0, max=3)))
            product.recipient_types.set(fake.random_elements(
                recipient_types, length=fake.random_int(min=0, max=2)))

        self.stdout.write(self.style.SUCCESS('Fake data created successfully'))
