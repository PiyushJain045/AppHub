from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages # for sending success or failure messages
from gfg import settings

#for sending email
from django.core.mail import send_mail, EmailMessage #email.send() more power
from django.contrib.sites.shortcuts import get_current_site #for sending conformation link
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token


from django.contrib.auth.models import User #during GET and to store user data in db
from django.contrib.auth import authenticate, login, logout #during POST 'signin'
from .models import UserNumber
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, "start/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        number = request.POST['number']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered")
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be alpha-Numeric!")
            return redirect('home')
        
        if len(number) != 10:
            messages.error(request, "Phone number should be 10 digit!")
            return redirect('home')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.is_active = False
        myuser.save()


        # ADD phone number
        user_number = UserNumber(user=myuser, phone_number=number)
        user_number.save()

        #Welcome Email
        messages.success(request, "Your account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.")
        
        subject = "Welcome to gfg - Django Login!!"
        message = "Hello" + myuser.first_name + "!! \n" + "Welcome to GFG!! \n Thank You for visiting our website \n We have alos sent you a conformation email please confirm your email address in order to activate your email account. \n\n Thanking you\n Piyush Jain" 
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list) #for simple text

        # Email address conformation Email 

        print("1")
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ gfg - Django Login!!"
        message2 = render_to_string('email_conformation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        print("2")

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email]
        )
        email.fail_silently = True
        email.send()
        return redirect('home')


def signin(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            print("Logged in")
            fname = request.user.username
            return render(request, "landing_page/index.html", {'fname': fname})
        else:
            print("Not logged in")

    if request.method == "POST":
        print("inside")
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username= username, password=pass1)
        print("User:", user)

        if user is not None:
            login(request, user)
            fname = user.username
            return redirect('signin')
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')

def activate(request, uidb64,token):
    try:
        print("success")
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        print("fail")
        myuser = None 

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your account has been successfully verified")
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')
    

def about(request):
    return render(request, "landing_page/about.html")