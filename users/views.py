from django.shortcuts import render, redirect, HttpResponse
from .forms import UserRegistrationForm, ProfileForm, CustomAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .decorators import role_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@role_required('admin')
def theater_admin_dashboard(request):
    # Logic for theater admin dashboard
    pass

@role_required('superadmin')
def super_admin_dashboard(request):
    # Logic for super admin dashboard
    pass

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')  # Redirect to a dashboard or home page
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})


def custom_login(request):
    form = CustomAuthenticationForm()  # Instantiate the form for GET requests
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)  # Pass data to form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashoard_redirect')
            else:
                form.add_error(None, "Invalid username or password.")  # Add error for invalid credentials
    return render(request, 'users/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_redirect(request):
    # if request.user.profile.role == 'regular':
    #     return HttpResponse('<h1>Regular User</h1>')
    #     # return redirect('regular_user_dashboard')  # Create this view
    # elif request.user.profile.role == 'theateradmin':
    #     return HttpResponse('<h1>Admin User</h1>')
    #     # return redirect('theater_admin_dashboard')  # Create this view
    # elif request.user.profile.role == 'superadmin':
    #     return HttpResponse('<h1>SuperAdmin User</h1>')
    #     # return redirect('super_admin_dashboard')  # Create this view
    # return redirect('login')
    return render(request, 'users/dashboard.html')

@login_required
def google_login_callback(request):
    if request.user.profile.role not in ['theateradmin','superadmin']:
        google_user_data = request.data  # Assume this is the response data from Google
        email = google_user_data.get('email')
        name = google_user_data.get('name')

        # Step 2: Check if the user already exists
        try:
            user = User.objects.get(email=email)
            # User exists, log them in
            login(request, user)
        except User.DoesNotExist:
            # Step 3: Create a new user and profile
            user = User.objects.create_user(
                username=email.split('@')[0],  # Use part of the email as the username
                email=email,
                first_name=name.split()[0],  # First name
                last_name=' '.join(name.split()[1:]),  # Last name (if applicable)
            )
            user.save()
            # Create a profile for the user
            profile = Profile.objects.create(user=user)
            profile.role = 'regular'  # Assign default role or set based on your logic
            profile.save()

            # Log in the new user
            login(request, user)

def accounts_login(request):
    return redirect('login')

