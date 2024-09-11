from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

#pdf
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import datetime
from xhtml2pdf import pisa

from .models import Product, CartItem, Address
from django.contrib.auth.models import User

# Create your views here.
class Home(View):
    def get(self, request):

        products = Product.objects.all()
        total_products = Product.objects.count()
        best_salers = Product.objects.all().order_by("-sold_quantity")[:6]
        satisfied_customer = User.objects.count()
        

        return render(request, "Frutiables/index.html", {
            "products": products,
            "satisfied_customer":satisfied_customer,
            "total_products": total_products,
            "best_salers": best_salers})


class Cart(View):
    def get(self, request):
        arr = []
        cart_items = CartItem.objects.filter(user=request.user)
        
        for item in cart_items:
            item.total_price = item.quantity * item.product.price
            arr.append(item.total_price)
        bill_total = sum(arr)

        return render(request, "Frutiables/cart.html", {"cart_items": cart_items,
                                                        "bill_total":bill_total})
    
    def post(self, request):
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)

        # Check if the cart item already exists
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )
        # exists created=False

        if created:
            # Item was newly created, set quantity to 1
            print("OK1")
            cart_item.quantity = 1

        else:
            print("OK2")
            # Item already exists, update the quantity based on the action (+ or -)
            action = request.POST.get("action")
            print("action:", action)
            if action == "plus":
                print("plus")
                cart_item.quantity += 1
            elif action == "minus" and cart_item.quantity > 1:
                print("minus")
                cart_item.quantity -= 1
            else:
                print("None")

        cart_item.save()

        return redirect('f_cart')



class Checkout(View):
    def get(self, request):
        print("Inside get")
        print("bill_total:", request.GET.get("bill_total"))
        bill_total = request.GET.get("bill_total")
        address = Address.objects.get(default=True)
        return render(request, "Frutiables/chackout.html", {"address": address,
                                                            "bill_total": bill_total})
    
    def post(self, request):
        print("inside checkout post")
        return redirect('f_checkout')
    
# Address
class Contact(View):
     def get(self, request):
         addresses = Address.objects.filter(user=request.user)
         return render(request, "Frutiables/contact.html", {
             "addresses":addresses
         })
     
     def post(self, request):
         print("inside")
         current_address_id = request.POST.get("address_id")
         current_default = Address.objects.get(id=current_address_id)

         default_address = Address.objects.get(default=True)

         default_address.default = False
         default_address.save()

         current_default.default = True
         current_default.save()

         print("exit")

         return redirect('f_contact')

class Shop(View):
    def get(self, request):
        products_sort_by_name = Product.objects.order_by('name')
        products_sort_by_sells = Product.objects.order_by('sold_quantity')

        return render(request, "Frutiables/shop.html",{
            "products": products_sort_by_name,
            "products_sort_by_sells": products_sort_by_sells
        })

class payment(View): 
    def get(self, request):
        print("inside payment get")
        return render(request, "Frutiables/payment.html")
        
    def post(self, request):
        print("inside payment post")

        invoice_data = {
        'invoice_number': 'INV-1001',
        'date': datetime.today().strftime("%d/%m/%Y"),
        'amount': request.POST.get("bill_total"),
        'customer_name': request.POST.get("bill_name"),
        } 
        
        html_string = render_to_string('Frutiables/bill.html', invoice_data)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="your_bill.pdf"'
    
        pisa_status = pisa.CreatePDF(html_string, dest=response)
    
        if pisa_status.err:
            return HttpResponse('We had some errors with generating the PDF', status=500)
        return response
        # pdf_response = response
        # return redirect('f_payment')
        

    
# Just for template render
class Shop_Detail(TemplateView):
     template_name = 'Frutiables/shop-detail.html'


class Testimonial(TemplateView):
     template_name = 'Frutiables/testimonial.html'
