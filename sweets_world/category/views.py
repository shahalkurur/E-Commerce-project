from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import *
from sweetapp.models import CustomUser, Profile
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# Create your views here.
from django.contrib import messages
import random
# from .forms import UserForm, UserProfileForm



from django.shortcuts import render, redirect, get_object_or_404
from .models import products, Cart

from django.http import JsonResponse
from .models import Cart, products


def store(request):
    Category=category.objects.all()  
    context={
        'category':Category,}
    return render(request,'store.html',context)

def price_filter(request):
    if request.method=='POST':
        selected_categories=request.POST.getlist('category')
        
        From=request.POST.get('price_from')
        To=request.POST.get('price_to')
        print(From,To)
        category_filter = Q()
        for cat_id in selected_categories:
            category_filter |= Q(category__id=cat_id)
        Products=products.objects.filter(category_filter,Q(price__gte=From) & Q(price__lte=To)).order_by('price')
        
        


        #here the pagination not working loading to home ie method
        page=1
        try:
            page = request.GET.get('page', 1)
            page = int(page)
        except ValueError:
            page = 1
        filter_paginator=Paginator(Products,4)
        prod_list=filter_paginator.get_page(page)
        Result_count=Products.count()
        Category=category.objects.all()
        context={
            'category':Category,
            'Products':Products,
            'count':Result_count
        }
        
        return render(request,'store.html',context)
    
    return redirect('home')

def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        result=products.objects.filter(prod_name__icontains=keyword)
        Result_count=result.count()

        cat=category.objects.all()
        context={'products':result,
                 'category':cat,
                 'count':Result_count}
    return render(request,'search_result.html',context)


def add_cart(request):
    if request.method=='POST':
        if request.user.is_authenticated:
           # Check if the required data is present in the POST request
          Prod_id = request.POST.get('prod_id')
          prd=request.POST.get('prod_qty')
          print(Prod_id,prd)
          prod_check=products.objects.get(id=Prod_id)
          
              
              
          
          if(prod_check):
                if(Cart.objects.filter(user=request.user, product_id=Prod_id)):
                     
                     return JsonResponse({'error': 'Product alredy in cart'})
                else:
                     product_qty = float(request.POST.get('prod_qty'))#bcose model stock field was float
                     
                     if prod_check.stock >= product_qty:
                        Cart.objects.create(product_id=Prod_id,
                                         user=request.user,
                                         quandity=product_qty)
                        
                        return JsonResponse({'status': 'Product added to cart'})
                        
                     
                     else:
                        return JsonResponse({'error': 'only'+ str(prod_check.stock)+'available'})           
          return JsonResponse({'error': 'no such Product'}) 
        else:
            return JsonResponse({'error': 'login to continue'})#return redirect('category/cart')
    return redirect('category/home')


    # wish list


@login_required(login_url='login')
def wish_list(request):
    
    wishlist=Wishlist.objects.filter(user=request.user)       
    context={
        'wishlist':wishlist    
    }
    return render(request,'cart/wishlist.html',context)

def addtowishlist(request):
    if request.method=='POST':
        prd_id=request.POST.get('prod_id')
        prod=products.objects.get(id=prd_id)
        if(prod):
            if (Wishlist.objects.filter(user=request.user,product=prod)):
                messages.error(request,"Product already in Wishlist")
                return JsonResponse({'status':"already added"})
            else:
                Wishlist.objects.create(user=request.user,product=prod)
                messages.success(request,'Product added successfully to Wishlist')
                
                return render('wishlist')
    return redirect('/')

def delete_wishlist(request,pk):

    data=Wishlist.objects.get(user=request.user,product_id=pk)
    data.delete()
    return redirect ('wishlist')

