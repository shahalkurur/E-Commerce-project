
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.db import transaction
from decimal import Decimal
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator


from reportlab.pdfgen import canvas
from io import BytesIO

from .models import CustomUser
from category.models import *
from django.core.mail import send_mail
import random

import time
from datetime import datetime,timedelta,date

#regarding forgot password
from django.contrib.sites.shortcuts import get_current_site  # Import get_current_site
from django.contrib.auth.tokens import default_token_generator  # Fix typo in import
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

from .forms import DateForm
def otp_verification(request):
    if request.method == 'POST':
        otp_ = request.POST.get("otp")
        email = request.session.get('email')
        password=request.session.get('password')
        otp_expiration_time = request.session.get('otp_expiration_time')
        print(f"otp veri : {email},{request.session.get('password')},{request.session.get('username')},{otp_expiration_time}")


        if not email:
            messages.error(request, "Email not found in the session")

        if int(time.time()) <= otp_expiration_time:
            if otp_ == request.session.get("otp") and email:
               
               username=request.session.get('username')
               mobile=request.session.get('mobile')
               user=CustomUser.objects.create_user(username=username,email=email,password=password,mobile=mobile)
               user.save()
               del request.session['email']
               del request.session['otp']
               del request.session['otp_expiration_time']
               auth.login(request, user)
               response = redirect('home')
               return response
            
            else:
                messages.error(request, "OTP does not match")
                return render (request, 'app/otp.html')
        else:
            messages.error(request, 'OTP expired')
            return redirect('signup')
    else:
        messages.error(request, "not post")
        return redirect('signup')

def home(request):
   cat=category.objects.filter(status=0).order_by('id')
   pro=products.objects.filter(status=0).order_by('id')

   context={
       'Category':cat,
       'Product':pro
   }
   return render(request, 'index.html',context) 
def signup(request):
  return render(request,'app/signup.html')
def login_page(request):
    return render(request,'app/login.html')


@login_required(login_url='login')
def logout_user(request):
  
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('home')#(request,'index.html')





