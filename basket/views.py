from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from store.models import Product
from .basket import Basket

def basket_summary(req):
    context = {'basket':Basket(req)}
    return render(req, 'store/basket/summary.html',context)

def basket_add(req):
    basket = Basket(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('productid'))
        qty = int(req.POST.get('productqty'))
        product = get_object_or_404(Product,id=product_id)
        basket.add(product=product, qty=qty)
        basketqty=basket.__len__()
        context = {'qty':basketqty}
        response = JsonResponse(context)
        return response
    
def basket_delete(req):
    
    basket = Basket(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('productid'))
        basket.delete(product=product_id)
        
        context = {'qty':basket.__len__(),
                   'subtotal':basket.get_total_price()
                }
        return JsonResponse((context))
    
def basket_update(req):
    basket = Basket(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('productid'))
        qty = int(req.POST.get('productqty'))
        basket.update(product=product_id, qty=qty)
        context = {'qty':basket.__len__(),
                   'subtotal':basket.get_total_price()
                }
        return JsonResponse((context))