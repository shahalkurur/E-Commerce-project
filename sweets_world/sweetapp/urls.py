from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('user_login', views.user_login, name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('signup_verification/', views.signup_verification, name="signup_verification"),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('logout_user/',views.logout_user,name='logout_user'),

    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),

     


    path('admin_dsh/',views.admin_dsh,name='admin_dsh'),
    path('sign_out/',views.signout_adm,name='sign_out'),
    path('manage_user/',views.manage_user,name='manage_user'),
    path('block_user/<int:id>/',views.block_user,name='block_user'),
    path('unblock_user/<int:id>/',views.unblock_user,name='unblock_user'),


    path('manage_category/',views.manage_category,name='manage_category'),
    path('manage_products/',views.manage_products,name='manage_products'),
    path('manage_orders/',views.manage_orders,name='manage_orders'),
    path('manage_coupens/',views.manage_coupens,name='manage_coupens'),
    path('manage_offer/',views.manage_offer,name='manage_offer'),
    path('sale_graph/',views.sale_graph,name='sale_graph'),

     path('generate-pdf/',views.generate_pdf,name='generate-pdf'),
    path('generatepdf/<int:id>/',views.generatepdf,name='generatepdf'),

    path('add_coupen/',views.add_coupen,name='add_coupen'),
    path('activate_coupen/<int:id>/',views.activate_coupen,name='activate_coupen'),

    path('status_update/<int:pk>/',views.status_update,name='status_update'),

    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/<int:id>/',views.edit_category,name='edit_category'),
    path('delete_category/<int:id>/',views.delete_category,name='delete_category'),

    path('add_category_offer/',views.add_category_offer,name='add_category_offer'),
    path('delete_category_offer/<int:offer_id>/',views.delete_category_offer,name='delete_category_offer'),
    





    path('add_products/',views.add_products,name='add_products'),
    path('edit_products/<int:id>/',views.edit_products,name='edit_products'),
    path('update_product/<int:id>',views.update_product,name='update_product'),
    path('delete_products/<int:id>',views.delete_products,name='delete_products'),

    path('sales_report/', views.daily_sales_report, name='sales_report'),
    path('monthly_sales/', views.monthly_sales, name='monthly_sales'),
    path('year_sales/', views.year_sales, name='year_sales'),
    path('period_of_sale/', views.period_of_sale, name='period_of_sale'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),




    path('cat_by_prod/<int:id>',views.cat_by_prod,name='cat_by_prod'),
    path('cat_by_prod/',views.cat_by_prod,name='cat_by_prod'),


    path('product_detail/<int:id>/', views.product_detail, name='product_detail')
    


]


# to fetch images from database
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)