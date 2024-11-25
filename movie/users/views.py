from django.shortcuts import render,  redirect,  get_object_or_404
from .forms import CustomAuthenticationForm,  UserUpdateForm
from django.contrib.auth import authenticate,  login,  logout
from .decorators import role_required
from django.contrib.auth.decorators import login_required
from Theaters.models import Theater
from Movies.models import Show
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from Bookings.models import Booking
from Food.models import Order
from allauth.socialaccount.providers.google.views import OAuth2LoginView

#  def register(request):
#      if request.method == 'POST':
#          user_form = UserRegistrationForm(request.POST)
#          profile_form = ProfileForm(request.POST)
#          theater_form = TheaterForm(request.POST)

#          if user_form.is_valid() and profile_form.is_valid():
#              user = user_form.save(commit=False)
#              user.bypass_profile_creation = True
#              user.save()
#              profile = profile_form.save(commit=False)
#              profile.user = user
#              profile.save()

#              # Check if the user is a Theater Admin
#              if profile.role in ['theateradmin']:
#                  if theater_form.is_valid():
#                      theater = theater_form.save(commit=False)
#                      theater.admin = user
#                      theater.save()
#                  else:
#                      # If theater form is invalid,  delete the created user and profile
#                      user.delete()
#                      messages.error(request,  "Theater information is invalid.")
#                      return redirect('register')

#              messages.success(request,  "Registration successful. You can now log in.")
#              return redirect('login')
#          else:
#              messages.error(request,  "Please correct the errors below.")
#      else:
#          user_form = UserRegistrationForm()
#          profile_form = ProfileForm()
#          theater_form = TheaterForm()

#      context = {
#          'user_form': user_form, 
#          'profile_form': profile_form, 
#          'theater_form': theater_form, 
#      }
#      return render(request,  'users/register.html',  context)


def custom_login(request):
    form = CustomAuthenticationForm()  # Instantiate the form for GET requests
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)  # Pass data to form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,  password=password)
            if user is not None:
                login(request,  user)
                return redirect('regular-dashboard')
            else:
                form.add_error(None,  "Invalid username or password.")  # Add error for invalid credentials
    return render(request,  'users/login.html',  {'form': form})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
@role_required(['regular', 'theateradmin'])
def regular_dashboard(request):
    if request.user.profile.role == 'theateradmin':
       theater = get_object_or_404(Theater, admin=request.user)
       return redirect('theater-dashboard', pk=theater.id)
    shows = Show.objects.all()
    query = request.GET.get('query',  '')  #  Get the search query,  default to an empty string
    shows = Show.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    is_empty = False
    if query:
        shows = shows.filter(
            Q(movie__title__icontains=query) | Q(theater__name__icontains=query) | Q(screen__name__icontains=query))
        print(shows)
        if not shows:
            is_empty = True

    user_bookings = Booking.objects.filter(user=request.user)
    food_orders = {booking.id: Order.objects.filter(booking=booking) for booking in user_bookings}

    context = {
        'shows':shows, 
        'is_empty':is_empty, 
        'user_bookings': user_bookings, 
        'food_orders': food_orders, 
    }
    return render(request,  'users/dashboard.html', context)


def accounts_login(request):
    return redirect('login')


@login_required
@role_required(['regular', 'theateradmin'])
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,  instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request,  f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form, 
    }
    return render(request,  'users/profile.html',  context)
