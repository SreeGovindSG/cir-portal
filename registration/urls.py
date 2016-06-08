from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from registration import views
from registration.views import *
from registration.models import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='register/register.html')),
    url(r'^user/$', UserRegistrationView.as_view(), name='register_user'),
     url(r'^user/success/', TemplateView.as_view(template_name='register/user/success.html'),
        name='user_registration_success'),
     url(r'^portal/student', TemplateView.as_view(template_name='register/manage_students.html'),name="manage_students"),
     url(r'^portal/staff', TemplateView.as_view(template_name='register/manage_staff.html'),name="manage_staff"),
     url(r'^preferences', TemplateView.as_view(template_name='preferences.html'),name="preferences"),
     url(r'^sign-in', TemplateView.as_view(template_name='sign-in.html'),name="sign-in"),
     url(r'^index', TemplateView.as_view(template_name='index.html'),name="index"),
     url(r'^student/$', StudentRegistrationView.as_view(), name='register_student'),
     url(r'^cirstaff/success/', TemplateView.as_view(template_name='register/cirstaff/success.html'), name='success'),
     url(r'^bulk/$', StudentBulkUploadView.as_view(), name='register_student_bulk'),
     url(r'^bulk/handle/$', views.handle_student_upload, name='upload_students'),
     url(r'^list/$', StudentListView.as_view(), name='list'),
     url(r'^profile/edit/(?P<stud_id>\d+)/$', StudentListUpdateView.as_view(), name='student_profile_update'),
     url(r'^profile/edit/(?P<aums_id>[\w|\W]+)/$', StudentListUpdateView.as_view(), name='student_profile_update'),
    ]