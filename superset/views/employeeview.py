from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models import University, company_universities, company, Jobs, University_jobs, Applicants, student
from ..forms import company_form, job_form, Edit_companyform
from django.http import HttpResponse


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def companydetails(request):
    if request.method == "GET":
        if company.objects.filter(Email_ID=request.user.email):
            return redirect("company_dashboard")
        else:
            y = University.objects.all()
            x = []
            for i in y:
                x.append(i.College)
            data = {"Email_ID": request.user.email}
            form = company_form(initial=data)
            form.fields['Email_ID'].widget.attrs['readonly'] = True
            return render(request, 'superset/companyform.html', {"form": form, "x": x})
    else:
        universitiys = request.POST.getlist('choice')
        form = company_form(request.POST)
        c_name = form['Company_Name'].value()
        if form.is_valid():
            form.save()
        p_object = company.objects.get(Company_Name=c_name)
        u_objects = []
        for u in universitiys:
            y = company_universities(company_name=p_object, universities=u)
            u_objects.append(y)
        company_universities.objects.bulk_create(u_objects)
        return redirect("company_dashboard")


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def company_dashboard(request):
    y = company.objects.get(Email_ID=request.user.email)
    return render(request, 'superset/company_dashboard.html', {"count": 0, "y": y})


def jobid():
    x = Jobs.objects.all().count()
    return x+1


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def createjobs(request):
    if request.method == "GET":
        name = company.objects.get(Email_ID=request.user.email)
        data = {"Company_Name": name}
        form = job_form(initial=data)
        form.fields['Company_Name'].widget.attrs['readonly'] = True
        data = company.objects.get(
            Company_Name=name).comuv.filter(company_name=name)
        return render(request, 'superset/company_dashboard.html', {"count": 1, "form": form, "x": data})
    else:
        y = jobid()
        x = Jobs()
        x.job_id = y
        uy = request.POST.getlist('college')
        u_object = []
        form = job_form(request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                setattr(x, key, value)
            x.save()
        for u in uy:
            k = University_jobs(
                job_id=Jobs.objects.get(job_id=y), universitiy=u)
            u_object.append(k)
        University_jobs.objects.bulk_create(u_object)
        return redirect("viewjobs")


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def viewjobs(request):
    y = company.objects.get(Email_ID=request.user.email)
    x = Jobs.objects.filter(Company_Name=y.Company_Name)
    if (x):
        return render(request, 'superset/company_dashboard.html', {"count": 2, 'x': x, 'msg': 'Your Job Profiles'})
    else:
        return render(request, 'superset/company_dashboard.html', {"count": 2, 'msg': "You don't have any job profiles"})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def editjobs(request, id):
    if request.method == "GET":
        c_name = company.objects.get(Email_ID=request.user.email)
        x = Jobs.objects.get(job_id=id)
        if (x.Company_Name != c_name.Company_Name):
            return redirect("viewjobs")
        form = job_form(instance=x)
        form.fields['Company_Name'].widget.attrs['readonly'] = True
        form.fields['Xth_perecentage'].widget.attrs['readonly'] = True
        form.fields['XIIth_percentage'].widget.attrs['readonly'] = True
        form.fields['College_CGPA'].widget.attrs['readonly'] = True
        return render(request, 'superset/company_dashboard.html', {"count": 3, "form": form})
    else:
        x = Jobs.objects.get(job_id=id)
        form = job_form(request.POST or None, instance=x)
        if form.is_valid():
            form.save()
            return redirect('viewjobs')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def cancel(request):
    return redirect('viewjobs')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def applicants(request, id):
    c_name = company.objects.get(Email_ID=request.user.email)
    j = Jobs.objects.get(job_id=id)
    if (j.Company_Name != c_name.Company_Name):
        return redirect("viewjobs")
    k = Jobs.objects.get(job_id=id).applicants.filter(Application_status='P')
    l = Jobs.objects.get(job_id=id).applicants.filter(Application_status='A')
    p_app = []
    for i in k:
        p_app.append(i.email)
    x = student.objects.filter(Email_ID__in=p_app)
    a_app = []
    for i in l:
        a_app.append(i.email)
    y = student.objects.filter(Email_ID__in=a_app)
    if (x and y):
        return render(request, 'superset/company_dashboard.html', {"count": 4, "id": id, "x": x, "y": y, 'msg1': "Pending Applicants", 'msg2': "Selected Applicants"})
    elif (x):
        return render(request, 'superset/company_dashboard.html', {"count": 4, "id": id, "x": x, 'msg1': "Pending Applicants", })
    elif (y):
        return render(request, 'superset/company_dashboard.html', {"count": 4, "id": id, "y": y, 'msg2': "Selected Applicants"})
    else:
        return render(request, 'superset/company_dashboard.html', {"count": 4, 'msg1': "No Applicants"})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def applicantdetails(request, id, mail):
    if request.method == "GET":
        c_name = company.objects.get(Email_ID=request.user.email)
        j = Jobs.objects.get(job_id=id)
        k = Applicants.objects.filter(email=mail)
        if (j.Company_Name != c_name.Company_Name):
            return redirect("viewjobs")
        if (not k):
            return redirect("viewjobs")
        x = student.objects.get(Email_ID=mail)
        k = k.get()
        return render(request, 'superset/company_dashboard.html', {"count": 5, "x": x, "jid": id, "email": mail, "k": k, 'msg': "Applicant Details"})
    else:
        status = request.POST.getlist('choice')
        x = Jobs.objects.get(job_id=id).applicants.get(
            email=mail)
        x.Application_status = status[0]
        x.save()
        return redirect("applicants", id=id)
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Company').exists())
def company_profile(request):
    if request.method == "GET":
        x = company.objects.get(Email_ID=request.user.email)
        y = Edit_companyform(instance=x)

        return render(request, 'superset/company_dashboard.html', {"count": 6, "y": y, })
    else:
        x = company.objects.get(Email_ID=request.user.email)
        y = Edit_companyform(request.POST, instance=x)
        if y.is_valid():
            x.save()
            y.save()
            return redirect("company_dashboard")
