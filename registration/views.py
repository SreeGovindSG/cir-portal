from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from cirplacements import settings
from django.views.generic.edit import FormView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from braces.views import LoginRequiredMixin, AnonymousRequiredMixin
from registration.models import *
from registration.forms import *
from django.views.generic import ListView
from django.http import Http404
from django.http import HttpResponse
import simplejson as json
import pyexcel.ext.xls   # pip install pyexcel-xls
import pyexcel.ext.xlsx # pip install pyexcel-xlsx
import pyexcel.ext.ods # pip install pyexcel-ods
import django_excel as excel
from django.template import RequestContext
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage
from mail_templated import send_mail
import uuid
from ccavutil import encrypt,decrypt
from string import Template
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import datetime
from django.core.exceptions import PermissionDenied


class CurrentUserMixin(object):
    model = User

    def get_object(self, *args, **kwargs):
        try: obj = super(CurrentUserMixin, self).get_object(*args, **kwargs)
        except AttributeError: obj = self.request.user
        return obj


# Create your views here
def anonymous_required(func):
    def as_view(request, *args, **kwargs):
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL )
        if request.user.is_authenticated():
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response
    return as_view

class UserRegistrationView(AnonymousRequiredMixin, FormView):
    template_name = "register/user/register_user.html"
    authenticated_redirect_url = reverse_lazy(u"home")
    form_class = UserRegistrationForm
    success_url = '/register/user/success/'

    def form_valid(self, form):
        form.save()
        return FormView.form_valid(self, form)

class StudentRegistrationView( LoginRequiredMixin, FormView):
    template_name = "register/cirstaff/register_student.html"
    form_class = StudentRegistrationForm
    success_url = '/register/cirstaff/success'

    def form_valid(self, form):
        form.instance.aums_id = form.instance.aums_id.lower()
        form.save()
        return FormView.form_valid(self, form)

class StudentBulkUploadView( LoginRequiredMixin, FormView):
    template_name = "register/cirstaff/register_bulk_student.html"
    form_class = UploadFileForm
    success_url = '/register/student/success/'


def handle_student_upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            studentFields = filehandle.get_array()[1:]
            counter = 0
            for student in studentFields:
                Student.Objects.create_student_fromfile(student[0].lower(),student[1],student[2],student[3],student[4], student[5],
                                                        student[6],student[7],student[8],student[9],student[10],student[11],student[12],student[13],student[14])
                counter = counter+1

            return render_to_response('register/cirstaff/register_bulk_student_list.html',{'counter':counter },
                                       context_instance=RequestContext(request))
        else :
             return redirect(request.META['HTTP_REFERER'])
    else:
         return HttpResponseBadRequest()


class StudentListView(LoginRequiredMixin,ListView):
    template_name = 'register/cirstaff/list.html'

    def get_queryset(self):
        return Student.Objects.all()


class StudentListUpdateView(UpdateView):
    model = Student
    fields = student_fields
    template_name_suffix = '_update_form'
    success_url = '/register/cirstaff/success/'

    def get_object(self, queryset=None):
        obj = Student.Objects.get(aums_id=self.kwargs['aums_id'])
        if obj:
            return obj
        else:
            raise Http404("That doesnt exist.")