from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/<int:pk>/', views.theater_dashboard, name='theater-dashboard'), 
    path('add_screen/', views.screen_add, name='screen-add'), 
    path('edit_screen/<int:screen_id>/',  views.screen_edit,  name='screen-edit'), 
    path('delete_screen/<int:screen_id>/',  views.screen_delete,  name='screen-delete'), 
]