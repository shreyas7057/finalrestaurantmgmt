from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.models import User
from django.views import View
from django.http import JsonResponse, request
import json
from validate_email import validate_email
from .models import Customer, Staff
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

# activation mail imports 
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator

# for login
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse

# for password reset
from django.core.mail import send_mail,BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator




class UsernameValidation(View):
    def post(self,request):
        data = json.loads(request.body) #gets data in valid py dictionary
        # pick username
        username = data['username']

        # check whether username alphanumeric chars
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric char'},status=400)

        # if username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username already taken'},status=409)
        
        return JsonResponse({'username_valid':True})


class EmailValidation(View):
    def post(self,request):
        data = json.loads(request.body) #gets data in valid py dictionary
        # pick username
        email = data['email']

        # check whether username alphanumeric chars
        if not validate_email(email):
            return JsonResponse({'email_error':'Email invalid'},status=400)

        # if username is already taken
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'email already taken'},status=409)

        
        return JsonResponse({'email_valid':True})


class PasswordValidate(View):

    def post(self):
        data = json.loads(request.body)
        password = data['password']

        if len(password)<8:
            return JsonResponse({'password_error':'password to short'},status=409)

        return JsonResponse({'password_error':True})


def signup(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        area = request.POST.get('area')

        # if len(password)<8:
        #     messages.error(request,'password must contain min 8 char ')
        
        user = User.objects.create_user(username,email,password)
        user.set_password(password)

        user.is_active = False
        user.save()

        customer_data = Customer(customer=user)
        customer_data.save()

        customerProfile = Customer(customer=user,address=address,contact=contact,area=area)
        customerProfile.save()

        # sending activation mail
        email_subject = 'Activate your account'

        # path to verify user

        # encode user id
        # force_bytes will give encoded id
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # get token which user will verify
        token = token_generator.make_token(user)

        # get domain which are using we
        # this will give like www.yourwebsitename.com
        domain = get_current_site(request).domain

        link = reverse('activate',kwargs={'uidb64':uidb64,'token':token})

        # relative url to verification
        activate_url = 'http://'+domain+link

        email_body = 'Hi '+user.username+' Please use this link to verify your account '+activate_url
        email = EmailMessage(
            email_subject,
            email_body,
            'noreply@example.com',
            [email],

        )
        email.send(fail_silently=False)


        messages.success(request,'Account Created. Activation link send on your mail id.')

        return redirect('signup')

    else:
        return render(request, 'auth/signup.html')


# this view will help user to verify that user is using one time this link and after verfiying turing is_active as True so successfully verified.
class VerificationView(View):

    def get(self,request,uidb64,token):

        # getting encoded userid

        # force_text converts into humanreadble format
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user,token):
                return redirect('login'+'?message='+'User is already activated')

            # checking whether token is used one time or more than one time
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request,'Account activated successfully.')
            return redirect('login')
        except Exception as ex:
            pass

        return redirect('login')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request,'User logged in successfully')
                return redirect('/')            

            else:
                messages.error(request,'Account is not active.')
                return redirect('login')
        else:
            messages.error(request,'Invalid credentials')
            return redirect("login")  
    else:
        return render(request, 'auth/login.html')

def logout_user(request):
    logout(request)
    messages.success(request,'User successfully logged out.')
    return redirect('login')


# staff user 

def signup_staff(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.create_user(username,email,password)
        user.set_password(password)
        user.is_active = False
        user.save()
        messages.success(request,'Send for approval wait for message.')
        return redirect('signup_staff')
    
    return render(request,'customadmin/staff_register.html')



def register_staff_admin(request):
    if request.method == "POST":
        pass

    return render(request,'customadmin/register_staff_admin.html')


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('/')

    else:
        profile = Customer.objects.get(customer=request.user)
        context = {
            'profile':profile
        }
        return render(request,'auth/user_profile.html',context)

# not in use we are not using this func
def password_reset_request(request):
    if request.method == "POST":
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Password Reset Request'
                    email_template_name = 'auth/password_message.txt'
                    parameters = {
                        'email':user.email,
                        'domain':'localhost:8000',
         
                    }
                    email = render_to_string(email_template_name,parameters)
                    try:
                        send_mail(subject,email,'',[user.email],fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid Header')

                    return redirect('')
    else:
        password_form = PasswordResetForm()
    context = {
        'password_form':password_form
    }
    return render(request,'auth/password_reset.html',context)

# def update_address(request,id):
#     customer = Customer.objects.get(id=request.user)
#     if request.method == "POST":
#         address = request.POST.get('address')

#     return render(request,'auth/update_address.html')