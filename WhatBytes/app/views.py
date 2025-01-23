from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')

def loginPage(request):
    if request.method=='POST':
        email=request.POST.get('emailID')
        password=request.POST.get('password')
        user=authenticate(request,username=email,password=password)
        if user:
            login(request, user)
            return redirect('DashboardPage')
        else:
            messages.error(request, 'Wrong Credentials!')
            return render(request, 'login.html')
    return render (request,'login.html')

def signupPage(request):
    if request.method == 'POST':
        email = request.POST.get('emailID')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        if password != repassword:
            messages.error(request, 'Confirm your password again')
            return render(request, 'signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'signup.html')

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            return redirect('LoginPage')
        except Exception as e:
            messages.error(request, 'Please enter your credentials again')
            return render(request, 'signup.html')
    return render(request, 'signup.html')

def forgotPwdPage(request):
    if request.method == 'POST':
        email = request.POST.get('emailID')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return redirect('LoginPage')
        except User.DoesNotExist:
            messages.error(request, "Email does not exist")
            return render(request, 'forgotpwd.html')
    return render(request, 'forgotpwd.html')

def changePwdPage(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user
        user.set_password(password)
        user.save()
        return redirect('ProfilePage')
    return render(request, 'changepwd.html')

def dashboardPage(request):
    return render(request, 'dashboard.html')

def profilePage(request):
    username = request.user.username
    return render(request, 'profile.html', {'username':username})

def logoutPage(request):
    logout(request)
    return redirect('Home')
