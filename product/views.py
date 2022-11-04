import json
from django.http import HttpResponse
from django.views.generic.list import ListView
from django .contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Sum, F, Q

from product.models import Cart, Order, Product, Wishlist
from django.core import serializers
from django.http import JsonResponse

class Allproducts(ListView):
    model = Product
    template_name = "allproducts.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            wish, list = Wishlist.objects.get_or_create(user=self.request.user)
            wishitems = wish.product.all()
            context['wishlist'] = (wishitems)
        return context


class Searchresult(ListView):
    model = Product
    template_name = "product.html"

    def get_queryset(self):
        query1 = self.request.GET.get("product_name")
        object_list = Product.objects.filter((Q(title__icontains=query1) | Q(
            brand__name__icontains=query1)) & ~Q(stock__contains="0"))
        if object_list.exists():
            pass
        else:
            messages.error(self.request, 'Products Are Not Found')
        return object_list


@login_required
def Add_to_cart(request, Product_id):
    if request.method == "POST":
        product = Product.objects.get(id=Product_id)
        cart = Cart.objects.create(
            product=product,
            user=request.user,
            price=product.price,
        )
    return redirect("all")


@login_required
def cart_remove(request, Cart_id):
    remove_item = Cart.objects.get(id=Cart_id)
    remove_item.delete()
    return redirect("cart")


@login_required
def order_remove(request, Cart_id, order_id):
    if request.method == "POST":
        remove_item = Cart.objects.get(id=Cart_id)
        qunt = remove_item.quantity
        remove_price = Order.objects.get(id=order_id)
        remove_item.delete()
        total_product_cost = remove_price.items.values().aggregate(price__sum=Sum(F('price')*F('quantity')))['price__sum']
        if total_product_cost is None:
            print("dvsdvsdv  dvdsfds ")
            remove_price.delete()
        else:
            print(remove_item.quantity)
            remove_price.total_product_cost = total_product_cost
            remove_price.save()
    return redirect("order")


def add_quntity(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.filter(product=product ,user = request.user)
        qunt = request.POST.get('quantity')
        cart.update(quantity=qunt)
        return redirect("cart")
    else:
        pass
    return redirect("cart")


@login_required
def add_order(request):
    user = request.user
    taxs = 18
    total_product_price = Cart.objects.filter(Q(user=request.user) & Q(is_active=True)).aggregate(
        total=Sum(F('price')*F('quantity')))['total']
    if total_product_price is not None:
        orders = Order.objects.create(
            user=request.user, tax=taxs, total_product_cost=total_product_price,)
        orders.items.add(
            *Cart.objects.filter(Q(user=request.user) & Q(is_active=True)))
        inactive = Cart.objects.filter(user=request.user)
        inactive.update(is_active=False)
        orders.save()
    return redirect("order")


class Orderproducts(ListView):
    model = Order
    template_name = "order.html"

    def get_queryset(self):
        object_list = Order.objects.filter(user=self.request.user)
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sub_total'] = Order.objects.filter(user=self.request.user).aggregate(
            Sum('total_product_cost'))['total_product_cost__sum']
        context['tax'] = Order.objects.filter(user=self.request.user).aggregate(
            total=Sum(F('total_product_cost') * 18/100))['total']
        if context['sub_total'] is not None:
            context['total_price'] = context['sub_total'] + context['tax']
        return context


class ListCartItem(ListView):
    model = Cart
    context_object_name = 'cartitems'
    template_name = 'list_cartitems.html'

    def get_queryset(self):
        object_list = Cart.objects.filter((Q(user=self.request.user) & Q(is_active=True)))
        if object_list.exists():
            pass
        else:
            messages.error(self.request, ' your cart is empty  ')
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['total_price'] = self.get_queryset().aggregate(Sum('price'))['price__sum']
        return context

@login_required
def order_place(request):
    return HttpResponse("your order is placed")

@login_required
def add_wishlist(request, Product_id):
    if request.method == "POST":
        wish_product = Product.objects.get(id=Product_id)
        obj, add_wish = Wishlist.objects.get_or_create(user=request.user)
        obj.product.add(wish_product)
    return redirect('all')

def rm_wishlist(request, Product_id):
    if request.method == "POST":
        wish_product = Product.objects.get(id=Product_id)
        obj = Wishlist.objects.get(user=request.user)
        obj.product.remove(wish_product)
    return redirect('all')

class Wishproducts(ListView):
    model = Wishlist
    template_name = "wish.html"

    def get_queryset(self):
        object_list = Wishlist.objects.filter(user=self.request.user)
        return object_list

def product_api(request):
    products =  Product.objects.all()
    data = serializers.serialize("json", products)
    return JsonResponse(json.loads(data), safe=False)
def cart_api(request):
    products =  Cart.objects.all()
    data = serializers.serialize("json", products)
    return JsonResponse(json.loads(data), safe=False)

def search_api(request):
     query1 = request.GET.get("product_name")
     object_list = Product.objects.filter((Q(title__icontains=query1) | Q(
            brand__name__icontains=query1)) & ~Q(stock__contains="0"))
     data = serializers.serialize("json", object_list)
     #data =list(object_list.values())
     return JsonResponse(json.loads(data),safe=False)

def order_api(request):
    products =  Order.objects.all()
    data = serializers.serialize("json", products)
    return JsonResponse(json.loads(data), safe=False)