@csrf_exempt
@login_required(login_url='login')
def view_cart(request):
    
    user = request.user
    cart = Cart.objects.filter(user=user)
    coupen_obj=None
    total = 0
    quandity = 0
    if 'cancel' in request.POST:
        return redirect('cart')
    if request.method=='POST':
        coupen=request.POST.get('coupen')
        print(coupen)
        if coupen:
                try:
                    coupen_obj=Coupen.objects.get(code__icontains=coupen,is_active=True)
                    
                except:
                    messages.error(request,"Coupen not Valid")
                    return redirect('cart') 
    
    for p in cart:
        total += (p.product.price * p.quandity)
        quandity += p.quandity
    if coupen_obj:
             dis_pctg=coupen_obj.discount
             try:
                 discount= (dis_pctg* total) / 100
                 total=total-discount
                 messages.success(request,f'you got {dis_pctg}% discount')
                 print(total)              
             except:
                    pass
        
    tax = (2 * total) / 100
    grand = total + tax
    
    context = {
        'user': user,
        'cart': cart,
        'total': total,
        'quandity': quandity,
        'tax': tax,
        'grand': grand,
        'coupen':coupen_obj,
    }
    
    return render(request, 'cart/cart.html', context)


def cart_qty_update(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('prod_id'))
        qty = int(request.POST.get('new_quantity'))
        
        cart_=Cart.objects.get( user=request.user, product__id=prod_id)
       
        if(cart_):
           cart_.quandity =qty
           cart_.save()
      
    total=0
    
    tax=0;grand=0
    cart_=Cart.objects.get( user=request.user, product__id=prod_id)# find prod to change cart qty
         
    a=cart_.id
    print(a)
    
    subtotal = cart_.sub_total()
    cart=Cart.objects.filter( user=request.user)
    for item in cart:
        total+=item.sub_total()
    
    subtotal_data= subtotal
    

    tax = (2 * total) / 100

    
    grand = total + tax
    data={ 
            
        'quandity':qty,
        'grand':grand,
        'tax':tax,
        'total':total,
        'subtotals':subtotal_data,
        'item_id_':a   
        
    }
    print(data)              
    return JsonResponse(data)


    
@csrf_exempt
def cart(request):
    return render(request,'cart/cart.html')


def delete_cart(request,id):
    user=request.user
    product=get_object_or_404(products,id=id)
    cart_item=Cart.objects.filter(product=product,user=user)
    cart_item.delete()
    return redirect('cart') 
  
@login_required(login_url='login')
def check_out(request):
    user=request.user
    wal=None
    total=0
    coupen=None
    total_amount=0
    grnd_total=0
    user_profile=Profile.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    addrs=Address.objects.filter(user=user,is_deleted=False)
    
    
                           
    id=request.POST.get('coupen')
    if id:
        coupen=Coupen.objects.get(id=id)
        dis_pctg=coupen.discount
        for i in cart_items:
            total += i.product.price* i.quandity
        dis= (dis_pctg* total) / 100
        total=total-dis
        tax=(2 * total) / 100
        total_amount=tax+total 
               

    total=0
    for i in cart_items:
        total += (i.product.price * i.quandity)
   
    tax=(2 * total) / 100
    grnd_total=tax+total
                   
    try:
        wal = CustomUser.objects.get(email=user)     
    except:
          pass
    
    
    if wal.my_wallet >= grnd_total or wal.my_wallet >=total_amount and total_amount!=0 :
        flag='True'
    elif wal.my_wallet < (grnd_total or total_amount):
        flag='False'
    
    context={'flag':flag,'amount':total_amount,'wallet':wal,'addrs':addrs,
             'grand':grnd_total,'coupen':coupen,'cart_items':cart_items}
    return render(request,'cart/checkout.html',context)


