
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name="f_home"),
    path('Shop', views.Shop.as_view(), name="f_shop"),
    path('Cart', views.Cart.as_view(), name="f_cart"),
    path('Checkout', views.Checkout.as_view(), name="f_checkout"),
    path('Shop_Detail', views.Shop_Detail.as_view(), name="f_shop_detail"),
    path('Contact', views.Contact.as_view(), name="f_contact"),
    path('Testimonial', views.Testimonial.as_view(), name="f_testimonial"),
    path('checkout/payment', views.payment.as_view(), name="f_payment")
]