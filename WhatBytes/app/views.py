from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.
def home(request):
    return render(request, 'home.html')

def loginPage(request):
    if request.method=='POST':
        email = request.POST.get('emailID')
        password = request.POST.get('password')
        user = authenticate(request,username=email,password=password)
        if user:
            login(request, user)
            return redirect('DashboardPage')
        else:
            messages.error(request, 'Invalid email or password!')
            return render(request, 'login.html')
    return render(request,'login.html')

def signupPage(request):
    if request.method=='POST':
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
            validate_password(password)
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            return redirect('LoginPage')
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'signup.html')
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
        except:
            messages.error(request, "Please check your Email ID again")
            return render(request, 'forgotpwd.html')
        
        try:
            validate_password(password)
            user.set_password(password)
            user.save()
            return redirect('LoginPage')
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'forgotpwd.html')
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
            return render(request, 'forgotpwd.html')
    return render(request, 'forgotpwd.html')

def changePwdPage(request):
    if request.method == 'POST':
        password = request.POST.get('password')

        try:
            validate_password(password, user=request.user)
            user = request.user
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('ProfilePage')
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'changepwd.html')
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
            return render(request, 'changepwd.html')
    return render(request, 'changepwd.html')

def dashboardPage(request):
    username = request.user.username
    return render(request, 'dashboard.html', {'username':username})

def profilePage(request):
    username = request.user.username
    email = request.user.email
    date_joined = request.user.date_joined
    return render(request, 'profile.html', {'username': username, 'email': email, 'date_joined': date_joined})

def logoutPage(request):
    logout(request)
    return redirect('Home')
