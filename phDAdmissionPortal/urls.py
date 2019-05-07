from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	
    path('', views.AdmissionDetails, name = "AdmissionDetails"),
    path('admissionDetails/', views.AdmissionDetails, name = "AdmissionDetails"),
    path('personalDetails/', views.PersonalDetails, name = "PersonalDetails"),
    path('educationalQualifications/', views.EducationalQualifications, name = "EducationalQualifications"),
    path('workExperience/', views.WorkExperience, name = "WorkExperience"),
    path('attachments/', views.Attachments, name = "Attachments"),
    path('success/', views.Success, name = "Success"),
    path('adminFilterView/', views.AdminFilterView, name = "AdminFilterView"),
    path('adminResultView/', views.AdminResultView, name = "AdminResultView"),
    path('adminPrimaryView/', views.AdminPrimaryView, name = "AdminPrimaryView"),
    path('adminLogin/', views.AdminLogin, name = "AdminLogin"),
    
]
