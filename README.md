## Table of contents
* [General info](#general-info)
* [Project Structure](#project-structure)
* [Technologies](#technologies)
* [Setup](#setup)
* [project details](#project-details)


## General info
# Django E-commerce Site with Payment Gateway and REST API. 
An E-commerce site where users can browse products, add them to their shopping cart,
and make purchases. Implement an API to expose the platform's functionality to other services.
	

## Project Structure
```
.
├── ...
├── devxhub-ecommerce       # Project Root Directory
│   ├── cart                # shopping cart app
│   ├── config              # project setting configuration.
│   ├── custom_auth         # Authentication app. such as: login, logout, register
│   ├── order               # Order app, all order and order item.
|   ├── product             # All Product and stock.
|   ├── static              # Project static files.
|   ├── templates           # Project related all templates.
|   ├── user_profile        # User Information app. such as: shipping address, phone no etc.
│   └── ...                 
└── ...
```

## Technologies
Project is created with:
* Python version: 3.8.10
* Django version: 4.1.1
* Django Rest Framework version: 3.14.0
* Database Sqlite3
* Java Script
* Bootstrap
* fontawesome
	
## Setup
To run this project, install it locally using pip:

```
$ git clone  https://github.com/monir07/devxhub-ecommerce.git
$ virtualenv venv
$ source venv/bin/activate
$ cd devxhub-ecommerce
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py create_data
$ python manage.py runserver
```

## Project Details

* User Authentication:
User can Registration, Login, and Logout functionality. When an user register, user profile automatically created. After login User can update their profile by clicking update profile.

* Product Management:
Product Database Create with fields: name, description, price, image, and stock status. user can visit all product by clicking shop button at home page. product list page have product search option and pagination.

* Shopping Cart:
User can add product in shopping cart by clicking add to cart button. Authenticate and UnAuthenticate user also add product in cart. Shopping Cart functionality design with django session. After added product in cart user can increase or decrease product quantity. user can get product discount by using coupon code. 

* Purchases and Payment Integration:
After added product in shopping cart user can checkout for payment. after clicking checkout button user see his basic information with shipping address then clock continue user PayPal payment button. After completing payment user can see his order list by clicking order list button. user also see order summery by clicking view button in order list. demo paypal client account: monirulslm7@outlook.com and password: Monir@786

* Admin Interface:
Provide an admin interface using Django's built-in capabilities. The admin should be able to add, edit, delete and search products, orders, order items, user profile, coupon etc. admin user also able to active or de-active normal user and also change password, set permission etc.

* RESTful API:
Implement a RESTful API using Django REST Framework. The API allow clients to retrieve product information. Also require appropriate authentication to retrieve product information. API url: 
```
$ /products/product-list-api/
```
