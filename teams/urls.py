from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('search/', views.search, name='search'),
    path('org-chart/', views.org_chart, name='org_chart'),
    path('audit-log/', views.audit_log, name='audit_log'),

    # Teams
    path('create/', views.team_create, name='team_create'),
    path('<int:pk>/', views.team_detail, name='team_detail'),
    path('<int:pk>/edit/', views.team_edit, name='team_edit'),
    path('<int:pk>/delete/', views.team_delete, name='team_delete'),
    path('<int:team_pk>/add-member/', views.add_member, name='add_member'),
    path('<int:team_pk>/remove-member/<int:member_pk>/', views.remove_member, name='remove_member'),
    path('<int:team_pk>/add-repo/', views.add_repository, name='add_repository'),

    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('departments/<int:pk>/edit/', views.department_edit, name='department_edit'),
]
