from django.shortcuts import render,get_object_or_404,redirect
from .forms import AddScreenForm
from django.urls import reverse
from .models import Theater,Screen
from Movies.models import Show
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import theater_admin_required,is_theater_admin

@login_required
@theater_admin_required
def theater_dashboard(request, pk):
    theater = get_object_or_404(Theater, pk=pk)
    screens = Screen.objects.filter(theater=theater)
    shows = Show.objects.filter(theater=theater)
    return render(request, 'Theaters/theater_dashboard.html', {'theater': theater, 'screens': screens, 'shows':shows})


@login_required
def screen_add(request):
    theater = get_object_or_404(Theater, admin=request.user)
    if request.method == 'POST':
        screen_form = AddScreenForm(request.POST)
        
        if screen_form.is_valid():
            screen = screen_form.save(commit=False)
            screen.theater = theater
            screen.save()
            return redirect(reverse('theater-dashboard', kwargs={'pk': theater.id}))
    else:
        screen_form = AddScreenForm()
    
    return render(request, 'Theaters/screen_add.html', {'screen_form': screen_form, 'theater': theater})


@login_required
@is_theater_admin
def screen_edit(request, screen_id):
    screen = get_object_or_404(Screen, id=screen_id)

    if request.method == 'POST':
        screen_form = AddScreenForm(request.POST, instance=screen)
        if screen_form.is_valid():
            #Save the updated screen details
            screen_form.save()
            return redirect('theater-dashboard', pk=screen.theater.pk)  #Redirect to theater detail page
    else:
        screen_form = AddScreenForm(instance=screen)

    return render(request, 'Theaters/screen_edit.html', {'screen_form': screen_form, 'screen': screen})


@login_required
@is_theater_admin
def screen_delete(request, screen_id):
    screen = get_object_or_404(Screen, id=screen_id)

    if request.method == 'POST':
        #If it's a POST request, delete the screen
        screen.delete()
        messages.success(request, "The screen has been deleted successfully.")
        return redirect('theater-dashboard', pk=screen.theater.pk)  #Redirect back to the theater details page
    
    return render(request, 'Theaters/screen_confirm_delete.html', {'screen': screen})