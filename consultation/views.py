# from django.shortcuts import render
# from rest_framework import status, generics, viewsets
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from django.shortcuts import get_object_or_404
# from django.db import transaction
# from .models import VideoCallPipeline, MedicalQuestionnaire
# from .serializers import (
#     VideoCallPipelineSerializer, MedicalQuestionnaireSerializer,
#     RequestConsultationSerializer, SubmitFormSerializer
# )
# from django.contrib.auth import get_user_model
# from rest_framework.permissions import IsAuthenticated, AllowAny
# import uuid
# from django.utils import timezone

# class ConsultationRequestView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:

#             serializer = RequestConsultationSerializer(data=request.data)
#             if not serializer.is_valid():
#                 return Response({
#                     'status': 'error',
#                     'message': 'Validation failed',
#                     'errors': serializer.errors
#                 }, status=status.HTTP_400_BAD_REQUEST)

#         data = serializer.validated_data
            
#             existing_pipeline = VideoCallPipeline.objects.filter(
#                 patient_id=data['patient_id'],
#                 doctor_id=data['doctor_id']
#             ).exclude(
#                 status__in=[
#                     VideoCallPipeline.PipelineStatus.REJECTED,
#                     VideoCallPipeline.PipelineStatus.CALL_ENDED
#                 ]
#             ).first()

#             if existing_pipeline:
#                 return Response({
#                     'status': 'error',
#                     'message': 'An active consultation already exists between this patient and doctor',
#                     'pipeline_id': existing_pipeline.id
#                 }, status=status.HTTP_400_BAD_REQUEST)

#         pipeline = VideoCallPipeline.objects.create(
#             patient_id=data['patient_id'],
#             doctor_id=data['doctor_id'],
#             channel_name=str(uuid.uuid4()),
#             session_type=data['session_type'],
#             amount=data['amount'],
#             status=VideoCallPipeline.PipelineStatus.REQUESTED
#         )

#             return Response({
#                 'status': 'success',
#                 'message': 'Consultation request created successfully',
#                 'data': VideoCallPipelineSerializer(pipeline).data
#             }, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({
#                 'status': 'error',
#                 'message': 'An unexpected error occurred',
#                 'error': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class ConsultationStatusView(APIView):
#     permission_classes = [AllowAny]

#     def get_pipeline(self, pk):
#         return get_object_or_404(VideoCallPipeline, pk=pk)

#     def validate_status_transition(self, current_status, new_status):
#         # If the new status is the same as current status, return success
#         if current_status == new_status:
#             return True, None

#         valid_transitions = {
#             VideoCallPipeline.PipelineStatus.REQUESTED: [VideoCallPipeline.PipelineStatus.ACCEPTED, VideoCallPipeline.PipelineStatus.REJECTED],
#             VideoCallPipeline.PipelineStatus.ACCEPTED: [VideoCallPipeline.PipelineStatus.PAYMENT_PENDING],
#             VideoCallPipeline.PipelineStatus.PAYMENT_PENDING: [VideoCallPipeline.PipelineStatus.PAYMENT_COMPLETED],
#             VideoCallPipeline.PipelineStatus.PAYMENT_COMPLETED: [VideoCallPipeline.PipelineStatus.FORM_PENDING],
#             VideoCallPipeline.PipelineStatus.FORM_PENDING: [VideoCallPipeline.PipelineStatus.FORM_SUBMITTED],
#             VideoCallPipeline.PipelineStatus.FORM_SUBMITTED: [VideoCallPipeline.PipelineStatus.CALL_READY],
#             VideoCallPipeline.PipelineStatus.CALL_READY: [VideoCallPipeline.PipelineStatus.CALL_STARTED],
#             VideoCallPipeline.PipelineStatus.CALL_STARTED: [VideoCallPipeline.PipelineStatus.CALL_ENDED],
#         }
        
#         if current_status not in valid_transitions:
#             return False, f"Invalid current status: {current_status}"
            
#         if new_status not in valid_transitions[current_status]:
#             return False, f"Cannot transition from {current_status} to {new_status}. Valid transitions are: {valid_transitions[current_status]}"
            
#         return True, None

