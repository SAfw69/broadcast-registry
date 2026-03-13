from django.contrib import admin
from django.urls import path, include
from teams import views as team_views

admin.site.site_header = "Broadcast Company Admin"
admin.site.site_title = "Broadcast Admin Portal"
admin.site.index_title = "Engineering Team Registry"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', team_views.home, name='home'),
    path('teams/', include('teams.urls')),
    path('users/', include('users.urls')),
]
