from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
from django.db import models

courses = (
    ('B.Tech', 'B.Tech'),
    ('B.Sc.', 'B.Sc.'),
    ('B.A', 'B.A'),
    ('M.Sc', 'M.Sc'),
    ('M.Tech', 'M.Tech')
)

branches = (
    ('CSE', 'CSE'),
    ('AI', 'AI'),
    ('ECE', 'ECE')
)

genders = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

categories = (
    ('General', 'General'),
    ('SC', 'SC'),
    ('ST', 'ST'),
    ('OBC', 'OBC'),
)
# Create your models here.
r_status=(
    ('UR','Unregistered'),
    ('R','Registered'),
)
a_status=(
    ('UA','Unapproved'),
    ('A','Approved'),
)
class student(models.Model):
    Email_ID = models.EmailField(unique=True)
    Full_Name = models.CharField(max_length=100)
    College = models.CharField(max_length=250)
    College_Roll_No = models.CharField(max_length=100,blank=True)
    Course = models.CharField(max_length = 20, choices = courses,blank=True)
    Branch = models.CharField(max_length = 20, choices = branches,blank=True)
    Passing_Year = models.CharField(max_length=50,blank=True)
    Gender = models.CharField(max_length = 20, choices = genders,blank=True)
    DOB = models.DateField(blank=True,null=True)
    Category = models.CharField(max_length = 20, choices = categories,blank=True)
    Contact_Number = models.IntegerField(blank=True,null=True)
    Skills = models.CharField(max_length=200,blank=True)
    Photo = models.ImageField(upload_to='profile_photo/',blank=True)
    College_Id_Card = models.FileField(upload_to='clg_id_card/',blank=True)
    Resume = models.FileField(upload_to='resumes/',blank=True)
    Xth_Percentage = models.DecimalField(max_digits=4, decimal_places=2,blank=True,null=True)
    Xth_Marksheet = models.FileField(upload_to='10th_marksheet/',blank=True)
    XIIth_Percentage = models.DecimalField(max_digits=4, decimal_places=2,blank=True,null=True)
    XIIth_Marksheet = models.FileField(upload_to='12th_marksheet/',blank=True)
    College_CGPA = models.DecimalField(max_digits=3, decimal_places=2,blank=True,null=True)
    College_Marksheets = models.FileField(upload_to='clg_marksheet/',blank=True)
    registration_status=models.CharField(max_length=20,choices=r_status,default="UR")
    approval_status=models.CharField(max_length=20,choices=a_status,default="UA")

    def __str__(self):
        return self.Email_ID

class Uvstudents(models.Model):
    College_Name = models.CharField(max_length=250,unique=True)
    File = models.FileField(upload_to='college_Students/',validators=[FileExtensionValidator(['csv'])])
    def __str__(self):
        return self.College_Name
    
class University(models.Model):
    College=models.CharField(max_length=250,unique=True)
    University=models.CharField(max_length=250)
    Passphrase=models.CharField(max_length=250,unique=True)
    email=models.EmailField(unique=True)
    Full_Name=models.CharField(max_length=250)
    def __str__(self):
        return self.College

class company(models.Model):
    Email_ID = models.EmailField(unique=True)
    Company_Name = models.CharField(max_length=100,unique=True) 
    Address = models.CharField(max_length=300)   
    Description = models.TextField(max_length=500)

    def __str__(self):
        return self.Company_Name
    
class company_universities(models.Model):
    company_name=models.ForeignKey(company, on_delete=models.CASCADE,blank=True,null=True,related_name='comuv')
    universities=models.CharField(max_length=100,blank=True,null=True) 

    def __str__(self):
        return self.universities 
    
class Jobs(models.Model):
    job_id = models.CharField(unique=True, max_length=3)
    job_role=models.CharField(max_length=100)
    CTC=models.CharField(max_length=100) 
    Location=models.CharField(max_length=200)
    Xth_perecentage=models.DecimalField(max_digits=4, decimal_places=2,blank=True,null=True)
    XIIth_percentage= models.DecimalField(max_digits=4, decimal_places=2,blank=True,null=True)
    College_CGPA = models.DecimalField(max_digits=3, decimal_places=2,blank=True,null=True)  
    Company_Name = models.CharField(max_length=100) 

    def __str__(self):
        return self.job_id

class University_jobs(models.Model):
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE, blank=True, null=True, related_name='studentjob')
    universitiy = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.job_id)


class Applicants(models.Model):
    a_choices = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    )
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE, blank=True, null=True, related_name='applicants')
    email = models.EmailField()
    Application_status = models.CharField(max_length=1, choices=a_choices, default='P')
    Resume = models.FileField(upload_to='Job_Applicants/',validators=[FileExtensionValidator(['pdf'])])

    def __str__(self):
        return str(self.email)

    
