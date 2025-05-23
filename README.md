# Consultation Platform Documentation

## Overview
This documentation covers both the backend API and Flutter mobile application implementation for a video consultation platform that enables patients to connect with doctors through video calls, chat, or recommendations.

## System Architecture

### Backend API
The backend is built with Django REST Framework and manages the consultation pipeline, user authentication, and data persistence.

### Mobile App
The Flutter mobile application provides separate interfaces for patients and doctors, handling the consultation flow and real-time communication.

## Pipeline States
The consultation process follows a specific state machine:

```
REQUESTED
    ↓
    ├──→ ACCEPTED → PAYMENT_PENDING → PAYMENT_COMPLETED → FORM_PENDING → FORM_SUBMITTED → CALL_READY → CALL_STARTED → CALL_ENDED
    ↓
REJECTED
```

### State Descriptions and UI Flows



1. **REQUESTED**
   - **Patient View**: 
     - Shows waiting screen with "Waiting for doctor to accept" message
     - No actions available
   - **Doctor View**:
     - Shows request screen with patient details
     - Options to Accept or Reject
     - Displays session type (Call/Chat/Recommendation)

2. **ACCEPTED**
   - **Patient View**:
     - Shows confirmation screen
     - Displays "Doctor has accepted your request"
     - Button to proceed to payment
   - **Doctor View**:
     - Shows waiting screen
     - Displays "Waiting for patient payment"

3. **REJECTED**
   - **Patient View**:
     - Shows rejection screen
     - Displays "Doctor unavailable"
     - Button to return to home screen
   - **Doctor View**:
     - Returns to home screen

4. **PAYMENT_PENDING**
   - **Patient View**:
     - Shows payment screen
     - Integrates payment gateway (e.g., Stripe)
     - Handles payment success/failure
   - **Doctor View**:
     - Shows waiting screen
     - Displays "Waiting for patient to complete payment"

5. **PAYMENT_COMPLETED**
   - **Patient View**:
     - Automatically transitions to form pending
   - **Doctor View**:
     - Shows waiting screen
     - Displays "Waiting for patient to submit form"

6. **FORM_PENDING**
   - **Patient View**:
     - Shows medical form screen
     - Collects patient medical information
     - Handles form submission
   - **Doctor View**:
     - Shows waiting screen
     - Displays "Waiting for patient to submit form"

7. **FORM_SUBMITTED**
   - **Patient View**:
     - Shows waiting screen
     - Displays "Waiting for doctor to join"
   - **Doctor View**:
     - Shows form review screen
     - Displays patient's submitted form
     - Button to proceed to session

8. **CALL_READY**
   - **Patient View**:
     - Shows preparing call screen
     - Displays "Preparing to join session"
   - **Doctor View**:
     - Shows call ready screen
     - Displays "Ready to join [session type]"
     - Button to join session

9. **CALL_STARTED**
   - **Patient View**:
     - For Call: Shows video call screen with Agora integration
     - For Chat: Shows chat interface
     - For Recommendation: Shows waiting screen for doctor's recommendation
   - **Doctor View**:
     - For Call: Shows video call screen with Agora integration
     - For Chat: Shows chat interface
     - For Recommendation: Shows recommendation input screen

10. **CALL_ENDED**
    - **Patient View**:
      - Shows call ended screen
      - Displays "Session has ended"
      - Button to return to home screen
    - **Doctor View**:
      - Shows call ended screen
      - Displays "Session has ended"
      - Button to return to home screen

## API Endpoints

### 1. Create Consultation Request
- **URL**: `/api/consultation/request/`
- **Method**: `POST`
- **Description**: Creates a new consultation request
- **Request Body**:
```json
{
    "patient_id": 1,
    "doctor_id": 2,
    "session_type": "Call"
}
```

### 2. Create Medical Questionnaire
- **URL**: `/api/questionnaires/`
- **Method**: `POST`
- **Description**: Creates a new medical questionnaire
- **Request Body**: [See full questionnaire fields in API documentation]

### 3. Status Update Endpoints
All status update endpoints follow the same pattern:
- **Method**: `PUT`
- **Headers**: `Content-Type: application/json`

#### Available Status Updates:
1. Accept Consultation: `/api/consultation/{id}/accept/`
2. Reject Consultation: `/api/consultation/{id}/reject/`
3. Set Payment Pending: `/api/consultation/{id}/paymentPending/`
4. Complete Payment: `/api/consultation/{id}/paymentCompleted/`
5. Set Form Pending: `/api/consultation/{id}/formPending/`
6. Submit Form: `/api/consultation/{id}/submit-form/`
7. Set Call Ready: `/api/consultation/{id}/callReady/`
8. Start Call: `/api/consultation/{id}/callStarted/`
9. End Call: `/api/consultation/{id}/callEnded/`

### 4. Current Consultation
- **URL**: `/api/consultation/current/{user_type}/{user_id}/`
- **Method**: `GET`
- **Description**: Gets the current active consultation for a user

## Flutter Implementation Notes

### Key Components
1. **State Management**
   - Use Provider or Bloc for state management
   - Maintain current pipeline state
   - Handle real-time updates

2. **UI Components**
   - Separate screens for each pipeline state
   - Responsive design for different screen sizes
   - Loading states and error handling

3. **Real-time Communication**
   - Agora SDK for video calls
   - WebSocket for chat functionality
   - Push notifications for status updates

### Implementation Considerations
1. **Error Handling**
   - Network errors
   - Payment failures
   - Form validation
   - State transition errors

2. **Security**
   - Secure storage of user credentials
   - Encrypted communication
   - Payment data protection

3. **Performance**
   - Efficient state updates
   - Image optimization
   - Caching strategies

## Testing

### API Testing
1. Test each endpoint with valid and invalid data
2. Verify state transitions
3. Check error handling
4. Validate response formats

### Flutter App Testing
1. Test each screen and state
2. Verify real-time communication
3. Test payment integration
4. Validate form submissions
5. Check navigation flows

## Deployment

### Backend
1. Set up production database
2. Configure security settings
3. Set up SSL certificates
4. Configure CORS

### Flutter App
1. Generate release builds
2. Configure app signing
3. Set up CI/CD pipeline
4. Configure app store listings

## Notes
- All timestamps are in UTC
- Status transitions are strictly enforced
- Each consultation can only be linked to one questionnaire
- A questionnaire can only be linked to one consultation
- Active consultations are those that haven't reached the CALL_ENDED state
- Real-time communication requires stable internet connection
- Payment processing requires secure environment
- Form data must be validated on both client and server 