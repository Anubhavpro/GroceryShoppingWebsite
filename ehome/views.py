from django.shortcuts import render, redirect
from .models import *
from django.views import View
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# This view class, Productcategory, retrieves products categorized as 'Top Savers Today' (TSP) 
# and 'Best Offer' (BO) from the database using the Product model. It then renders the index.html 
# template with the retrieved products passed as context variables 'Top_Savers_Today' and 'Best_Offer'.
# These variables can be utilized in the template to display the respective product listings.
class Productcategory(View):
    def get(self, request):
        Top_Savers_Today = Product.objects.filter(category='TSP')
        Best_Offer = Product.objects.filter(category='BO')
        return render(request, 'ehome/index.html', {'Top_Savers_Today':Top_Savers_Today,'Best_Offer':Best_Offer})
   
# This function-based view, 'address', is decorated with '@login_required', ensuring that only authenticated users 
# can access it. It retrieves the address information associated with the currently logged-in user from the 
# 'customer' model and passes it to the 'address.html' template using the context variable 'add'. 
# This allows the template to display the user's address information.    
@login_required
def address(request):
    add = customer.objects.filter(user=request.user)
    return render(request, 'ehome/address.html',{'add':add})

# This function-based view, 'MyCart', is decorated with '@login_required', ensuring that only authenticated users
# can access it. It adds a product to the user's shopping cart. It retrieves the logged-in user's information 
# from the request, as well as the product ID from the GET parameters. It then fetches the corresponding product 
# from the database using the 'Product' model. Afterward, it creates an entry in the 'cart' model associating 
# the user with the product, and redirects the user to the '/cart' URL to view their updated shopping cart.
@login_required
def MyCart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    cart(user=user, product=product).save()
    return redirect('/cart')


# This function-based view, 'show_cart', is decorated with '@login_required', ensuring that only authenticated users 
# can access it. It displays the contents of the user's shopping cart. It retrieves the logged-in user's information 
# from the request and fetches the corresponding cart items from the 'cart' model associated with that user. 
# It calculates the total amount of the items in the cart, including shipping charges, and renders the 'addtocart.html' 
# template with the cart items and total amount if the cart is not empty. If the cart is empty, it renders the 
# 'emptycart.html' template instead.
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cartt = cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 80.0
        total_amount = 0.0
        cart_product = [p for p in cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request,'ehome/addtocart.html', {'carts':cartt, 'totalamount':totalamount, 'amount':amount})
        else:
            return render(request, 'ehome/emptycart.html')


# This function, 'plus_cart', handles the increase in quantity of a product in the user's shopping cart.
# It checks if the request method is 'GET' and retrieves the product ID from the GET parameters.
# Then, it fetches the corresponding cart item from the 'cart' model based on the product ID and the logged-in user.
# It increments the quantity of the cart item by 1 and saves the changes.
# It recalculates the total amount for all items in the cart, including shipping charges.
# Finally, it returns a JSON response containing the updated quantity, amount, and total amount.
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 80.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)


# This function, 'minus_cart', handles the decrease in quantity of a product in the user's shopping cart.
# It checks if the request method is 'GET' and retrieves the product ID from the GET parameters.
# Then, it fetches the corresponding cart item from the 'cart' model based on the product ID and the logged-in user.
# It decrements the quantity of the cart item by 1 and saves the changes.
# It recalculates the total amount for all items in the cart, including shipping charges.
# Finally, it returns a JSON response containing the updated quantity, amount, and total amount.
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 80.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)

# This function, 'remove_cart', handles the removal of a product from the user's shopping cart.
# It checks if the request method is 'GET' and retrieves the product ID from the GET parameters.
# Then, it fetches the corresponding cart item from the 'cart' model based on the product ID and the logged-in user.
# It deletes the cart item from the database.
# It recalculates the total amount for all items in the cart, including shipping charges.
# Finally, it returns a JSON response containing the updated amount and total amount.
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 80.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'amount':amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)


# This function, 'blog', renders the 'blog.html' template when accessed.
# It simply returns the rendered template in response to the request.
def blog(request):
    return render(request, 'ehome/blog.html')

# This function, 'blogdetail', renders the 'blog-detail.html' template when accessed.
# It simply returns the rendered template in response to the request.
def blogdetail(request):
    return render(request, 'ehome/blog-detail.html')



# This function-based view, 'checkout', is decorated with '@login_required', ensuring that only authenticated users 
# can access it. It handles the checkout process for the user's shopping cart. It retrieves the logged-in user's 
# information and address details from the 'customer' model. It also fetches the items in the user's cart from the 
# 'cart' model. It calculates the total amount of the items in the cart, including shipping charges. 
# It then renders the 'checkout.html' template with the user's address details, cart items, and total amount.
@login_required
def checkout(request):
    user = request.user
    add = customer.objects.filter(user=user)
    cart_items = cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 80.0
    totalamount = 0.0
    cart_product = [p for p in cart.objects.all() if p.user == request.user]
    if cart_product :
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount +shipping_amount

    return render(request, 'ehome/checkout.html', {'add':add, 'totalamount':totalamount,'cart_items':cart_items})


# This function, 'contact', renders the 'contact.html' template, which is used for displaying contact information 
# or a contact form. It simply returns the rendered template in response to the request.
def contact(request):
    return render(request, 'ehome/contact.html')

# This function-based view, 'orderlist', is decorated with '@login_required', ensuring that only authenticated users 
# can access it. It retrieves the order history for the logged-in user from the 'Orderplaced' model. 
# It then renders the 'orderlist.html' template with the retrieved order history passed as the context variable 'order_placed'.
@login_required
def orderlist(request):
    op = Orderplaced.objects.filter(user=request.user)
    return render(request, 'ehome/orderlist.html', {'order_placed':op})    