@login_required(login_url='login')
def add_address(request):
    if request.method=="POST":
        fname=request.POST.get('first_name')
        lname=request.POST.get('last_name')
        email=request.POST.get('email')
        ph=request.POST.get('phoneNumber')
        add=request.POST.get('address')
        state=request.POST.get('state')
        pin=request.POST.get('pin')
        print(fname,state,add)
        print('kkkkkk')
        return redirect('check_out')
        
        
        
        # adrs=Address.objects.create(
        #     user=request.user,
        #     first_name=fname,
        #     last_name=lname,
        #     email=email,
        #     phoneNumber=ph,
        #     addressline1=add,
        #     state=state,
        #     pin=pin
            
        # )
        # print(adrs)
        # print(adrs.id)

    pass    
    context={
        
    }
        
    return render(request,'checkout.html',context)


@login_required(login_url='login')
def placeorder(request):
    
    if request.method=='POST':
        
        current_user=CustomUser.objects.filter(id=request.user.id).first()
        address_id=request.POST.get('address')
        
        addrs=Address.objects.filter(id=address_id).first()
        # print(addrs.first_name)
        

        #checking wallet have sufficient amount if ;then use
        
        pay_mode=request.POST.get('paymentmode')
       

        if pay_mode=='wallet':
            total=request.POST.get('wallet_pay')
            

            if current_user.my_wallet >= float(total):
                    current_user.my_wallet -= float(total)
                    current_user.save()                  
            else:                   
                    messages.error(request,"Dont have sufficient amount in Wallet")
                    return redirect('check_out')
        else:
            total=request.POST.get('total')
        neworder=Order()
        if address_id:
            neworder.user=request.user
            neworder.f_name=addrs.first_name
            neworder.l_name=addrs.last_name
            neworder.address=addrs.addressline1
            neworder.mobile=addrs.phoneNumber
            neworder.state=addrs.state
        else:
            neworder.user=request.user
            neworder.f_name=request.POST.get('first_name')
            print(f'neworder-{neworder.f_name}')
            neworder.l_name=request.POST.get('')
            neworder.address=request.POST.get('')
            neworder.mobile=request.POST.get('')
            neworder.state=request.POST.get('')
        #     # current_user.save()

        # if not Profile.objects.filter(user=request.user):
        #     profile_user=Profile()
        #     profile_user.address=request.POST.get('address')
        #     profile_user.country=request.POST.get('country')
        #     profile_user.state=request.POST.get('state')
        #     profile_user.city=request.POST.get('city')
        #     # profile_user.save()


                # neworder=Order()
                # neworder.user=request.user
                # neworder.f_name=request.POST.get('fname')
                # neworder.l_name=request.POST.get('lastname')
                # neworder.email=request.POST.get('email')
                # neworder.mobile=request.POST.get('phonenumber')
                # neworder.address=request.POST.get('address')
                # neworder.country=request.POST.get('country')
                # neworder.state=request.POST.get('state')
                # neworder.pincode='121'
                # neworder.city=request.POST.get('city')
                # neworder.payment_mode=request.POST.get('paymentmode')
                # neworder.payment_id=request.POST.get('payment_id')
                # neworder.total_price=total
        
        #instead of calculating send total amont from the page
        # cart=Cart.objects.filter(user=request.user)
        # total=0
        # cart_total=0
        # for item in cart:
        #      total += item.product.price* item.quandity
        # tax=(2 * total) / 100
        # cart_total=tax+total
        
        

        # trck_no=random.randint(111111,999999)
        # while Order.objects.filter(tracking_no=trck_no) is None:
        #     trck_no=random.randint(111111,999999)
        # neworder.tracking_no=trck_no
        # neworder.save()

        neworder_items=Cart.objects.filter(user=request.user)
        # for item in neworder_items:
        #     OrderItem.objects.create(
        #         order=neworder,
        #         price=item.product.price,
        #         product=item.product,
        #         quandity=item.quandity
        #     )
        #to update product stock in product table
            # order_product=products.objects.filter(id=item.product_id).first()
            # if order_product:
            #     order_product.stock=order_product.stock-item.quandity
            #     order_product.save()
        #to clear user's cart
        # Cart.objects.filter(user=request.user).delete()

        paymode=request.POST.get('paymentmode')
        
        if paymode=='Paid by paypal':
             JsonResponse({'status':"your order hasbeen placed by paypal"})
        else:
            messages.success(request,'your order hasbeen placed')

            return HttpResponse('order_success')  
    else :
        return redirect ('/')
     


