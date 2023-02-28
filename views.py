from django.shortcuts import render, redirect, get_object_or_404
from ShoppingApp.models import Product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    if request.user.is_authenticated:
        product=Product.objects.get(id=product_id)
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
            cart.save(),
        try:
            cart_item=CartItem.objects.get(product=product,cart=cart,user=request.user)
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity +=1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(
                user=request.user,
                product=product,
                quantity=1,
                cart=cart
            )
            cart_item.save()
        return redirect('cart:cart_detail')
    return redirect('login')

def cart_detail(request,total=0,counter=0,cart_items=None):
    if request.user.is_authenticated:
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(user=request.user,cart=cart,active=True)
            for cart_item in cart_items:
                total+=(cart_item.product.price * cart_item.quantity)
                counter +=cart_item.quantity
                cart_item.save()

        except ObjectDoesNotExist:
            pass
        return render(request,'service/cart.html',dict(user=request.user,cart_items=cart_items,total=total,counter=counter))
    return redirect('login')

# def cart_info(request):
#     if request.user.is_authenticated:
#         cart = CartItem.objects.filter(user=request.user)
#         return render(request, "shopping/cart.html", {
#             'cart': cart,
#         })

    return redirect('login')



def full_remove(request,product_id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
        return redirect('cart:cart_detail')
    return redirect('login')