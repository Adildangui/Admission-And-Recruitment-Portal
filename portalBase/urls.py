from django.contrib import admin
from django.urls import path, include
from . import views
from phDAdmissionPortal import views as phDAdmissionViews
from yourApp import views as yourAppViews


urlpatterns = [
    path('', views.Apply, name = "Apply"),
    path('apply/', views.Apply, name = "Apply"),
    path('phDAdmission/', phDAdmissionViews.AdmissionDetails, name = "phDAdmission"),
    path('yourApp/', yourAppViews.AdmissionDetails, name = "yourApp"),

]