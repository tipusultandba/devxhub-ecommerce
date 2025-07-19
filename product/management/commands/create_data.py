import requests
from django.core.management import BaseCommand
from django.utils.text import slugify
from product.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Creating data......')
        create_product()
        print('All Data Migrations Success')


def create_product():
    response = requests.get('https://fakestoreapi.com/products')
    count = 0
    if response.status_code == 200:
        # Access the response data
        items = response.json()
        for item in items:
            obj = Product(title=item['title'], slug=slugify(item['title']), price=item['price'], description=item['description'], stock=50, created_by_id=1)
            obj.save()
            count += 1
        
        print(f'{count} items successfully Saved to Product List without Image. Add image manually')
    else:
        # Handle the error or unexpected response
        print(f"Error: {response.status_code}")
        pass