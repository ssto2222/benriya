from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render

from basket.basket import Basket

from .models import Order, OrderItem
from mainapp.models.profile_models import Profile
from django.contrib.auth import get_user_model
import os
import stripe

def test(request):
    profile=Profile.objects.get(user=request.user)
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    if profile.stripe_id != "":
        customer= stripe.Customer.retrieve(profile.stripe_id)
        print(customer)
        return HttpResponse('success')

def add(request):
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = basket.get_total_price()
        fullname = request.POST.get('fullname')
        add1 = request.POST.get('add1')
        add2 = request.POST.get('add2')
        postcode = request.POST.get('postcode')
        ordertotal = basket.get_total_price()
        
        payment_intent_id = request.POST['payment_intent_id']
        payment_method_id = request.POST['payment_method_id']
        
        profile = Profile.objects.get(user=request.user)
        
        if profile.stripe_id != "":
            try:
                customer= stripe.Customer.retrieve(profile.stripe_id)
                payment_method_id = customer.invoice_settings.default_payment_method
            except:
                print(f'customer {profile.stripe_id} does not exist.')
            
        else:
            customer = stripe.Customer.create(
                    name = fullname + "様",
                    email = request.user.email,
                    payment_method = payment_method_id,
                    invoice_settings = {
                        'default_payment_method': payment_method_id
                    }
                )
            profile.stripe_id = customer.id
            profile.save()
        
        
        
        stripe.PaymentIntent.modify(
            
            payment_intent_id,
            customer=customer,
            payment_method=payment_method_id
        )
    
        stripe.PaymentIntent.confirm(
                    payment_intent_id
                    )
        
        
        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, 
                                        full_name=fullname, 
                                        address1=add1,
                                        address2=add2, 
                                        post_code=postcode,
                                        total_paid=baskettotal,
                                        order_total=ordertotal,
                                        order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': 'Adding oder to the list succeeded'})
       
        return response
    


def prepayment_confirmation(data):
    Order.objects.filter(order_key=data).update(prebilling_status=True)

def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders