"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from mainapp import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from mainapp.forms import (PwdResetConfirmForm, PwdResetForm)

name='mainapp'

handler500 = views.my_customized_server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login/', views.Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', views.signup),
    path('activate/<slug:uidb64>/<slug:token>', views.activate,name='activate'),
    #reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="mainapp/user/password_reset_form.html",
                                                                 success_url='password_reset_email_confirm',
                                                                 email_template_name='mainapp/user/password_reset_email.html',
                                                                 form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='mainapp/user/password_reset_confirm.html',
                                                                                                success_url='/password_reset_complete', 
                                                                                                form_class=PwdResetConfirmForm),
         name="password_reset_confirm"),
    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="mainapp/user/reset_status.html"), name='password_reset_done'),
    path('password_reset_complete/',
         TemplateView.as_view(template_name="mainapp/user/reset_status.html"), name='password_reset_complete'),
    path('account/', views.account),
    path('contact/', views.contact),
    path('quotation/', views.quotation),
    path('create-checkout-session', views.create_checkout_session),
    path('create-checkout-intent', views.CreateIntentView.as_view()),
    path('checkout/', views.checkout),
    path('checkout-confirm', views.checkout_confirm),
    path('success/',views.success),
    path('cancel/',views.cancel),
    path('blog/',include('blog.urls')),
    path('store/',include('store.urls',namespace='store')),
    path('basket/',include('basket.urls',namespace='basket')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