# This function-based view, 'payment_done', is decorated with '@login_required', ensuring that only authenticated users 
# can access it. It handles the completion of the payment process after a successful transaction. 
# It retrieves the logged-in user's information and the customer ID from the GET parameters. 
# Then, it fetches the corresponding customer information from the 'customer' model. 
# It also retrieves the items in the user's cart from the 'cart' model. 
# It creates 'Orderplaced' instances for each item in the cart, associating them with the user and customer, 
# and saves them in the database. After the order placement is completed, it deletes the items from the user's cart. 
# Finally, it redirects the user to the 'orderlist' URL to view their updated order history.
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    Customer = customer.objects.get(id=custid)
    Cart = cart.objects.filter(user=user)
    for c in Cart:
        Orderplaced(user=user, customer=Customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orderlist") 


class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists
        return render(request, 'ehome/product-detail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

# This function, 'shop', handles the display of products in the shop section based on various filters.
# It takes an optional parameter 'data' to determine the filtering criteria.
# If 'data' is None, it fetches all products categorized as 'Fruits_Vegetables' from the 'Product' model.
# If 'data' is 'Fruits' or 'Vegetables', it fetches products categorized as 'Fruits_Vegetables' and filtered by the brand specified in 'data'.
# If 'data' is 'below', it fetches products categorized as 'Fruits_Vegetables' and with a discounted price less than 100.
# If 'data' is 'above', it fetches products categorized as 'Fruits_Vegetables' and with a discounted price greater than 100.
# Finally, it renders the 'shop.html' template with the filtered products passed as the context variable 'Fruits_Vegetables'.
def shop(request,data=None):
    if data == None:
        Fruits_Vegetables = Product.objects.filter(category='FV')
    elif data == 'Fruits' or data == 'Vegetables':
        Fruits_Vegetables = Product.objects.filter(category='FV').filter(brand=data)
    elif data == 'below':
        Fruits_Vegetables = Product.objects.filter(category='FV').filter(discounted_price__lt=100)
    elif data == 'above':
        Fruits_Vegetables = Product.objects.filter(category='FV').filter(discounted_price__gt=100)
    return render(request, 'ehome/shop.html',{'Fruits_Vegetables':Fruits_Vegetables})

# This class-based view, 'ProfileView', is decorated with '@method_decorator(login_required, name='dispatch')', 
# ensuring that only authenticated users can access it. It utilizes the 'login_required' decorator to enforce 
# authentication before accessing the view. The 'get' method of this view renders the 'profile.html' template, 
# along with an empty instance of the 'CustomerProfileForm', allowing users to fill out their profile information.
@method_decorator(login_required,name='dispatch')
class ProdileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'ehome/profile.html', {'form':form})
    
    
    # This 'post' method within the 'ProfileView' class handles the submission of the customer profile form.
# It instantiates a 'CustomerProfileForm' object with the data received from the POST request.
# If the form data is valid, it extracts the cleaned data including name, phone, email, locality, city, 
# zipcode, and state. It then creates a new 'customer' object with the user and profile information, 
# saves it to the database, and displays a success message using Django's message framework.
# Finally, it renders the 'profile.html' template with the form, allowing users to see the updated profile information.
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            cus = customer(user=usr, name=name, phone=phone, email=email, locality=locality, city=city, zipcode=zipcode, state=state)
            cus.save()
            messages.success(request, 'Confratulations! Profile Updated Successfully')
        return render(request, 'ehome/profile.html', {'form':form})


# This function, 'wishlist', renders the 'wishlist.html' template, which is used for displaying the user's wishlist.
# It simply returns the rendered template in response to the request.
def wishlist(request):
    return render(request, 'ehome/wishlist.html')


# This function, 'footsubscribe', handles the subscription to the newsletter.
# It checks if the request method is 'POST', indicating a form submission.
# It then retrieves the email from the POST data and creates a new 'footnewslatter' object with the email.
# It saves the object to the database, representing the subscription to the newsletter.
# Finally, it renders the 'index.html' template in response to the request.
def footsubscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')   
        EM =  footnewslatter(email=email)
        EM.save()
    return render(request,'ehome/index.html')


# This function, 'contactform', handles the submission of a contact form.
# It checks if the request method is 'POST', indicating a form submission.
# It then retrieves the form data including fullname, phone, email, and message from the POST data.
# It creates a new 'contactform' object with the form data and saves it to the database.
# Finally, it renders the 'contact.html' template in response to the request.
def contctform(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')   
        CF =  contactform(fullname=fullname,phone=phone,email=email,message=message)
        CF.save()
    return render(request,'ehome/contact.html')


# This class-based view, 'CustomerRegistrationView', handles the customer registration process.
# The 'get' method is responsible for rendering the registration form when an HTTP GET request is made.
# It initializes an empty instance of 'CustomerRegistrationForm' and renders the 'customerregistration.html' template 
# with the form passed as context.
# The 'post' method processes the form submission when an HTTP POST request is made.
# It instantiates a 'CustomerRegistrationForm' object with the data received from the POST request.
# If the form data is valid, it displays a success message using Django's message framework and saves the form data.
# Finally, it renders the 'customerregistration.html' template with the form passed as context, whether the form is valid or not.
class CutomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'ehome/customerregistration.html', {'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! Registered Successfully')
            form.save()
        return render(request,'ehome/customerregistration.html', {'form':form})
   




