from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	
	path('', include('portalBase.urls')),
    path('portalHome/', include('portalBase.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('phDAdmission/', include('phDAdmissionPortal.urls'), name = "phDAdmission"),
    path('yourApp/', include('yourApp.urls'), name = "yourApp"),
]