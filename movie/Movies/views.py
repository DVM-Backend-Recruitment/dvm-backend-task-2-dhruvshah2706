# views.py
from django.shortcuts import render,  redirect,  get_object_or_404
from django.utils import timezone
from .models import Show,  Theater,  Movie
from .forms import ScheduleShowForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import is_theater_admin

@login_required
def schedule_show(request):
    # Get the theater linked to the logged-in user
    theater = get_object_or_404(Theater,  admin=request.user)
    
    if request.method == 'POST':
        form = ScheduleShowForm(request.POST,  theater=theater)
        if form.is_valid():
            show = form.save(commit=False)
            movie = show.movie
            show.theater = theater
            show.end_time = show.start_time + timezone.timedelta(minutes=movie.duration)  # Calculate end time
            show.save()
            return redirect('theater-dashboard',  pk=theater.id)
    else:
        form = ScheduleShowForm(theater=theater)

    return render(request,  'Movies/schedule_show.html',  {'form': form,  'theater': theater})


@login_required
@is_theater_admin
def show_edit(request,  show_id):
    show = get_object_or_404(Show,  id=show_id)

    if request.method == 'POST':
        show_form = ScheduleShowForm(request.POST,  instance=show)
        if show_form.is_valid():
            # Save the updated show details
            show = show_form.save(commit=False)
            movie = show.movie
            show.end_time = show.start_time + timezone.timedelta(minutes=movie.duration)  # Calculate end time
            show.save()
            return redirect('theater-dashboard',  pk=show.theater.pk)  # Redirect to theater detail page
    else:
        show_form = ScheduleShowForm(instance=show)

    return render(request,  'Movies/show_edit.html',  {'show_form': show_form,  'show': show})


@login_required
@is_theater_admin
def show_delete(request,  show_id):
    show = get_object_or_404(Show,  id=show_id)

    if request.method == 'POST':
        # If it's a POST request,  delete the screen
        show.delete()
        messages.success(request,  "The screen has been deleted successfully.")
        return redirect('theater-dashboard',  pk=show.theater.pk)  # Redirect back to the theater details page
    
    return render(request,  'Movies/show_confirm_delete.html',  {'show': show})
