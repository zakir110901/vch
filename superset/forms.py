from django import forms
from .models import student, Uvstudents, University, company, Jobs


class studentform(forms.ModelForm):

    class Meta:
        model = student
        fields = '__all__'


class Edit_stform(forms.ModelForm):

    class Meta:
        model = student
        fields = '__all__'
        widgets = {
            'Email_ID': forms.EmailInput({'readonly': 'readonly'}),
            'College': forms.TextInput({'readonly': 'readonly'}),
            'College_Roll_No': forms.TextInput({'readonly': 'readonly'}),
            'Passing_Year': forms.TextInput({'readonly': 'readonly'}),
            'Xth_Percentage': forms.TextInput({'readonly': 'readonly'}),
            'XIIth_Percentage': forms.TextInput({'readonly': 'readonly'}),
            # 'Xth_Marksheet': forms.FileInput({'disabled': 'disabled'}),
            # 'XIIth_Marksheet': forms.FileInput({'disabled': 'disabled'}),
            'DOB': forms.DateInput({'readonly': 'readonly'}),
            'Course': forms.TextInput({'readonly': 'readonly'}),
            'Branch': forms.TextInput({'readonly': 'readonly'}),
            'registration_status': forms.HiddenInput(),
            'approval_status': forms.HiddenInput()
        }

class Edit_clgform(forms.ModelForm):

    class Meta:
        model = University
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput({'readonly': 'readonly'}),
            'College': forms.TextInput({'readonly': 'readonly'}),
            # 'University': forms.TextInput({'readonly': 'readonly'}),
            'Passphrase': forms.TextInput({'readonly': 'readonly'}),
            # 'Full_Name': forms.TextInput({'readonly': 'readonly'}),
        }

class Edit_companyform(forms.ModelForm):

    class Meta:
        model = company
        fields = '__all__'
        widgets = {
            'Email_ID': forms.EmailInput({'readonly': 'readonly'}),
            'Company_Name': forms.TextInput({'readonly': 'readonly'}),
        }


class Uvstudentform(forms.ModelForm):
    class Meta:
        model = Uvstudents
        fields = '__all__'


class Universityform(forms.ModelForm):
    class Meta:
        model = University
        fields = '__all__'


class Studentform(forms.ModelForm):
    class Meta:
        model = student
        fields = '__all__'


class company_form(forms.ModelForm):

    class Meta:
        model = company
        fields = "__all__"


class job_form(forms.ModelForm):

    class Meta:
        model = Jobs
        fields = ['job_role', 'CTC', 'Location', 'Xth_perecentage',
                  'XIIth_percentage', 'College_CGPA', 'Company_Name']
