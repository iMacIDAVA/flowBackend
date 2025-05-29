from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class MedicalQuestionnaire(models.Model):
    nume_si_prenume_reprezentant_legal = models.CharField(max_length=255)
    nume_si_prenume = models.CharField(max_length=255)
    data_nastere = models.DateField()
    greutate = models.DecimalField(max_digits=5, decimal_places=2)
    alergic_la_vreun_medicament = models.BooleanField(default=False)
    la_ce_medicament_este_alergic = models.CharField(max_length=255, blank=True, null=True)
    febra = models.BooleanField(default=False)
    tuse = models.BooleanField(default=False)
    dificultati_respiratorii = models.BooleanField(default=False)
    astenie = models.BooleanField(default=False)
    cefalee = models.BooleanField(default=False)
    dureri_in_gat = models.BooleanField(default=False)
    greturi_varsaturi = models.BooleanField(default=False)
    diaree_constipatie = models.BooleanField(default=False)
    refuzul_alimentatie = models.BooleanField(default=False)
    iritatii_piele = models.BooleanField(default=False)
    nas_infundat = models.BooleanField(default=False)
    rinoree = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
#can you make me endpoint that it will recive MedicalQuestionnaire and after checking 
class VideoCallPipeline(models.Model):
    class PipelineStatus(models.TextChoices):
        REQUESTED = 'Requested'
        ACCEPTED = 'Accepted'
        REJECTED = 'Rejected'
        PAYMENT_PENDING = 'PaymentPending'
        PAYMENT_COMPLETED = 'PaymentCompleted'
        FORM_PENDING = 'FormPending'
        FORM_SUBMITTED = 'FormSubmitted'
        CALL_READY = 'CallReady'
        CALL_STARTED = 'CallStarted'
        CALL_ENDED = 'CallEnded'

    class SessionType(models.TextChoices):
        CALL = 'Call'
        CHAT = 'Chat'
        RECOMMENDATION = 'Recommendation'

    patient_id = models.IntegerField(default=0)
    doctor_id = models.IntegerField(default=0)
    channel_name = models.CharField(max_length=100)
    session_type = models.CharField(max_length=20, choices=SessionType.choices)
    status = models.CharField(max_length=20, choices=PipelineStatus.choices, default=PipelineStatus.REQUESTED)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    questionnaire = models.ForeignKey(MedicalQuestionnaire, null=True, blank=True, on_delete=models.SET_NULL)
    payment_completed_at = models.DateTimeField(null=True, blank=True)
    form_submitted_at = models.DateTimeField(null=True, blank=True)
    call_started_at = models.DateTimeField(null=True, blank=True)
    call_ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['patient_id']),
            models.Index(fields=['doctor_id']),
            models.Index(fields=['status']),
            models.Index(fields=['session_type']),
        ]
