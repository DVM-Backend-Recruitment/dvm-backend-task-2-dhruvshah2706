from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.schedule_show, name='show-schedule'), 
    path('edit/<int:show_id>', views.show_edit,  name='show-edit'), 
    path('delete/<int:show_id>/',  views.show_delete,  name='show-delete'), 
]
