import sys
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User
from ..models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from sdotify import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from ..tokens import generate_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

@csrf_exempt
def enter_email(request):
    if request.method == "POST":
        email = request.POST['email']
        
        try:
            # Validate the email
            validate_email(email)
        except ValidationError:
            # Invalid email format
            messages.error(request, "This email is invalid. Make sure it's written like example@email.com")
            return render(request, 'authentication/signup1.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered! Please use a different email.")
            return render(request, 'authentication/signup1.html')
        else:
            # Email is not registered, proceed to the next step
            request.session['email'] = email  # Store the email in the session
            return redirect('register_user')
    
    return render(request, 'authentication/signup1.html')

@csrf_exempt
def register_user(request):
    if 'email' not in request.session:
        # If email is not in the session, redirect to step 1
        return redirect('enter_email')

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        phone = request.POST['phone_number']
        dob = request.POST['dob']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try a different username.")
        elif len(username) > 20:
            messages.error(request, "Username must be under 20 characters.")
        elif pass1 != pass2:
            messages.error(request, "Passwords didn't match.")
        else:
            email = request.session['email']
            myuser = User.objects.create_user(username=username, email=email, password=pass1, phone_number=phone, dob=dob)
            myuser.is_active = False
            myuser.save()
            del request.session['email']  # Remove email from session
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to SĐỗtify!!"
        message = "Hello " + "!! \n" + "Welcome to SĐỗtify!! \nThank you for visiting our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanks You"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email SĐỗtify"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('signin')
        
        
    return render(request, "authentication/signup2.html")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password. Please try again.")
            return redirect('signin')
    
    return render(request, "authentication/signin.html")



def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

@login_required
def information(request):
    data = User.objects.get(username = request.user.username)
    return render(request, 'home/infor.html', {'data': data})

