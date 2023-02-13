from django.shortcuts import render,redirect
from blog.models import Article
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .tokens import account_activation_token
from .models.account_models import User
from mainapp.forms import UserCreationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import send_mail
from django.views.generic import View
import os

import json
import jsonify
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

def index(request):
    objs=Article.objects.all()
    context={
        'articles': objs
    }
    return render(request,'mainapp/index.html',context)

def signup(request):
    context={}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.is_active = False
            user.save()
            # login(request,user)
            # messages.success(request,"登録完了！")
            current_site = get_current_site(request)
            subject = 'Tuttofareアカウントをアクティベートしてください'
            message = render_to_string('mainapp/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('新規登録が成功しました。アクティベーション用のリンクをご登録メールにお送りしました。（迷惑メールフォルダに入っている可能性があります。）\
                                registered succesfully and activation sent')
        else:
            context = {'form':form}
    return render(request,'mainapp/auth.html',context)

def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        print('uid, userが見つかりません。')
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect('/')
    else:
        return render(request,'mainapp/registration/activation_invalid.html')
    
      
    

class Login(LoginView):
    template_name = 'mainapp/auth.html'

    def form_valid(self,form):
        messages.success(self.request, "ログイン完了！")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "ログイン失敗！")
        return super().form_invalid(form)

def logout(request):
    context={}
    return render(request,'mainapp/logout.html',context)

@login_required
def account(request):
    context={}
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        print(form)
        if form.is_valid():
           profile = form.save(commit=False)
           profile.user = request.user
           profile.save()
           messages.success(request,"更新完了！")
    return render(request,'mainapp/account.html',context)

def contact(request):
    context = {}
    if request.method == 'POST':
        subject = "お問い合わせがありました。"
        message = "お問い合わせがありました。\n名前: {}\nメールアドレス: {}\n内容: {}".format(
                    request.POST.get('name'),
                    request.POST.get('email'),
                    request.POST.get('content'))        
        
        email_from = os.environ['EMAIL_HOST_USER']
        email_to = [
        os.environ['EMAIL_HOST_USER'], 
        ]
        send_mail(subject,message, email_from,email_to)
        messages.success(request,'お問い合わせいただきありがとうございました。ご入力内容が送信されました。')
    return render(request,'mainapp/contact.html',context)
@csrf_exempt
def quotation(request):
    context={}
    return render(request,'mainapp/quotation.html',context)

def success(request):
    user = User.objects.get(id=request.user.id)
    context={"username": user.email}
    return render(request,'mainapp/success.html',context)

def cancel(request):
    context={}
    return render(request,'mainapp/cancel.html',context)

@require_POST
@login_required
def payment_method(request):
    
    automatic = request.POST.get('automatic','on')
    payment_method = request.POST.get('payment_method','card')
    context = {}
    
    payment_intent = stripe.PaymentIntent.create(
        amount = 1400,
        currency = 'jpy',
        payment_method_types=['card'],
        
    )
    
    if payment_method == 'card':
        context['secret_key'] = payment_intent.client_secret
        context['STRIPE_PUBLISHED_KEY'] = os.environ.get('STRIPE_PUBLISHED_KEY')
        context['customer_email'] = request.user.email
        return render(request,'mainapp/payments/card.html',context)


DOMAIN = "http://127.0.0.1:8000"

def create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                     'price': 'price_1LKcetDGjgnmtiVob0XW5mzW',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=DOMAIN + '/success',
            cancel_url=DOMAIN + '/cancel',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    amount = 0
    for item in items:
        amount += int(item)
    return amount

@method_decorator(csrf_exempt, name='dispatch')
class CreateIntentView(View):
    
    def post(self, request, *args, **kwargs):
        try:
         
            # ['items']
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=1400,
                currency='jpy',
                setup_future_usage='off_session',
                automatic_payment_methods={
                'enabled': True,
                },
            )
            #'STRIPE_PUBLISHED_KEY'=os.environ.get('STRIPE_PUBLISHED_KEY')
            context = {
                'clientSecret': intent['client_secret']
                
            }
            #return render(request,'mainapp/checkout.html',context)
            return JsonResponse(context)
        except Exception as e:
            return JsonResponse({"error":str(e)})

@login_required
def checkout(request):
    
    context={}
    return render(request,'mainapp/checkout_form.html',context)

@login_required
def checkout_confirm(request):
    
    user = User.objects.get(id=request.user.id)
    
    context={"email":user.email}
    return render(request,'mainapp/checkout.html',context)