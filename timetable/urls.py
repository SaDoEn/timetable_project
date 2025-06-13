from django.urls import path
from django.contrib import admin
from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.home, name='home'),
    path('timetable/', views.TimetableListView.as_view(), name='timetable_list'),
    path('timetable/add/', views.TimetableCreateView.as_view(), name='timetable_add'),
    path('timetable/<int:pk>/edit/', views.TimetableUpdateView.as_view(), name='timetable_edit'),
    path('timetable/<int:pk>/delete/', views.TimetableDeleteView.as_view(), name='timetable_delete'),
    path('logout/', views.custom_logout, name='logout')
]
admin.site.site_header = "Адміністрування розкладу"
admin.site.site_title = "Адмін-панель розкладу"
admin.site.index_title = "Керування розкладом навчального закладу"