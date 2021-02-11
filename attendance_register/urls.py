from django.contrib import admin
from django.urls import path, include
from adminpage import views as admview
from employees import views as empview

urlpatterns = [
    path('admin/', admin.site.urls),

    # employee
    path('', empview.index, name='index'),
    path('employee/signup', empview.signup, name='signup'),
    path('employee/details', empview.details, name='details'),
    path('employee/homepage', empview.homepage, name='homepage'),
    path('employee/end_work', empview.end_work, name='end_work'),
    path('employee/logout', empview.logoutuser, name = 'logout'),

    # admin
    path('admin_panel/homepage', admview.homepage, name='admin_homepage'),
    path('admin_panel/logout', empview.logoutuser, name = 'logout'),


]
