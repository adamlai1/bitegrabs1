from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('groups/', include('groups.urls')),  # Include the groups URLs here
    path('', views.home, name='home'),
]
