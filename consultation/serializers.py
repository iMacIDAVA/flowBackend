from rest_framework import serializers
from .models import MedicalQuestionnaire, VideoCallPipeline

class MedicalQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalQuestionnaire
        fields = '__all__'

class VideoCallPipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCallPipeline
        fields = '__all__'

class RequestConsultationSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField(
        required=True,
        error_messages={
            'required': 'Patient ID is required',
            'invalid': 'Patient ID must be a valid integer'
        }
    )
    doctor_id = serializers.IntegerField(
        required=True,
        error_messages={
            'required': 'Doctor ID is required',
            'invalid': 'Doctor ID must be a valid integer'
        }
    )
    session_type = serializers.ChoiceField(
        choices=VideoCallPipeline.SessionType.choices,
        required=True,
        error_messages={
            'required': 'Session type is required',
            'invalid_choice': 'Session type must be one of: Call, Chat, Recommendation'
        }
    )
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        error_messages={
            'required': 'Amount is required',
            'invalid': 'Amount must be a valid decimal number'
        }
    )

class SubmitFormSerializer(serializers.Serializer):
    questionnaire_id = serializers.IntegerField(
        required=True,
        error_messages={
            'required': 'Questionnaire ID is required',
            'invalid': 'Questionnaire ID must be a valid integer'
        }
    )

    def validate_questionnaire_id(self, value):
        if not MedicalQuestionnaire.objects.filter(id=value).exists():
            raise serializers.ValidationError("Questionnaire with this ID does not exist")
        return value 




class MedicalQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalQuestionnaire
        fields = '__all__'  # Include all fields from MedicalQuestionnaire