@login_required(login_url='login')
def user_dashboard(request):
    #to find count of orders
    orders=Order.objects.order_by('created_at').filter(user_id=request.user.id)
    ord_count=orders.count()
    
    wal=CustomUser.objects.get(email=request.user)
    print(type(wal.my_wallet))

    
    return render(request,'dashboard.html',{'ord_count':ord_count,'wallet':wal})

def my_orders(request):

    orders=Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request,'cart/my_orders.html',{'orders':orders})




from sweetapp.forms import UserForm, UserProfileForm

@login_required(login_url='login')
def edit_profile(request): 

    user = request.user    
    userprofile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Error updating profile. Please check the form.')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=userprofile)

    return render(request, 'cart/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required(login_url='login')
def change_password(request):

    if request.method=='POST':
      current_pswd=request.POST['current_pswd']
      new_pswd=request.POST['new_pswd']
      confirm_pswd=request.POST['confirm_pswd']

      user=CustomUser.objects.get(username__exact=request.user.username)

      if new_pswd == confirm_pswd:
          success=user.check_password(current_pswd)#pswd cant check without inbuild bcos hashed pswd
          if success:
              user.set_password(new_pswd)
              user.save()
              #auth.logout(request)
              messages.success(request,'password changed')
              return redirect('change_password')
          else:
              messages.error(request,'wrong password')
              return redirect('change_password')
      else:
         messages.error(request,'password does not match')
         return redirect('change_password')
          
    return render(request,'cart/change_pswd.html')


def order_details(request,pk):
    
    user=request.user
    total=0
    sub_total=0
    tax=0
   
    orders=Order.objects.get(tracking_no=pk,user=user)
    print(orders)
    orderitem=OrderItem.objects.filter(order=orders)
    print(orderitem)
    for i in orderitem:
        sub_total += i.product.price * i.quandity
        
    tax=(2 * sub_total) / 100
    total=tax+sub_total
    context={
        'total':total,    
        'orderitem':orderitem ,
        
        'orderstatuses': orders.orderstatuses
    }
    return render(request,'cart/order_details.html',context)

def cancel_order(request,pk):
        order=Order.objects.get(id=pk)
        
        custom_user=CustomUser.objects.get(email=request.user)        
        orderitems=OrderItem.objects.filter(order_id=pk)
        

        for orderitem in orderitems:
             orderitem.product.stock +=orderitem.quandity  #return product  stock to server
             orderitem.product.save()

        if  order.status=='Delivered' or order.status=='Complete':
            wal=Wallet.objects.create(
                user=request.user,
                amount=order.total_price,
                order=order
            )
            wal.save()
            # print(type(order.total_price),order.total_price)
            # print(custom_user.my_wallet)
            custom_user.my_wallet += order.total_price # round(order.total_price, 2)
            
            # print(type(custom_user.my_wallet))
            # print(custom_user.my_wallet)
            custom_user.save()
            order.status='Refund'
            order.save()

        else:
             order.status=='cancel'
             order.save()
        
        return redirect('my_orders')


         # razor pay functions

def razor_pay(request):
    cart_items=Cart.objects.filter(user=request.user)
    total=0
    grnd_total=0
    for item in cart_items:
        total += item.product.price* item.quandity
    tax=(2 * total) / 100
    grnd_total=tax+total
    

    context={'grand_total':grnd_total,'cart_items':cart_items}
    print(grnd_total)
    return JsonResponse({
        'grand_total':grnd_total,
        
    })

def orders(request):
    return HttpResponse('my order')


def order_success(request,order_id):
    print(order_id)
    neworder=Order.objects.get(id=order_id)
    print(neworder.tracking_no,neworder.total_price)

    return render(request,'dd.html',{'neworder':neworder})



            