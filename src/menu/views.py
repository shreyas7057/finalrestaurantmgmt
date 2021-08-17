from django.shortcuts import redirect, render,get_object_or_404
from django.views.generic.base import View
from .models import Food,Cart,OrderContent,Order
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from django.core.paginator import Paginator
from accounts.models import Customer,Comment
from django.core.mail import send_mail


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404

from django.db.models import Count
from io import BytesIO




# Create your views here.



# def menu_filter_by_course(request):
#     foods = Food.objects.all()
    
#     if foods == "Desserts":
#         foods = Food.objects.filter(course="Desserts")

#     elif foods == "":
#         foods = Food.objects.filter(course="Desserts")

#     elif foods == "":
#         foods = Food.objects.filter(course="Desserts")

#     else:
#         foods = Food.objects.all()
    

# def menu(request):
#     cuisine = request.GET.get('cuisine')
#     print(cuisine)
#     if cuisine is not None:
#         if ((cuisine == "Desserts")):
#             foods = Food.objects.filter(status="Enabled",course="Desserts")
#         elif(cuisine == "Starters Dish"):
#             foods = Food.objects.filter(status="Enabled",course="Starters Dish")
#         elif(cuisine == "Main Course"):
#             foods = Food.objects.filter(course="Main Course")
        
#         elif(cuisine == "Cold Drinks"):
#             foods = Food.objects.filter(course="Cold Drinks")
#     else:
#         foods = Food.objects.filter()
        
#     return render(request, 'menu/menu.html', {'foods':foods, 'cuisine':cuisine})

def all_foods_index_page(request):
    current_year = datetime.datetime.now().year
    foods = Food.objects.all()
    comments = Comment.objects.all()

    context = {
        'foods':foods,
        'current_year':current_year,
        'comments':comments
    }
    return render(request,'index.html',context)


def all_foods_menu_page(request):
    foods = Food.objects.all()
    context = {
        'foods':foods
    }
    return render(request,'menu/menu.html',context)


def food_filter_dessert(request):
    foods = Food.objects.filter(course="Desserts")

    paginator = Paginator(foods, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'foods':page_obj
    }

    return render(request,'menu/food_desserts.html',context)


def food_filter_starters(request):
    foods = Food.objects.filter(course="Starters Dish")
    context = {
        'foods':foods
    }
    return render(request,'menu/food_starters.html',context)


def food_filter_main_course(request):
    foods = Food.objects.filter(course="Main Course")
    context = {
        'foods':foods
    }
    return render(request,'menu/food_main_course.html',context)


def food_filter_cold_drinks(request):
    foods = Food.objects.filter(course="Cold Drinks")
    context = {
        'foods':foods
    }
    return render(request,'menu/food_cold_drinks.html',context)


def food_details(request, id):
    if request.user.is_authenticated:
        food = Food.objects.get(id=id)

        # adding comment 
        if request.method == "POST":
            user = request.user
            content = request.POST.get('content')
            comment_user = Comment.objects.create(user=user,content=content)
            comment_user.save()
            return redirect('/')

        return render(request, 'menu/single.html', {'food':food})

    else:
        return redirect('login')



def addTocart(request, foodID, userID):
    if request.user.is_authenticated:
        food = Food.objects.get(id=foodID)
        user = User.objects.get(id=userID)
        cart = Cart.objects.create(food=food, user=user)
        cart.save()
        return redirect('cart')

    else:
        return redirect('login')


def cart(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        items = Cart.objects.filter(user=user)
        total = 0
        for item in items:
            total += item.food.sale_price

        return render(request, 'menu/cart.html', {'items': items, 'total':total})

    else:
        return redirect('login')


def delete_from_cart(request,id):
    item = Cart.objects.get(id=id)
    item.delete()
    return redirect('cart')


def placeOrder(request):
    
    if request.user.is_authenticated:
    
        to_email = []
        customer = Customer.objects.get(customer=request.user)
        print(customer.address)
        items = Cart.objects.filter(user=request.user)
        for item in items:
            food = item.food
            order = Order.objects.create(customer=customer, order_timestamp=timezone.now(), payment_status="Pending", 
            delivery_status="Pending", total_amount=food.sale_price, payment_method="Cash On Delivery", location=customer.address)
            order.save()
            orderContent = OrderContent(food=food, order=order)
            orderContent.save()
            item.delete()
        mail_subject = 'Order Placed successfully'
        to = str(customer.customer.email)
        to_email.append(to)
        from_email = 'shreyas7057@gmail.com'
        message = "Hi "+customer.customer.username+" Your order was placed successfully. Please go to your dashboard to see your order history. Your order id is "+str(order.id)+"."
        send_mail(
            mail_subject,
            message,
            from_email,
            to_email,
        )
        return redirect('success_order')

    else:
        return redirect('login')


def success_order(request):
    return render(request,'menu/success_order.html')


def invoice_order(request,id):

    # orders = get_object_or_404(OrderContent, pk=id)
    orders = OrderContent.objects.filter(pk=id)

    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(customer=user)
    # orders = Order.objects.filter(customer=customer).order_by('-id')
    
    pdf = render_to_pdf('menu/invoice.html', {'orders': orders,'customer':customer,'user':user})

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=invoice %s.pdf" % id
        response['Content-Disposition'] = content

        return response
    
    return HttpResponse("Not found")


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# not working
# def recent_order(request):
#     user = User.objects.get(id=request.user.id)
#     customer = Customer.objects.get(customer=user)
#     orders = Order.objects.filter(customer=customer).order_by('-id')[1:]
#     return render(request, 'menu/single.html', {'orders': orders,'user':user})


def my_orders(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(customer=user)
    orders = Order.objects.filter(customer=customer).order_by('-id')
    return render(request, 'menu/orders.html', {'orders': orders,'user':user})


def menu_order_course(request):
    queryset = OrderContent.objects.filter().values('course').annotate(course_count=Count('course'))
    data = list(queryset.values_list('course_count', flat=True))
    labels = list(queryset.values_list('course', flat=True))
    return render(request, "auth/user_profile.html", {
    'labels': labels,
    'data': data,
    })




