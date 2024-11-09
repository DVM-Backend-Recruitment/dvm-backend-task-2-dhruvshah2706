from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, ProfileForm, CustomAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .decorators import role_required
from django.contrib.auth.decorators import login_required
from Theaters.forms import TheaterForm
from Theaters.models import Theater
from django.contrib import messages

@role_required('admin')
def theater_admin_dashboard(request):
    #Logic for theater admin dashboard
    pass

@role_required('superadmin')
def super_admin_dashboard(request):
    #Logic for super admin dashboard
    pass

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        theater_form = TheaterForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.bypass_profile_creation = True
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            #Check if the user is a Theater Admin
            if profile.role in ['theateradmin']:
                if theater_form.is_valid():
                    theater = theater_form.save(commit=False)
                    theater.admin = user
                    theater.save()
                else:
                    #If theater form is invalid, delete the created user and profile
                    user.delete()
                    messages.error(request, "Theater information is invalid.")
                    return redirect('register')

            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
        theater_form = TheaterForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'theater_form': theater_form,
    }
    return render(request, 'users/register.html', context)


def custom_login(request):
    form = CustomAuthenticationForm()  #Instantiate the form for GET requests
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)  #Pass data to form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard_redirect')
            else:
                form.add_error(None, "Invalid username or password.")  #Add error for invalid credentials
    return render(request, 'users/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_redirect(request):
    if request.user.profile.role == 'theateradmin':
       theater = get_object_or_404(Theater,admin=request.user)
       return redirect('theater-dashboard',pk=theater.id)
    return render(request, 'users/dashboard.html')

def accounts_login(request):
    return redirect('login')

