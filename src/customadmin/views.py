from django.db import models
from django.shortcuts import redirect, render,get_object_or_404

# Create your views here.
from accounts.models import Customer,Staff
from menu.models import Food

import csv
from django.http import HttpResponse

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Count

from django.views.generic import CreateView,UpdateView

from django.contrib import messages
from django.contrib.auth import authenticate,logout

from menu.models import Food,Order,OrderContent
from accounts.models import Customer


def admin_index(request):
    if request.user.is_staff:
        all_customers = Customer.objects.all().count()
        all_foods = Food.objects.all().count()
        all_orders = Order.objects.all().count()
        context = {
            'all_customers':all_customers,
            'all_foods':all_foods,
            'all_orders':all_orders,
        }
        return render(request,'customadmin/index.html',context)
    else:
        return redirect('login')


def all_customers(request):
    customers = Customer.objects.all()
    context = {
        'customers':customers
    }
    return render(request,'customadmin/all_customers.html',context)


def all_customers_export_as_csv(request):
    customer = Customer.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="All Customers.csv"'

    # adding values or fields
    writer = csv.writer(response)
    writer.writerow(['Username','Email','Address','Contact','Area','Is Active'])
    for i in customer:
        writer.writerow([i.customer.username,i.customer.email,i.address,i.contact,i.area,i.customer.is_active])

    return response


def all_customers_export_as_pdf(request,*args,**kwargs):
    customers = Customer.objects.all()
    template_path = 'customadmin/all_customer_pdf.html'
    context = {'customers': customers}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # if you want to directly download pdf then use this
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # if you want to display or view the html page in form of pdf
    response['Content-Disposition'] = 'attachment; filename="All Customer.pdf"'
    
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def customers_area_graph(request):
    customers = Customer.objects.values('area').annotate(dcount=Count('area'))
    
    context = {
        'customers':customers
    }
    return render(request,'customadmin/customers_area_graph.html',context)


# def add_food_menu(request):
#     return render(request,'customadmin/add_food.html')

class FoodCreateView(CreateView):
    model=Food
    success_message="Food Menu Added!"
    fields="__all__"
    template_name = 'customadmin/add_food.html'


def all_menu_display_admin(request):
    all_foods = Food.objects.all()
    context = {
        'all_foods':all_foods
    }
    return render(request,'customadmin/all_foods_admin.html',context)

def single_menu_admin(request,id):
    food = Food.objects.get(id=id)
    context = {
        'food':food
    }
    return render(request,'customadmin/single_food_admin.html',context)

class edit_single_menu_admin(UpdateView):
    model = Food
    fields = '__all__'
    template_name = 'customadmin/edit_single_menu_admin.html'


def logout_admin(request):
    logout(request)
    messages.success(request,'User successfully logged out.')
    return redirect('login')


def all_orders_admin(request):
    # order = Order.objects.all()
    # order_content = OrderContent.objects.filter(order=order)
    
    # context = {
    #     'order_content':order_content,
    #     'order':order
    # }
    return render(request,'customadmin/all_orders_admin.html')


# this will graphically show how many menus are present in particular course
def course_menu_count(request):
    courses = Food.objects.values('course').annotate(dcount=Count('course'))
    context = {
        'courses':courses
    }
    return render(request,'customadmin/course_menu_count.html',context)


def all_menu_export_as_csv(request):
    food = Food.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="All Menu.csv"'

    # adding values or fields
    writer = csv.writer(response)
    writer.writerow(['Username','Email','Address','Contact','Area','Is Active'])
    for i in food:
        writer.writerow([i.food.username,i.food.email,i.address,i.contact,i.area,i.customer.is_active])

    return response