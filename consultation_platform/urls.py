"""
URL configuration for consultation_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from consultation.views import (
    ConsultationRequestView,
    ConsultationStatusView,  
    FormSubmissionView,
    CurrentConsultationView,
    MedicalQuestionnaireCreateView,
    CreateQuestionnaireAndLinkView , 
    PipelineQuestionnaireView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Consultation Request
    path('api/consultation/request/', ConsultationRequestView.as_view(), name='consultation-request'),
    
    # Form Submission - This needs to be BEFORE the status update pattern
    path('api/consultation/<int:pk>/submit-form/', FormSubmissionView.as_view(), name='form-submission'),
    
    # Create and Link Questionnaire
    path('api/consultation/<int:session_id>/create-questionnaire/', CreateQuestionnaireAndLinkView.as_view(), name='create-questionnaire-and-link'),
    
    # Consultation Status Updates
    path('api/consultation/<int:pk>/<str:action>/', ConsultationStatusView.as_view(), name='consultation-status'),
    
    # Current Consultation
    path('api/consultation/current/<str:user_type>/<int:user_id>/', CurrentConsultationView.as_view(), name='current-consultation'),
    
    # Medical Questionnaire
    path('api/questionnaires/', MedicalQuestionnaireCreateView.as_view(), name='questionnaire-create'),
    path('consultation/<int:session_id>/questionnaire/', PipelineQuestionnaireView.as_view(), name='pipeline-questionnaire'),
]
