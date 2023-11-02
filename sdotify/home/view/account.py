from django.contrib.auth.decorators import login_required
from ..models import User
from django.shortcuts import render, redirect

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