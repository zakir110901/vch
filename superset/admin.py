from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import student, Uvstudents, University, company, company_universities, Jobs, University_jobs, Applicants
# Register your models here.


class StudentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


class UvstudentsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


class UniversityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


class companyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


class company_universitiesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


class JobsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


class University_jobsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


class ApplicantsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


admin.site.register(student, StudentAdmin)
admin.site.register(Uvstudents, UvstudentsAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(company, companyAdmin)
admin.site.register(company_universities, company_universitiesAdmin)
admin.site.register(Jobs, JobsAdmin)
admin.site.register(Applicants, ApplicantsAdmin)
admin.site.register(University_jobs, University_jobsAdmin)