#     def put(self, request, pk, action):
#         try:
#             # Validate action
#             valid_actions = {
#                 'accept': VideoCallPipeline.PipelineStatus.ACCEPTED,
#                 'reject': VideoCallPipeline.PipelineStatus.REJECTED,
#                 'paymentPending': VideoCallPipeline.PipelineStatus.PAYMENT_PENDING,
#                 'paymentCompleted': VideoCallPipeline.PipelineStatus.PAYMENT_COMPLETED,
#                 'formPending': VideoCallPipeline.PipelineStatus.FORM_PENDING,
#                 'callReady': VideoCallPipeline.PipelineStatus.CALL_READY,
#                 'callStarted': VideoCallPipeline.PipelineStatus.CALL_STARTED,
#                 'callEnded': VideoCallPipeline.PipelineStatus.CALL_ENDED
#             }

#             if action not in valid_actions:
#                 return Response({
#                     'status': 'error',
#                     'message': f'Invalid action: {action}. Valid actions are: {list(valid_actions.keys())}'
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Get pipeline
#             pipeline = self.get_pipeline(pk)
            
#             # Validate status transition
#             is_valid, error_message = self.validate_status_transition(pipeline.status, valid_actions[action])
#             if not is_valid:
#                 return Response({
#                     'status': 'error',
#                     'message': error_message,
#                     'current_status': pipeline.status
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Update status
#             pipeline.status = valid_actions[action]
            
#             # Update timestamps for specific statuses
#             if action == 'paymentCompleted':
#         pipeline.payment_completed_at = timezone.now()
#             elif action == 'callStarted':
#                 pipeline.call_started_at = timezone.now()
#             elif action == 'callEnded':
#                 pipeline.call_ended_at = timezone.now()
            
#         pipeline.save()
            
#             return Response({
#                 'status': 'success',
#                 'message': f'Status updated to {valid_actions[action]}',
#                 'data': VideoCallPipelineSerializer(pipeline).data
#             })
            
#         except Exception as e:
#             return Response({
#                 'status': 'error',
#                 'message': 'An unexpected error occurred',
#                 'error': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class FormSubmissionView(APIView):
#     permission_classes = [AllowAny]

#     def put(self, request, pk):
#         try:
#             # Check if consultation exists
#         pipeline = get_object_or_404(VideoCallPipeline, pk=pk)
            
#             # Check if consultation is in correct state
#         if pipeline.status != VideoCallPipeline.PipelineStatus.FORM_PENDING:
#                 return Response({
#                     'status': 'error',
#                     'message': 'Form can only be submitted when consultation is in FormPending state',
#                     'current_status': pipeline.status
#                 }, status=status.HTTP_400_BAD_REQUEST)
            
#             # Validate request data
#             if not request.data:
#                 return Response({
#                     'status': 'error',
#                     'message': 'No data provided. Please provide questionnaire_id'
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             if 'questionnaire_id' not in request.data:
#                 return Response({
#                     'status': 'error',
#                     'message': 'questionnaire_id is required'
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Validate questionnaire exists
#             questionnaire_id = request.data.get('questionnaire_id')
#             try:
#                 questionnaire = MedicalQuestionnaire.objects.get(id=questionnaire_id)
#             except MedicalQuestionnaire.DoesNotExist:
#                 return Response({
#                     'status': 'error',
#                     'message': f'Questionnaire with ID {questionnaire_id} does not exist'
#                 }, status=status.HTTP_404_NOT_FOUND)

#             # Check if questionnaire is already linked to another consultation
#             existing_pipeline = VideoCallPipeline.objects.filter(
#                 questionnaire_id=questionnaire_id
#             ).exclude(
#                 id=pk
#             ).first()

#             if existing_pipeline:
#                 return Response({
#                     'status': 'error',
#                     'message': f'This questionnaire is already linked to consultation ID {existing_pipeline.id}'
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Update pipeline
#         pipeline.status = VideoCallPipeline.PipelineStatus.FORM_SUBMITTED
#             pipeline.questionnaire = questionnaire
#         pipeline.form_submitted_at = timezone.now()
#         pipeline.save()
            
#             return Response({
#                 'status': 'success',
#                 'message': 'Form submitted successfully',
#                 'data': VideoCallPipelineSerializer(pipeline).data
#             })
            
#         except Exception as e:
#             return Response({
#                 'status': 'error',
#                 'message': 'An unexpected error occurred',
#                 'error': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class CurrentConsultationView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, user_type, user_id):
#         try:
#             if user_type not in ['patient', 'doctor']:
#                 return Response({
#                     'status': 'error',
#                     'message': 'Invalid user type. Must be either patient or doctor'
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             filter_kwargs = {f'{user_type}_id': user_id}
#         pipeline = VideoCallPipeline.objects.filter(
#                 **filter_kwargs
#             ).exclude(
#                 status=VideoCallPipeline.PipelineStatus.CALL_ENDED
#             ).order_by('-created_at').first()

