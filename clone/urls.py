"""clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from superset.views import adminview, employeeview, studentview, universityview
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    # admin
    path('admindashboard', adminview.admindashboard, name='admindashboard'),
    path('Ustudents', adminview.Ustudents, name="Ustudents"),
    # employee
    path('companydetails', employeeview.companydetails, name='companydetails'),
    path('company_dashboard', employeeview.company_dashboard,name='company_dashboard'),
    path('createjobs', employeeview.createjobs, name='createjobs'),
    path('viewjobs', employeeview.viewjobs, name='viewjobs'),
    path('editjobs/<int:id>', employeeview.editjobs, name='editjobs'),
    path('cancel', employeeview.cancel, name='cancel'),
    path('applicants/<int:id>', employeeview.applicants, name='applicants'),
    path('applicantdetails/<int:id>/<str:mail>',employeeview.applicantdetails, name='applicantdetails'),
    path('company_profile', employeeview.company_profile, name='company_profile'),
    # student
    path('home', studentview.home, name='home'),
    path('dashboard', studentview.dashboard, name='dashboard'),
    path('logoutuser', studentview.logoutuser, name='logoutuser'),
    path('register', studentview.register, name='register'),
    path('studentdetails', studentview.studentdetails, name='studentdetails'),
    path('studentjobs', studentview.studentjobs, name='studentjobs'),
    path('viewprofile/<str:id>', studentview.viewprofile, name='viewprofile'),
    path('withdraw/<str:id>', studentview.withdraw, name='withdraw'),
    path('myjobs', studentview.myjobs, name='myjobs'),
    path('stprofile', studentview.stprofile, name='stprofile'),
    # university
    path('college_dashboard', universityview.college_dashboard, name='college_dashboard'),
    path('college_profile', universityview.college_profile, name='college_profile'),
    path('addstudent', universityview.addstudent,name='addstudent'),
    path('universitydetails',universityview.universitydetails,name='universitydetails'),
    path('unregisteredst',universityview.unregisteredst,name="unregisteredst"),
    path('sendmail',universityview.sendmail,name='sendmail'),
    path('registeredst',universityview.registeredst,name='registeredst'),
    path('unapprovedst',universityview.unapprovedst,name='unapprovedst'),
    path('approve/<str:email>',universityview.approve,name='approve'),
    path('approvedst',universityview.approvedst,name='approvedst'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)