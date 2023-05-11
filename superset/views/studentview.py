from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from ..models import Uvstudents, University, student, Jobs, University_jobs, Applicants
from ..forms import studentform, Edit_stform


def home(request):
    if request.method == 'GET':
        return render(request, 'superset/login.html')
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'superset/login.html', {'error': 'User not found. Please enter correct username and password'})
        else:
            login(request, user)
            if user.groups.filter(name='Student').exists():
                return redirect('studentdetails')
            if user.groups.filter(name='University').exists():
                return redirect('universitydetails')
            if user.groups.filter(name='Company').exists():
                return redirect('companydetails')
            if request.user.is_superuser:
                return redirect("admindashboard")


def register(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        if User.objects.filter(username=uname).exists():
            return render(request, 'superset/login.html', {'error': 'User Already Exists. Please Login'})
        elif student.objects.filter(Email_ID=uname) and University.objects.filter(Passphrase=pwd):
            user = User.objects.create_user(
                username=uname, password=pwd, email=uname)
            group = Group.objects.get(name='Student')
            user.groups.add(group)
            user.save()
            login(request, user)
            return redirect('studentdetails')
        else:
            return render(request, 'superset/login.html', {'error': 'Wrong Credentials'})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())
def studentdetails(request):
    if request.method == "GET":
        x = student.objects.filter(Email_ID=request.user).get()
        if x.registration_status == "R":
            return redirect("dashboard")
        else:
            mycontext = {
                "Name": x.Full_Name,
                "email": x.Email_ID,
                "college": x.College,
                "college_roll_no": x.College_Roll_No,
            }
            return render(request, 'superset/students/studentform.html', mycontext)
    if request.method == "POST":
        x = student.objects.filter(Email_ID=request.user).get()
        k = request.POST.dict()
        z = request.FILES.dict()
        print(z)
        first_key = next(iter(k))
        k.pop(first_key)
        for i, y in k.items():
            setattr(x, i, y)
        for i, y in z.items():
            setattr(x, i, y)
        x.registration_status = "R"
        x.save()
        return redirect("dashboard")


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())
def dashboard(request):
    x = student.objects.get(Email_ID=request.user.email)
    return render(request, 'superset/students/student_dashboard.html', {"count": 0, "x": x})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())
def studentjobs(request):
    r = []
    y = student.objects.get(Email_ID=request.user.email)
    z = University_jobs.objects.filter(universitiy=y.College)
    for i in z:
        r.append(i.job_id)
    # return HttpResponse("jobs")
    return render(request, 'superset/students/student_dashboard.html', {"count": 1, "x": r})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())
def viewprofile(request, id):
    if request.method == "GET":
        x = Jobs.objects.get(job_id=id)
        m = Applicants.objects.filter(job_id=x).filter(
            email=request.user.email).exists()
        if m:
            l = Applicants.objects.filter(job_id=x).filter(
                email=request.user.email)
            l = l.get()
            return render(request, 'superset/students/student_dashboard.html', {"count": 2, "m_count": 1, "x": x, "l": l, "msg": "You have already applied for this job profile"})
        else:
            y = student.objects.filter(Email_ID=request.user.email).filter(
                Xth_Percentage__gte=x.Xth_perecentage).filter(
                XIIth_Percentage__gte=x.XIIth_percentage).filter(
                College_CGPA__gte=x.College_CGPA)
            if y.exists():
                y = y.get()
                k = str(y.Resume)
                k = k.split("/")
                k = k[1]
                return render(request, 'superset/students/student_dashboard.html', {"count": 2, "m_count": 0, "x": x, "y": y, "k": k})
            else:
                return render(request, 'superset/students/student_dashboard.html', {"count": 2, "m_count": 2, "x": x, "msg": "You Are Not Eligible for this Job Profile"})
    else:
        x = Jobs.objects.get(job_id=id)
        k = student.objects.get(Email_ID=request.user.email)
        y = Applicants(job_id=x, email=k.Email_ID, Resume=k.Resume)
        y.save()
        return redirect("studentjobs")


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())
def withdraw(request, id):
    if request.method == "POST":
        x = Jobs.objects.get(job_id=id)
        m = Applicants.objects.filter(job_id=x).filter(
            email=request.user.email)
        m.delete()
        return redirect("studentjobs")


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())
def myjobs(request):
    r = []
    y = student.objects.get(Email_ID=request.user.email)
    x = Applicants.objects.filter(email=y.Email_ID)
    for i in x:
        r.append(i.job_id)
    return render(request, 'superset/students/student_dashboard.html', {"count": 3, "x": r, })


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())
def stprofile(request):
    if request.method == "GET":
        x = student.objects.get(Email_ID=request.user.email)
        y = Edit_stform(instance=x)

        return render(request, 'superset/students/student_dashboard.html', {"count": 4, "y": y, })
    else:
        x = student.objects.get(Email_ID=request.user.email)
        y = Edit_stform(request.POST, instance=x)
        if y.is_valid():
            x.approval_status = "UA"
            x.save()
            y.save()
            return redirect("dashboard")


def logoutuser(request):
    logout(request)
    return redirect('home')