#         if not pipeline:
#                 return Response({
#                     'status': 'success',
#                     'has_active_session': False,
#                     'message': 'No active consultation found'
#                 })

#             return Response({
#                 'status': 'success',
#                 'has_active_session': True,
#                 'data': VideoCallPipelineSerializer(pipeline).data
#             })
            
#         except Exception as e:
#             return Response({
#                 'status': 'error',
#                 'message': 'An unexpected error occurred',
#                 'error': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class MedicalQuestionnaireCreateView(generics.CreateAPIView):
#     queryset = MedicalQuestionnaire.objects.all()
#     serializer_class = MedicalQuestionnaireSerializer
#     permission_classes = [AllowAny]

# class CreateQuestionnaireAndLinkView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, session_id):
#         try:
#             # First validate the session exists and is in correct state
#             pipeline = get_object_or_404(VideoCallPipeline, pk=session_id)
            
#             if pipeline.status != VideoCallPipeline.PipelineStatus.FORM_PENDING:
#                 return Response({
#                     'status': 'error',
#                     'message': 'Form can only be submitted when consultation is in FormPending state',
#                     'current_status': pipeline.status
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Validate questionnaire data
#             questionnaire_serializer = MedicalQuestionnaireSerializer(data=request.data)
#             if not questionnaire_serializer.is_valid():
#                 return Response({
#                     'status': 'error',
#                     'message': 'Validation failed',
#                     'errors': questionnaire_serializer.errors
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Perform both operations in a single transaction
#             with transaction.atomic():
#                 # Create the questionnaire
#                 questionnaire = questionnaire_serializer.save()
                
#                 # Update the pipeline
#                 pipeline.questionnaire = questionnaire
#                 pipeline.status = VideoCallPipeline.PipelineStatus.FORM_SUBMITTED
#                 pipeline.form_submitted_at = timezone.now()
#                 pipeline.save()

#             return Response({
#                 'status': 'success',
#                 'message': 'Questionnaire created and linked successfully',
#                 'data': {
#                     'questionnaire': MedicalQuestionnaireSerializer(questionnaire).data,
#                     'pipeline': VideoCallPipelineSerializer(pipeline).data
#                 }
#             }, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({
#                 'status': 'error',
#                 'message': 'An unexpected error occurred',
#                 'error': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import VideoCallPipeline, MedicalQuestionnaire
from .serializers import (
    VideoCallPipelineSerializer, MedicalQuestionnaireSerializer,
    RequestConsultationSerializer
)
from rest_framework.permissions import AllowAny
import uuid
from django.utils import timezone

class ConsultationRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = RequestConsultationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'status': 'error',
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data
            
            # Check if doctor has any active sessions
            doctor_active_sessions = VideoCallPipeline.objects.filter(
                doctor_id=data['doctor_id']
            ).exclude(
                status__in=[
                    VideoCallPipeline.PipelineStatus.REJECTED,
                    VideoCallPipeline.PipelineStatus.CALL_ENDED
                ]
            ).first()

            if doctor_active_sessions:
                return Response({
                    'status': 'error',
                    'message': 'Doctor is currently in an active consultation',
                    'pipeline_id': doctor_active_sessions.id
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if patient has any active sessions with this doctor
            existing_pipeline = VideoCallPipeline.objects.filter(
                patient_id=data['patient_id'],
                doctor_id=data['doctor_id']
            ).exclude(
                status__in=[
                    VideoCallPipeline.PipelineStatus.REJECTED,
                    VideoCallPipeline.PipelineStatus.CALL_ENDED
                ]
            ).first()

            if existing_pipeline:
                return Response({
                    'status': 'error',
                    'message': 'An active consultation already exists between this patient and doctor',
                    'pipeline_id': existing_pipeline.id
                }, status=status.HTTP_400_BAD_REQUEST)

            pipeline = VideoCallPipeline.objects.create(
                patient_id=data['patient_id'],
                doctor_id=data['doctor_id'],
                channel_name=str(uuid.uuid4()),
                session_type=data['session_type'],
                amount=data['amount'],
                status=VideoCallPipeline.PipelineStatus.REQUESTED
            )

            return Response({
                'status': 'success',
                'message': 'Consultation request created successfully',
                'data': VideoCallPipelineSerializer(pipeline).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConsultationStatusView(APIView):
    permission_classes = [AllowAny]

    def get_pipeline(self, pk):
        return get_object_or_404(VideoCallPipeline, pk=pk)

    def validate_status_transition(self, current_status, new_status):
        # If the new status is the same as current status, return success
        if current_status == new_status:
            return True, None

        valid_transitions = {
            VideoCallPipeline.PipelineStatus.REQUESTED: [
                VideoCallPipeline.PipelineStatus.ACCEPTED,
                VideoCallPipeline.PipelineStatus.REJECTED,

            ],
            VideoCallPipeline.PipelineStatus.ACCEPTED: [VideoCallPipeline.PipelineStatus.PAYMENT_PENDING , VideoCallPipeline.PipelineStatus.CALL_ENDED],
            VideoCallPipeline.PipelineStatus.PAYMENT_PENDING: [VideoCallPipeline.PipelineStatus.PAYMENT_COMPLETED , VideoCallPipeline.PipelineStatus.CALL_ENDED],
            VideoCallPipeline.PipelineStatus.PAYMENT_COMPLETED: [VideoCallPipeline.PipelineStatus.FORM_PENDING , VideoCallPipeline.PipelineStatus.CALL_ENDED],
            VideoCallPipeline.PipelineStatus.FORM_PENDING: [VideoCallPipeline.PipelineStatus.FORM_SUBMITTED , VideoCallPipeline.PipelineStatus.CALL_ENDED],
            VideoCallPipeline.PipelineStatus.FORM_SUBMITTED: [VideoCallPipeline.PipelineStatus.CALL_READY , VideoCallPipeline.PipelineStatus.CALL_ENDED],
            VideoCallPipeline.PipelineStatus.CALL_READY: [VideoCallPipeline.PipelineStatus.CALL_STARTED , VideoCallPipeline.PipelineStatus.CALL_ENDED],
            VideoCallPipeline.PipelineStatus.CALL_STARTED: [VideoCallPipeline.PipelineStatus.CALL_ENDED],
        }
        
        if current_status not in valid_transitions:
            return False, f"Invalid current status: {current_status}"
            
        if new_status not in valid_transitions[current_status]:
            return False, f"Cannot transition from {current_status} to {new_status}. Valid transitions are: {valid_transitions[current_status]}"
            
        return True, None

    def put(self, request, pk, action):
        try:
            # Validate action
            valid_actions = {
                'accept': VideoCallPipeline.PipelineStatus.ACCEPTED,
                'reject': VideoCallPipeline.PipelineStatus.REJECTED,
                'paymentPending': VideoCallPipeline.PipelineStatus.PAYMENT_PENDING,
                'paymentCompleted': VideoCallPipeline.PipelineStatus.PAYMENT_COMPLETED,
                'formPending': VideoCallPipeline.PipelineStatus.FORM_PENDING,
                'callReady': VideoCallPipeline.PipelineStatus.CALL_READY,
                'callStarted': VideoCallPipeline.PipelineStatus.CALL_STARTED,
                'callEnded': VideoCallPipeline.PipelineStatus.CALL_ENDED
            }

            if action not in valid_actions:
                return Response({
                    'status': 'error',
                    'message': f'Invalid action: {action}. Valid actions are: {list(valid_actions.keys())}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get pipeline
            pipeline = self.get_pipeline(pk)
            
            # Validate status transition
            is_valid, error_message = self.validate_status_transition(pipeline.status, valid_actions[action])
            if not is_valid:
                return Response({
                    'status': 'error',
                    'message': error_message,
                    'current_status': pipeline.status
                }, status=status.HTTP_400_BAD_REQUEST)

            # Update status
            pipeline.status = valid_actions[action]
            
            # Update timestamps for specific statuses
            if action == 'paymentCompleted':
                pipeline.payment_completed_at = timezone.now()
            elif action == 'callStarted':
                pipeline.call_started_at = timezone.now()
            elif action == 'callEnded':
                pipeline.call_ended_at = timezone.now()
            
            pipeline.save()
            
            return Response({
                'status': 'success',
                'message': f'Status updated to {valid_actions[action]}',
                'data': VideoCallPipelineSerializer(pipeline).data
            })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FormSubmissionView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, pk):
        try:
            # Check if consultation exists
            pipeline = get_object_or_404(VideoCallPipeline, pk=pk)
            
            # Check if consultation is in correct state
            if pipeline.status != VideoCallPipeline.PipelineStatus.FORM_PENDING:
                return Response({
                    'status': 'error',
                    'message': 'Form can only be submitted when consultation is in FormPending state',
                    'current_status': pipeline.status
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate request data
            if not request.data:
                return Response({
                    'status': 'error',
                    'message': 'No data provided. Please provide questionnaire_id'
                }, status=status.HTTP_400_BAD_REQUEST)

            if 'questionnaire_id' not in request.data:
                return Response({
                    'status': 'error',
                    'message': 'questionnaire_id is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate questionnaire exists
            questionnaire_id = request.data.get('questionnaire_id')
            try:
                questionnaire = MedicalQuestionnaire.objects.get(id=questionnaire_id)
            except MedicalQuestionnaire.DoesNotExist:
                return Response({
                    'status': 'error',
                    'message': f'Questionnaire with ID {questionnaire_id} does not exist'
                }, status=status.HTTP_404_NOT_FOUND)

            # Check if questionnaire is already linked to another consultation
            existing_pipeline = VideoCallPipeline.objects.filter(
                questionnaire_id=questionnaire_id
            ).exclude(
                id=pk
            ).first()

            if existing_pipeline:
                return Response({
                    'status': 'error',
                    'message': f'This questionnaire is already linked to consultation ID {existing_pipeline.id}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Update pipeline
            pipeline.status = VideoCallPipeline.PipelineStatus.FORM_SUBMITTED
            pipeline.questionnaire = questionnaire
            pipeline.form_submitted_at = timezone.now()
            pipeline.save()
            
            return Response({
                'status': 'success',
                'message': 'Form submitted successfully',
                'data': VideoCallPipelineSerializer(pipeline).data
            })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CurrentConsultationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_type, user_id):
        try:
            if user_type not in ['patient', 'doctor']:
                return Response({
                    'status': 'error',
                    'message': 'Invalid user type. Must be either patient or doctor'
                }, status=status.HTTP_400_BAD_REQUEST)

            filter_kwargs = {f'{user_type}_id': user_id}
            pipeline = VideoCallPipeline.objects.filter(
                **filter_kwargs
            ).exclude(
                    status__in=[
                        VideoCallPipeline.PipelineStatus.CALL_ENDED,
                        VideoCallPipeline.PipelineStatus.REJECTED
                    ]
                #status=VideoCallPipeline.PipelineStatus.CALL_ENDED
            ).order_by('-created_at').first()

            if not pipeline:
                return Response({
                    'status': 'success',
                    'has_active_session': False,
                    'message': 'No active consultation found'
                })

            return Response({
                'status': 'success',
                'has_active_session': True,
                'data': VideoCallPipelineSerializer(pipeline).data
            })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MedicalQuestionnaireCreateView(generics.CreateAPIView):
    queryset = MedicalQuestionnaire.objects.all()
    serializer_class = MedicalQuestionnaireSerializer
    permission_classes = [AllowAny]

class CreateQuestionnaireAndLinkView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, session_id):
        try:
            # First validate the session exists and is in correct state
            pipeline = get_object_or_404(VideoCallPipeline, pk=session_id)
            
            if pipeline.status != VideoCallPipeline.PipelineStatus.FORM_PENDING:
                return Response({
                    'status': 'error',
                    'message': 'Form can only be submitted when consultation is in FormPending state',
                    'current_status': pipeline.status
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate questionnaire data
            questionnaire_serializer = MedicalQuestionnaireSerializer(data=request.data)
            if not questionnaire_serializer.is_valid():
                return Response({
                    'status': 'error',
                    'message': 'Validation failed',
                    'errors': questionnaire_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # Perform both operations in a single transaction
            with transaction.atomic():
                # Create the questionnaire
                questionnaire = questionnaire_serializer.save()
                
                # Update the pipeline
                pipeline.questionnaire = questionnaire
                pipeline.status = VideoCallPipeline.PipelineStatus.FORM_SUBMITTED
                pipeline.form_submitted_at = timezone.now()
                pipeline.save()

            return Response({
                'status': 'success',
                'message': 'Questionnaire created and linked successfully',
                'data': {
                    'questionnaire': MedicalQuestionnaireSerializer(questionnaire).data,
                    'pipeline': VideoCallPipelineSerializer(pipeline).data
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class PipelineQuestionnaireView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, session_id):
        try:
            # Fetch the VideoCallPipeline
            pipeline = get_object_or_404(VideoCallPipeline, pk=session_id)
            
            # Check if questionnaire exists
            if not pipeline.questionnaire:
                return Response({
                    'status': 'error',
                    'message': 'No questionnaire associated with this pipeline'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Serialize and return the questionnaire
            serializer = MedicalQuestionnaireSerializer(pipeline.questionnaire)
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)