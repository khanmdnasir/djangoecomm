from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ValidationError
from django.http import response
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from .models import (Customer,Product,Cart,OrderPlaced)
from django.views import View
from django.contrib import messages
from .forms import CustomerRegistrationForm,ProfileForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def home(request):
    topwears=Product.objects.filter(category='TW')
    bottomwears=Product.objects.filter(category='BW')
    mobile=Product.objects.filter(category='M')
    laptop=Product.objects.filter(category='L')
    
    return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobile':mobile,'laptop':laptop})

def product_detail(request,pk):
    product=Product.objects.get(pk=pk)
    item_already_exist=False
    item_already_exist=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/productdetail.html',{'product':product,'item_already_exist':item_already_exist})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        sipping=70
        totalamount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                totalamount=amount+sipping
            return render(request,'app/addtocart.html',{'carts':cart,'amount':amount,'totalamount':totalamount})
        else:
            return render(request,'app/emptycart.html')

@login_required
def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        sipping=70
        totalamount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                totalamount=amount
            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+sipping
            }
            return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        sipping=70
        totalamount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                totalamount=amount
            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+sipping
            }
            return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.delete()
        amount=0.0
        sipping=70
        totalamount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                totalamount=amount
            data={
                'amount':amount,
                'totalamount':amount+sipping
            }
            return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def profile(request):
    form=ProfileForm()
    if request.method=='POST':
        form=ProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            zipcode=form.cleaned_data['zipcode']
            state=form.cleaned_data['state']
            reg=Customer(user=user,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
            reg.save()
            messages.success(request,'Profile Information Saved Successfully!')
    return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})

@login_required
def address(request):
    data=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'addresses':data,'active':'btn-primary'})
    
@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'orders':op})

@login_required
def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
        
    else:
        mobiles=Product.objects.filter(category='M').filter(brand=data)
        
    return render(request, 'app/mobile.html',{'mobiles':mobiles})


def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request=request,data=request.POST)
        form.fields['username'].widget.attrs['class']='form-control'
        form.fields['password'].widget.attrs['class']='form-control'
        if form.is_valid():
            uname=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=uname,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                return redirect('/login/')
        return render(request,'app/login.html',{'form':form})
    else:
        form=AuthenticationForm()
        form.fields['username'].widget.attrs['class']='form-control'
        form.fields['password'].widget.attrs['class']='form-control'
        return render(request, 'app/login.html',{'form':form})
# def change_password(request):
#     if request.method=='POST':
#         form=PasswordChangeForm(request=request,data=request.POST)
#         form.fields['old_password'].widget.attrs['class']='form-control'
#         form.fields['password1'].widget.attrs['class']='form-control'
#         form.fields['password2'].widget.attrs['class']='form-control'

#         if form.is_valid():
#             form.save()
#         return render(request,'app/changepassword.html',{'form':form})
#     else:
#         form=PasswordChangeForm()
#         form.fields['old_password'].widget.attrs['class']='form-control'
#         form.fields['password1'].widget.attrs['class']='form-control'
#         form.fields['password2'].widget.attrs['class']='form-control'
#         return render(request, 'app/changepassword.html',{'form':form})
# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
def CustomerRegistrationView(request):
    if request.method=='GET':
        form=CustomerRegistrationForm()
    else:
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Succesfully')
            form.save()
    return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    sipping=70
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        totalamount=amount+sipping
    return render(request, 'app/checkout.html',{'address':add,'cart_items':cart_items,'totalamount':totalamount})

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('/orders')