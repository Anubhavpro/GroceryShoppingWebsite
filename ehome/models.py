from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator ,MinValueValidator

#this is Our database model#

# State selection as per customer province#
state_choices = [
    ('Andhra Pradesh','Andhra Pradesh'),	
    ('Arunachal Pradesh','Arunachal Pradesh'),	
    ('Assam','Assam'),	
    ('Bihar','Bihar'),	
    ('Chhattisgarh','Chhattisgarh'),	
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),	
    ('Jharkhand','Jharkhand'),	
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),	
    ('Madhya Pradesh','Madhya Pradesh'),	
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),	
    ('Meghalaya','Meghalaya'),	
    ('Mizoram','Mizoram'),	
    ('Nagaland','Nagaland'),	
    ('Odisha','Odisha'),	
    ('Punjab','Punjab'),	
    ('Rajasthan','Rajasthan'),	
    ('Sikkim','Sikkim'),	
    ('Tamil Nadu','Tamil Nadu'),	
    ('Telangana','Telangana'),	
    ('Tripura','Tripura'),	
    ('Uttar Pradesh','Uttar Pradesh'),	
    ('Uttarakhand','Uttarakhand'),	
    ('West Bengal','West Bengal'),
    ('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),	
    ('Chandigarh','Chandigarh'),	
    ('Dadra & Nagar Haveli and Daman & Diu','Dadra & Nagar Haveli and Daman & Diu'),	
    ('Delhi','Delhi'),	
    ('Jammu and Kashmir','Jammu and Kashmir'),	
    ('Lakshadweep','Lakshadweep'),	
    ('Puducherry','Puducherry'),	
    ('Ladakh','Ladakh'),
]

class footnewslatter(models.Model):
    email = models.EmailField(max_length=30,null=True)

# User Contact form and this is a model which is used to our db #
class contactform(models.Model):
    fullname = models.CharField(max_length=40, null=True)
    phone = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=30, null=True)
    message = models.TextField(max_length=300, null=True)

class customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=30, null=True)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=state_choices, max_length=50)
 
def __str__(self):
    return str(self.id)
# Category of items & Offer,Deals#
category_choices = [
    ('TSP','Top Savers Today'),
    ('BO','Best Offer'),
    ('FV','Fruits & Vegetables'),
    ('GS','Grocery & Staples'),
    ('BV','Beverages'),
    ('BD','Breakfast & Dairy'),
    ('BSC','Biscuits, Snacks & Chocolates'),
    ('NSI','Noodles, Sauces & Instant Food'),
    ('MFS','Meats, Frozen & Seafood'),
    
]

# Product Detail Model# 
class Product(models.Model):
    product_title = models.CharField(max_length=100)
    selling_price = models.FloatField(null=True)
    discounted_price = models.FloatField(null=True)
    product_avail = models.FloatField(default=500,null=True)
    brand = models.CharField(max_length=100,null=True)
    product_desc = models.CharField(max_length=400,null=True)
    category = models.CharField(choices=category_choices, max_length=20,null=True)
    product_img = models.ImageField(blank=True, upload_to='static/productimg')



#this is Cart Model#
class cart(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
        
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

#Delivery Status#
status_choices = [
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
]


class Orderplaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=60, choices=status_choices, default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price