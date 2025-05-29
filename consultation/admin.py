from django.contrib import admin
from .models import MedicalQuestionnaire, VideoCallPipeline

@admin.register(VideoCallPipeline)
class VideoCallPipelineAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_id', 'doctor_id', 'session_type', 'status', 'amount', 'created_at', 'updated_at')
    list_filter = ('status', 'session_type', 'created_at')
    search_fields = ('patient_id', 'doctor_id', 'channel_name')
    readonly_fields = ('created_at', 'updated_at', 'payment_completed_at', 'form_submitted_at', 'call_started_at', 'call_ended_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient_id', 'doctor_id', 'channel_name', 'session_type', 'status', 'amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'payment_completed_at', 'form_submitted_at', 'call_started_at', 'call_ended_at'),
            'classes': ('collapse',)
        }),
        ('Related Information', {
            'fields': ('questionnaire',),
            'classes': ('collapse',)
        }),
    )

@admin.register(MedicalQuestionnaire)
class MedicalQuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'nume_si_prenume', 'nume_si_prenume_reprezentant_legal', 'data_nastere', 'greutate', 'created_at')
    list_filter = ('created_at', 'alergic_la_vreun_medicament')
    search_fields = ('nume_si_prenume', 'nume_si_prenume_reprezentant_legal')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('nume_si_prenume', 'nume_si_prenume_reprezentant_legal', 'data_nastere', 'greutate')
        }),
        ('Medical Information', {
            'fields': (
                'alergic_la_vreun_medicament',
                'la_ce_medicament_este_alergic',
                'febra',
                'tuse',
                'dificultati_respiratorii',
                'astenie',
                'cefalee',
                'dureri_in_gat',
                'greturi_varsaturi',
                'diaree_constipatie',
                'refuzul_alimentatie',
                'iritatii_piele',
                'nas_infundat',
                'rinoree'
            )
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
