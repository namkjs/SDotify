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


@login_required
def information(request):
    data = User.objects.get(username = request.user.username)
    print(data.dob)
    return render(request, 'home/infor.html', {'data': data})

@login_required
def edit(request):
    if request.method == 'POST':
        # Xử lý dữ liệu form sau khi người dùng lưu thay đổi
        user = request.user
        user.first_name = request.POST.get('phone_number')
        user.email = request.POST.get('email')
        user.dob = request.POST.get('dob')
        user.save()
        return redirect('information')  # Chuyển hướng về trang thông tin cá nhân

    return render(request, 'home/edit.html', {'user': request.user})
@csrf_exempt
def reset_password(request):
    if request.method == "POST":
        
        mail = request.POST.get('email')
        myuser = User.objects.get(email=mail)

        email_subject = "Reset your password"
        current_site = get_current_site(request)

        email_subject = "Reset password"
        message2 = render_to_string('reset_pass.html',{
            
            'name': myuser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [mail],
        )
        email.fail_silently = True
        email.send()
    return render(request, 'home/resetpassword.html')
@csrf_exempt

def reset(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        if request.method == "POST":
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            if pass1 == pass2:
                myuser.set_password(pass1)
                myuser.save()
                return redirect('home')
    else:
        return render(request,'activation_failed.html')
    return render(request, 'home/resetpassword2.html')