def user_login(request):
    if request.method == 'POST':
        user_email = request.POST['email']
        user_password = request.POST['password']

        

        user = authenticate(request, email=user_email, password=user_password)
        
        if user is not None:
            if user.is_superuser:
               login(request, user)
               return redirect('admin_dsh')
            else:
                
                login(request, user)
                messages.success(request,'you are now logged in')
                return redirect ('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'app/login.html')


def signup_verification(request):
   if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        mobile = request.POST.get('mobile')
       
        
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup_verification')
        
        # if not validate_email(email):
        #     messages.error(request, 'Please enter a valid email address.')
        #     return redirect('login')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('login')
        send_otp(request, email)
        request.session['email'] = email
        request.session['username']=username
        request.session['mobile']=mobile
        request.session['password']=password1
        
        return render(request, 'app/otp.html', {"email": email})
        
   else:
        return render(request, 'app/signup.html')
   

def send_otp(request, email,expiry_time=60):
    current_time = int(time.time())
    expiration_time = current_time + expiry_time
    request.session['otp_expiration_time'] = expiration_time

    s = "".join(random.choices("0123456789", k=4))
    request.session["otp"] = s
    send_mail("OTP for sign up", s, 'shahalkurur@gmail.com', [email], fail_silently=False)
    return render(request, "app/otp.html")

def forgot_password(request):

    if request.method=='POST':
        email=request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email__exact=email)
            current_site = request.get_host()
            
            mail_subject = 'reset your password'
            message = render_to_string('app/reset_pswd_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_mail = email
            send_email = EmailMessage(mail_subject, message, to=[to_mail])
            send_email.send()
            

            messages.success(request, 'password reset Email sent')
            return redirect('login')  # Use redirect instead of render to navigate to login
        else:
            
            messages.error(request, 'Email does not exist')
            return redirect('forgot_password')

    return render(request, 'app/forgot_pswd.html')

def resetpassword_validate(request,uidb64,token):

    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user=CustomUser._default_manager.get(pk=uid)
        
    except(TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
        user=None
        
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'reset your password')
        return redirect('resetpassword')
    else:
        
        messages.error(request,'link expired')
        return redirect('login')



def resetpassword(request):
    if request.method=='POST':
        new_pswd=request.POST['password_1']
        cnf_pswd=request.POST['password_2']
        if new_pswd==cnf_pswd:
           uid= request.session['uid']
           user=CustomUser.objects.get(pk=uid)
           user.set_password(new_pswd)
           user.save()
           messages.success(request,'Password reset successfully')
           return redirect('login')
        else:
            messages.error(request,'both password not match')
            
            return redirect('resetpassword')
    return render(request,'app/resetpassword.html')





              #  ADMIN  SIDE MANAGEMENT





def manage_user(request):
        users = CustomUser.objects.filter(is_staff= False).values('id', 'username', 'email', 'mobile', 'is_active')
        # page=Paginator(users,10)
        # page_number = request.GET.get('page')
        # users = page.get_page(page_number)
        context = {
                'users': users,
            }
        return render(request,'adm/manage_user.html',context)


def block_user(request,id):
    user=CustomUser.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect('manage_user')

def unblock_user(request,id):
    user=CustomUser.objects.get(id=id)
    
    user.is_active=True
    user.save()
    return redirect('manage_user')



def admin_dsh(request):
    if request.user.is_authenticated:
        
        
        return render(request,'adm/base.html')
    else:
        return render(request,'app/home.html')
    
#  admin category management 
def signout_adm(request):
    if 'login' in request.session:
        del request.session['login']
        auth.logout(request)
    return redirect('home')


def manage_category(request):
    Category=category.objects.filter(status=0).values('id','category_name').order_by('id')
    context = {'Category': Category}
    return render(request,'adm/manage_category.html',context)



def add_category(request):
    if request.method=='POST':
      name=request.POST.get('name')
      image=request.FILES.get('image')
      category.objects.create(category_name=name,cat_image=image)
      return redirect('manage_category')
    return render(request,'adm/add_category.html')
    
def edit_category(request,id):
    cat=category.objects.get(id=id)
    if request.method=='POST':
      name=request.POST.get('name') 
      image=request.FILES.get('image')
      
      if name:
            cat.category_name = name
      if image:
            cat.cat_image = image
      cat.save()
      return redirect('manage_category')
    return render (request,'adm/edit_category.html',{'cat':cat})

def delete_category(request,id):
        category.objects.get(id=id).delete()
        return redirect('manage_category')

 #  admin product management 


def manage_products(request):
    Products=products.objects.filter(is_available='True').order_by('id')
    context={'Products':Products}
    return render(request,'adm/manage_products.html',context)

def add_products(request):
    
    if request.method=='POST':
       cat_id=request.POST.get('category')#will print cat id
       
       cat_inst=category.objects.get(id=cat_id)#will print catgry name
       
       pr_name=request.POST.get('name')
       pr_image=request.FILES.get('image')
       price=request.POST.get('price')
       stock=request.POST.get('stock')
       discription=request.POST.get('discription')

       p=products.objects.create(
           category=cat_inst,prod_name=pr_name,prod_image=pr_image,price=price,stock=stock,description=discription)#des dis
       print(p)
       return redirect('manage_products')
    Category=category.objects.filter(status=0).values('id','category_name').order_by('id')
    context = {'Category': Category}
    return render(request,'adm/add_products.html',context)

from .forms import image_form

def edit_products(request,id):
    
   
    form=image_form(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        return HttpResponse('OK')
    
    prod=products.objects.get(id=id)
    #Products=products.objects.filter(status=0)
    Category = category.objects.all()
    context = {'Category': Category,
                'prod': prod,
                'form':form}
    return render(request,'adm/edit_products.html',context)

def update_product(request,id):     #when did with edit-prodct not fetch the cat_id show empty strng
    cat=category.objects.all()
    prod=products.objects.get(id=id)
    if request.method=='POST':
       
       print(f"prod id {prod}")
       name=request.POST['name']   
       if name:
           prod.prod_name=name 
       img = request.FILES.get('image')
       if img:
           prod.prod_image=img  
       price=request.POST.get('price')
       if price:
           prod.price=price
       cate= request.POST.get('category')
       if cate: 
             pro_key = category.objects.get(id=cate)
             prod.category = pro_key
       stock=request.POST.get('stock')
       if stock:
           prod.stock=stock
       des=request.POST['discription']
       if des:
           prod.description=des
        
       print(f"catgry name {pro_key}")# just checking oupt only not needed
       prod.save()
       return redirect('manage_products')
    
    context={
      'cat':cat,'prod':prod
             }
    return render(request,'adm/edite_products.html',context)

def delete_products(request,id):
        prod=products.objects.get(id=id)
        prod.is_available='False'
        prod.save()
        return redirect('manage_products')



def manage_orders(request):
    orderitem=Order.objects.all().order_by('-created_at')

    context={'orderitem':orderitem}
    return render(request,'adm/manage_orders.html',context)

def status_update(request,pk):
        if request.method=='POST':
             new_status=request.POST.get('status')
             user=request.user
             
             order=Order.objects.filter(id=pk).first()
             
             custom_user=CustomUser.objects.get(id=pk)
             custom_user.my_wallet += order.total_price
             custom_user.save()
             print('www',custom_user.my_wallet,request.user)

             if new_status == 'Cancel':
                wal=Wallet.objects.create(
                user=user,
                amount=order.total_price,
                order=order)
                wal.save()
                print(wal.amount)
             
             order.status=new_status
             order.save()
             return redirect('manage_orders')
def manage_coupens(request):
    coupens=Coupen.objects.all()
    context={'coupens':coupens}
    return render(request,'adm/coupen.html',context)

def add_coupen(request):
    code=request.POST.get('code')
    dis_percentage=request.POST.get('discount')
    start=request.POST.get('start')
    end=request.POST.get('end')
    min_amount=request.POST.get('min-amount')

    coupen=Coupen.objects.create(code=code,
                          discount=dis_percentage,
                          start_date=start,
                          end_date=end,
                          )
    coupen.save()
    messages.success(request,"Created coupen code")
    return redirect('manage_coupens')

def activate_coupen(request,id):
    val=request.POST.get('action')
    coupen=Coupen.objects.get(id=id)
    print(val,coupen)
    coupen.is_active=val
    coupen.save()
    return redirect('manage_coupens')


      # OFFER MANAGEMENT 


def manage_offer(request):
    cat=category.objects.all()
    offer_data = ProductOffer.objects.all()
    
    return render(request,'adm/offer.html',{'category':cat,'offer_data':offer_data})


@require_POST
@csrf_protect
@csrf_exempt
def add_category_offer(request):
    try:
        category_id = request.POST.get('category')
        discount_type = request.POST.get('discountType')
        percentage = request.POST.get('percentage')
        start_date_str = request.POST.get('startDate')
        end_date_str = request.POST.get('endDate')

        Cat_id = category.objects.get(id=category_id)
        

        start_date_naive = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date_naive = datetime.strptime(end_date_str, '%Y-%m-%d')

        start_date = timezone.make_aware(start_date_naive, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date_naive, timezone.get_current_timezone())
        print('dddd')

        existing_offer = ProductOffer.objects.filter(category=Cat_id, expire_date__gt=timezone.now()).first()
        if existing_offer:
            raise ValueError("An active offer already exists for this category. Please update the existing offer or choose a different category.")

        offer = ProductOffer(
            category=Cat_id,
            discount_type=discount_type,
            discount_value=percentage,
            start_date=start_date,
            expire_date=end_date
        )
        if discount_type != 'fixed' and int(percentage) > 99:
             raise ValueError("Percentage is up to 99")
        if not offer.is_valid_for_category():
            raise ValueError("Category offer is not valid.")

        with transaction.atomic():
            # Create the category offer
            offer.save()

           
            Products = products.objects.filter(category=Cat_id)
            
            
            for product in Products:
                if discount_type == 'fixed':
                    print(f'create old{product.old_price}prod{product.price}')
                    product.dis_price = product.old_price
                    product.old_price=product.price
                    percentage = float(str(percentage))  # Convert to Decimal
                    product.price = product.price - percentage
                else:
                    product.dis_price = product.old_price
                    product.old_price=product.price
                    percentage = float(str(percentage))  # Convert to Decimal
                    product.price = product.price - (percentage / 100) * product.price
                
                product.has_offer = True
                print(f'discount {percentage,product.price}')
                product.save()

        response_data = {'success': True, 'message': 'Category offer added successfully'}
    except ObjectDoesNotExist as e:
       
        response_data = {'success': False, 'message': 'Invalid category ID'}
    except IntegrityError:
        response_data = {'success': False, 'message': 'An offer for this category already exists'}
    except ValueError as e:
        response_data = {'success': False, 'message': str(e)}
    except Exception as e:
        response_data = {'success': False, 'message': str(e)}

    return JsonResponse(response_data)

@require_http_methods(['DELETE'])
@csrf_exempt
def delete_category_offer(request,offer_id):
    print(offer_id)
    try:
        offer = ProductOffer.objects.get(id=offer_id)
        offer.delete()
        Products = products.objects.filter(category=offer.category)
        for product in Products:
                print(f'old{product.old_price}dis{product.dis_price}')
                product.price = product.old_price
                product.old_price = product.dis_price
                product.dis_price = 0
                product.has_offer = False 
                product.save()

        response_data = {'success': True, 'message': 'Category offer deleted successfully'}
    except ObjectDoesNotExist:
        response_data = {'success': False, 'message': 'Invalid offer ID'}
    except Exception as e:
        response_data = {'success': False, 'message': str(e)}

    return JsonResponse(response_data) 
  

def generate_pdf(request):
    
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    orders = Order.objects.all()

   
    headers = ["Customer", "CONTACT", "DATE", "Total Paid"]
    col_widths = [pdf.stringWidth(header, "Helvetica", 25) for header in headers]


    col_widths[2] += 20  


    line_height = 34

    
    table_start_x = 100  
    y_position = 750

    for i, header in enumerate(headers):
        pdf.drawString(table_start_x + sum(col_widths[:i]), y_position - line_height, header)

    for order in orders:
        y_position -= line_height
        for i, value in enumerate([order.f_name, order.mobile, order.created_at.strftime('%Y-%m-%d'), str(order.total_price)]):
           
            if i == 2:
                pdf.setFont("Helvetica", 8)
                pdf.drawString(table_start_x + sum(col_widths[:i]), y_position - line_height, value)
                pdf.setFont("Helvetica", 10)  # Resetting the font size to the default
            else:
                pdf.drawString(table_start_x + sum(col_widths[:i]), y_position - line_height, str(value))

    pdf.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orders.pdf"'
    return response 



from django.http import FileResponse
import io
from reportlab.lib.units import inch

def generatepdf(request,id):
    
    buf= io.BytesIO()
    c= canvas.Canvas(buf,pagesize=letter, bottomup=0)
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    orders = Order.objects.filter(id=id)
    print(orders)
    order_items = OrderItem.objects.filter(order_id=id)
    print(order_items)
    lines = []
    lines.append("Sweets World")    
    lines.append("Invoice:")    
    for o in orders:
        for i in order_items:
            lines.append(f"Name: {o.address.first_name} {o.address.last_name}")
            lines.append(f"Product: {i.product.prod_name}")
            lines.append(f"Quantity: {i.quandity}")
            lines.append(f"Price: {i.product.price}")
            lines.append(f"Payment Type: {o.payment_mode}")
            lines.append(f"Order Id: {o.tracking_no}")
            lines.append(f"Amount: {o.total_price}")
            lines.append(f"Address: {o.address.addressline1},phno:{o.address.phone_number},state:{o.address.state}")
            lines.append("")
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
        
    return FileResponse(buf,as_attachment=True,filename='invoice.pdf')



    
    
        








def cat_by_prod(request,id):
        catid=id
        print('sss')
        try:
            cat = category.objects.get(id=id)
        except category.DoesNotExist:
        # Handle the case where the category with the given id doesn't exist
             return HttpResponseNotFound("Category not found")
        sortBy = request.POST.get('sort')
        print(sortBy)
        if sortBy == "Position" :
            prod= products.objects.filter(category=cat,is_available=True)
        elif sortBy == 'Name Ascen':
            prod= products.objects.filter(category=cat).order_by('prod_name')
            
        elif sortBy == 'Name Decen':
            prod= products.objects.filter(category=cat,is_available=True).order_by('-prod_name')
        elif sortBy == 'Price Ascen':
            prod= products.objects.filter(category=cat,is_available=True).order_by('price')
        elif sortBy == 'Price Decen':
            prod= products.objects.filter(category=cat,is_available=True).order_by('-price')   
        else:
            prod=products.objects.filter(category=cat).order_by('id') 
        print(prod)
            
       
        page = request.GET.get('page', 1)
        prod_paginator=Paginator(prod,4)
        prod_list=prod_paginator.get_page(page)
        
        

        context={'Products':prod_list,'cat_id':catid}
        return render(request,'cat_by_prod.html',context)

def product_detail(request,id):
    
    prod=products.objects.filter(id=id)
    context={'product':prod}
    return render(request,'product_details.html',context)



#    salaes report


from django.shortcuts import render, redirect
from .forms import DateForm
from datetime import datetime
from django.db.models import Sum


from django.shortcuts import render
from .forms import DateForm

def daily_sales_report(request):
    selected_date = None
    t_amount=0 ;t_order=0

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['salesdate']
            print(selected_date)
            dateorder=Order.objects.filter(created_at__date=selected_date,status__in=['Out for shipping','Delivered'])
            for i in dateorder:
                 t_amount += i.total_price
                 t_order +=1
    else:
        form = DateForm()
    context={'form':form,
             'selected_date':selected_date,
             't_amount':t_amount,
             't_order':t_order, 
             }
    return render(request, 'adm/sales_graph.html',context)

def monthly_sales(request):
    
    if request.method=='POST':
        month=request.POST.get('month')
        t_amount = 0; t_order=0
        order=Order.objects.filter(created_at__month=month,status__in=['Out for shipping','Delivered'])
        for i in order:
                 t_amount += i.total_price
                 t_order +=1
        print(t_amount,t_order)

        

    context={'t_amount':t_amount,
             't_order':t_order,
             'month':month}




    return render(request, 'adm/base.html',context)

from django.db.models import Q
def year_sales(request):
    if request.method=='POST':
        year=request.POST.get('selected_year')
        t_amount=0 ;t_order =0
        order=Order.objects.filter(created_at__year=year,status__in=['Out for shipping','Delivered'])
        for i in order:
                 t_amount += i.total_price
                 t_order +=1

    context={'t_amount':t_amount,
             't_order':t_order,
             'year':year}
    return render(request, 'adm/base.html',context)
from django.utils import timezone

def period_of_sale(request):
    if request.method=='POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')


        t_amount=0; t_order=0
        order=Order.objects.filter((Q(created_at__gte=from_date) & Q(created_at__lte=to_date)),status__in=['Out for shipping','Delivered'])
        for i in order:
                 t_amount += i.total_price
                 t_order +=1
        context={'t_amount':t_amount,
                 't_order':t_order,
                 'order':order,
                 'from_date':from_date,
                 'to_date':to_date}

    return render(request, 'adm/base.html',context)

from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from django.db.models import Count, Avg
import calendar


def sale_graph(request):
    active_users = CustomUser.objects.filter(is_active=True).exclude(is_superuser=True)
    total_active_users_count=active_users.count()
    total_orders_count = Order.objects.count()

    total_income = Order.objects.filter(Q(status='Delivered')|Q(status='Complete')).aggregate(total_income=Sum('total_price'))['total_income'] or 0
    
    orders=Order.objects.filter(Q(status='Delivered')|Q(status='Complete'))
    
   
    
    # Monthly sales data
    orders_month_report = (
        Order.objects.annotate(month=ExtractMonth("created_at"))
        .values("month")
        .annotate(monthly_orders_count=Count("id"))
        .annotate(monthly_sales=Sum("total_price"))
        .values("month", "monthly_orders_count", "monthly_sales"))

    month = []
    total_orders_per_month = []
    total_sales_per_month = []

    for order in orders_month_report:
        month.append(calendar.month_name[order["month"]])
        total_orders_per_month.append(order["monthly_orders_count"])
        total_sales_per_month.append(order["monthly_sales"])
    # print('month',month)
    # print(total_orders_per_month)
    # print(total_sales_per_month)


    current_month = timezone.now().month
    current_year = timezone.now().year
    
    
    orders_daily_report = (
        Order.objects.filter(Q(status='Delivered')|Q(status='Complete'))  # Adjust the status filter as needed
        .filter(created_at__month=current_month,created_at__year=current_year)
        .annotate(day=ExtractDay("created_at"))
        .values("day")
        .annotate(daily_orders_count=Count("id"))
        .annotate(daily_sales=Sum("total_price"))
        .values("day", "daily_orders_count", "daily_sales")
)

    day = []
    total_orders_per_day = []
    total_sales_per_day = []

    for order in orders_daily_report:
        day.append(order["day"])
        total_orders_per_day.append(order["daily_orders_count"])
        total_sales_per_day.append(order["daily_sales"])
    print(day)
    print(total_orders_per_day)
    print(total_sales_per_day)

    product_data = []
    productss=products.objects.filter(is_available='True')
    for product in productss:
        total_quantity_sold = OrderItem.objects.filter(product=product).aggregate(Sum('quandity'))['quandity__sum'] or 0
        total_incom = total_quantity_sold * product.price
        
        product_data.append({
            'product': product,
            'total_quantity_sold': total_quantity_sold,
            'total_incom': total_incom,
        })
    
    # Yearly sales count
    orders_year_report = (
        Order.objects.annotate(year=ExtractYear("created_at"))
        .values("year")
        .annotate(yearly_orders_count=Count("id"))
        .annotate(yearly_sales=Sum("total_price"))
        .values("year", "yearly_orders_count", "yearly_sales")
    )
    year = []
    total_orders_per_year = []
    total_sales_per_year = []

    for order in orders_year_report:
        year.append(order["year"])
        total_orders_per_year.append(order["yearly_orders_count"])
        total_sales_per_year.append(order["yearly_sales"])
    


    order_items = Order.objects.aggregate(order_sum=Sum("total_price"))
    
    data={
        'product_data':product_data,
        'orders':orders,
        'total_income':total_income,
        'total_orders_count':total_orders_count,
        'total_orders_per_day':total_orders_per_day,
        'total_sales_per_day':total_sales_per_day,
        "total_active_users_count": total_active_users_count,
        "sales": order_items,
        "month": month,
        "total_orders_per_month": total_orders_per_month,
        "total_sales_per_month": total_sales_per_month,

        "year": year,
        "total_orders_per_year": total_orders_per_year,
        "total_sales_per_year": total_sales_per_year,

        "day": day,
        "total_orders_per_day": total_orders_per_day,
        "total_sales_per_day": total_sales_per_day,

    }
    return render(request,'adm/sales_graph.html',data)


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def generate_pdf(request):
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    pdf = canvas.Canvas(buffer,pagesize=letter)

    orders = Order.objects.all()

   
    headers = ["Customer", "CONTACT",'ORDER NO', "DATE", "Total Paid"]
    col_widths = [pdf.stringWidth(header, "Helvetica", 25) for header in headers]


    col_widths[2] += 20 


    line_height = 34

    
    table_start_x = 100  
    y_position = 750

    for i, header in enumerate(headers):
        pdf.drawString(table_start_x + sum(col_widths[:i]), y_position - line_height, header)

    for order in orders:
        y_position -= line_height
        for i, value in enumerate([order.address.first_name, order.address.phone_number,order.tracking_no, order.created_at.strftime('%Y-%m-%d'), str(order.total_price)]):
           

            if i == 2:
                pdf.setFont("Helvetica", 8)
                pdf.drawString(table_start_x + sum(col_widths[:i]), y_position - line_height, value)
                pdf.setFont("Helvetica", 10)  # Resetting the font size to the default
            else:
                pdf.drawString(table_start_x + sum(col_widths[:i]), y_position - line_height, str(value))

    pdf.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orders.pdf"'
    return response









