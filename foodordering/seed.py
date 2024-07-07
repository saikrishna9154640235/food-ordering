import random
from faker import Faker
from django.utils.text import slugify
from foodordering.models import Product ,ProductMetaInformation  # Adjust import path as per your Django app structure
from datetime import datetime

fake = Faker()

def seed_db(n=10):
    try:
        for i in range(n):
            product_name = fake.word().capitalize() + ' ' + fake.word().capitalize()
            product_slug = slugify(product_name)
            product_description = fake.text()
            products_demo_price = random.randint(5, 50)  # Random demo price between 5 and 50
            quantity = random.randint(1, 1000)  # Random quantity between 1 and 1000
            
            # Create the Product object
            product = Product.objects.create(
                product_name=product_name,
                product_slug=product_slug,
                product_description=product_description,
            
                products_demo_price=products_demo_price,
                quantity=str(quantity)  # Assuming quantity is a string field
            )
            
            print(f"Product '{product_name}' seeded.")

    except Exception as e:
        print(f"An error occurred while seeding database: {e}")

if __name__ == '__main__':
    seed_db()


