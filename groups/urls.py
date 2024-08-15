from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_group, name='create_group'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('invite/<uuid:token>/', views.join_group, name='join_group'),  # This is where the error occurs
    path('guest-name/<uuid:token>/', views.enter_guest_name, name='enter_guest_name'),  # This fixes the error
    path('<int:group_id>/invite/', views.invite_member, name='invite_member'),
    path('<int:group_id>/preferences/', views.submit_preferences, name='submit_preferences'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/kick/<int:user_id>/', views.kick_member, name='kick_member'),
]