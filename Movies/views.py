#views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Show, Theater, Movie
from .forms import ShowForm

def schedule_show(request):
    #Get the theater linked to the logged-in user
    theater = get_object_or_404(Theater, admin=request.user)
    
    if request.method == 'POST':
        form = ShowForm(request.POST, theater=theater)
        if form.is_valid():
            show = form.save(commit=False)
            movie = show.movie
            show.theater = theater
            show.end_time = show.start_time + timezone.timedelta(minutes=movie.duration)  #Calculate end time
            show.save()
            return redirect('theater-detail', pk=theater.id)
    else:
        form = ShowForm(theater=theater)

    return render(request, 'Movies/schedule_show.html', {'form': form, 'theater': theater})
