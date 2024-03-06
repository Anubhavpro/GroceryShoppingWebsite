from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ehome import views
from django.contrib.auth import views as auth_views
from .forms import *

urlpatterns = [
    path('',views.Productcategory.as_view(),name='home'),
    path('address/', views.address, name='address'),
    path('blogdetail/', views.blogdetail, name='blogdetail'),
    path('blog/',views.blog, name='blog'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('orderlist/', views.orderlist, name='orderlist'),
    path('productdetail/<int:pk>', views.ProductDetailView.as_view(), name='productdetail'),
    path('profile/', views.ProdileView.as_view(), name='profile'),
    path('shop/', views.shop, name='shop'),
    path('add-to-cart/', views.MyCart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('shop/<slug:data>', views.shop, name='fruitdata'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('footsubscribe/', views.footsubscribe, name='footsubscribe'),
    path('contctform/', views.contctform, name='contactform'),
    path('registartion/',views.CutomerRegistrationView.as_view(), name='customerregistartion'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='ehome/login.html', authentication_form=LoginForm),name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='ehome/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='ehome/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='ehome/password_reset.html', form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='ehome/password_resetdone.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='ehome/password_reset_confirm.html', form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='ehome/password_reset_complete.html'),name='password_reset_complete'),
    path('paymentdone/', views.payment_done, name='paymentdone'),





]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)