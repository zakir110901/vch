from django.http import HttpResponse
from django.shortcuts import render,redirect
from ..forms import Uvstudentform, Universityform, Edit_clgform
from ..models import Uvstudents, University, student
from django.contrib.auth.decorators import login_required,user_passes_test
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

@login_required
@user_passes_test(lambda u: u.groups.filter(name='University').exists())
def universitydetails(request):
    if request.method=="GET":
        if University.objects.filter(email=request.user.email):
            return redirect("college_dashboard")
        else:
            x = request.user.email
            data = {
                "email":x
            }
            form = Universityform(initial=data)
            form.fields['email'].widget.attrs['readonly'] = True
            return render(request,'superset/university/universityform.html',{"form":form})
    else:
        form=Universityform(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("college_dashboard")
        else:
            return render(request,'superset/university/universityform.html',{"form":Universityform,"message":"The Details Entered are wrong"})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='University').exists())
def college_dashboard(request):
    e = request.user.email
    name = University.objects.filter(email = e).get().College
    return render(request,'superset/university/college_dashboard.html',{"count":0, "name":name})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='University').exists())
def addstudent(request):
    if request.method=="GET":
        y=University.objects.filter(email=request.user).get()
        x=Uvstudents.objects.filter(College_Name=y.College)
        if x:
            return render(request,'superset/university/college_dashboard.html',{"count":1,"mess_count":0,"message":"You Have Already Uploaded the File","x":x})
        else:
            initial_data = {'College_Name': y.College}
            form=Uvstudentform(initial=initial_data)
            form.fields['College_Name'].widget.attrs['readonly'] = True
            return render(request,'superset/university/college_dashboard.html',{"count":1,"mess_count":1,"form":form,"message":"Upload a CSV file with Name, Email and College of student"})
    else:
        y=University.objects.filter(email=request.user).get()
        form=Uvstudentform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("addstudent")
        else:
            initial_data = {'College_Name': y.College}
            form=Uvstudentform(initial=initial_data)
            form.fields['College_Name'].widget.attrs['readonly'] = True
            return render(request,'superset/university/college_dashboard.html',{"count":1,"mess_count":2,"form":form,"message":"Wrong Format"})    
        
@login_required
@user_passes_test(lambda u: u.groups.filter(name='University').exists())
def unregisteredst(request):
    y=University.objects.filter(email=request.user).get()
    x=student.objects.filter(College=y.College).filter(registration_status="UR")
    if x:
        return render(request,'superset/university/college_dashboard.html',{"count":2,"mess_count":0,"x":x})
    else:
        return render(request,'superset/university/college_dashboard.html',{"count":2,"mess_count":1,"message":"No Unregistered Students"})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='University').exists())
def registeredst(request):
    y=University.objects.filter(email=request.user).get()
    x=student.objects.filter(College=y.College).filter(registration_status="R")
    if x:
        return render(request,'superset/university/college_dashboard.html',{"count":3,"mess_count":0,"x":x})
    else:
        return render(request,'superset/university/college_dashboard.html',{"count":3,"mess_count":1,"message":"No Registered Students"})
    

@login_required
@user_passes_test(lambda u: u.groups.filter(name='University').exists())
def sendmail(request):
    if request.method=="POST":
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        sender_mail=request.user.email
        reciever_mail=request.POST['btn1']
        x=student.objects.filter(Email_ID=reciever_mail).get()
        y=University.objects.filter(email=sender_mail).get()
        subject = "Superset Registration"
        sender = {"email":sender_mail}
        replyTo = {"email":sender_mail}
        html_content = """<html><body><h1>Register For Superset </h1>
        <p>Click On the Link Below to Register<br> http://localhost:8000/home</p>
        <h4>Your Passphrase is :"""+str(y.Passphrase)+"""</h4></body></html>"""
        to = [{"email":reciever_mail,"name":x.Full_Name}]
        params = {"parameter":"My param value","subject":"New Subject"}
        # cc=[{'email':'eashansharma31@gmail.com'}]
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to,  reply_to=replyTo, headers=params,html_content=html_content, sender=sender, subject=subject)
        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email:")
        return redirect("unregisteredst")
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='University').exists())
def unapprovedst(request):
    y=University.objects.filter(email=request.user).get()
    x=student.objects.filter(College=y.College).filter(registration_status="R").filter(approval_status='UA')
    if x:
        return render(request,'superset/university/college_dashboard.html',{"count":4,"mess_count":0,"x":x})
    else:
        return render(request,'superset/university/college_dashboard.html',{"count":4,"mess_count":1,"message":"No Pending Approvals"})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='University').exists())
def approve(request,email):
    if request.method=="GET":
        x=student.objects.filter(Email_ID=email).get()
        if x.approval_status=="UA":
            return render(request,'superset/university/college_dashboard.html',{"count":5,"x":x,"btn_count":0})
        else:
            return render(request,'superset/university/college_dashboard.html',{"count":5,"x":x,"btn_count":1})
    
    if request.method=="POST":
        email=request.POST['btn']
        x=student.objects.filter(Email_ID=email).get()
        x.approval_status="A"
        x.save()
        return redirect("approvedst")

@login_required
@user_passes_test(lambda u: u.groups.filter(name='University').exists())
def approvedst(request):
    y=University.objects.filter(email=request.user).get()
    x=student.objects.filter(College=y.College).filter(registration_status="R").filter(approval_status='A')
    if x:
        return render(request,'superset/university/college_dashboard.html',{"count":6,"mess_count":0,"x":x})
    else:
        return render(request,'superset/university/college_dashboard.html',{"count":6,"mess_count":1,"message":"No Students Approved"})
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='University').exists())
def college_profile(request):
    if request.method == "GET":
        x = University.objects.get(email=request.user.email)
        y = Edit_clgform(instance=x)
        return render(request, 'superset/university/college_dashboard.html', {"count": 7, "y": y, })
    else:
        x = University.objects.get(email=request.user.email)
        y = Edit_clgform(request.POST, instance=x)
        if y.is_valid():
            x.save()
            y.save()
            return redirect("college_dashboard")