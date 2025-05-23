# Detailed Consultation Platform API Documentation

## Database Schema

### 1. VideoCallPipeline Table
```sql
CREATE TABLE consultation_videocallpipeline (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    patient_id INTEGER NOT NULL DEFAULT 0,
    doctor_id INTEGER NOT NULL DEFAULT 0,
    channel_name VARCHAR(100) NOT NULL,
    session_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Requested',
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    questionnaire_id BIGINT NULL,
    payment_completed_at DATETIME NULL,
    form_submitted_at DATETIME NULL,
    call_started_at DATETIME NULL,
    call_ended_at DATETIME NULL,
    FOREIGN KEY (questionnaire_id) REFERENCES consultation_medicalquestionnaire(id)
);

-- Indexes
CREATE INDEX idx_patient_id ON consultation_videocallpipeline(patient_id);
CREATE INDEX idx_doctor_id ON consultation_videocallpipeline(doctor_id);
CREATE INDEX idx_status ON consultation_videocallpipeline(status);
CREATE INDEX idx_session_type ON consultation_videocallpipeline(session_type);
```

### 2. MedicalQuestionnaire Table
```sql
CREATE TABLE consultation_medicalquestionnaire (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nume_si_prenume_reprezentant_legal VARCHAR(255) NOT NULL,
    nume_si_prenume VARCHAR(255) NOT NULL,
    data_nastere DATE NOT NULL,
    greutate DECIMAL(5,2) NOT NULL,
    alergic_la_vreun_medicament BOOLEAN NOT NULL DEFAULT FALSE,
    la_ce_medicament_este_alergic VARCHAR(255) NULL,
    febra BOOLEAN NOT NULL DEFAULT FALSE,
    tuse BOOLEAN NOT NULL DEFAULT FALSE,
    dificultati_respiratorii BOOLEAN NOT NULL DEFAULT FALSE,
    astenie BOOLEAN NOT NULL DEFAULT FALSE,
    cefalee BOOLEAN NOT NULL DEFAULT FALSE,
    dureri_in_gat BOOLEAN NOT NULL DEFAULT FALSE,
    greturi_varsaturi BOOLEAN NOT NULL DEFAULT FALSE,
    diaree_constipatie BOOLEAN NOT NULL DEFAULT FALSE,
    refuzul_alimentatie BOOLEAN NOT NULL DEFAULT FALSE,
    iritatii_piele BOOLEAN NOT NULL DEFAULT FALSE,
    nas_infundat BOOLEAN NOT NULL DEFAULT FALSE,
    rinoree BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL
);
```

## API Endpoints

### 1. Create Consultation Request
Creates a new consultation request between a patient and doctor.

#### Endpoint
```
POST /api/consultation/request/
```

#### Headers
```
Content-Type: application/json
```

#### Request Body
```json
{
    "patient_id": 1,        // Required, integer
    "doctor_id": 2,         // Required, integer
    "session_type": "Call"  // Required, enum: ["Call", "Chat", "Recommendation"]
}
```

#### Success Response (201 Created)
```json
{
    "status": "success",
    "message": "Consultation request created successfully",
    "data": {
        "id": 1,
        "patient_id": 1,
        "doctor_id": 2,
        "session_type": "Call",
        "status": "Requested",
        "channel_name": "uuid-string",
        "created_at": "2024-03-22T10:00:00Z",
        "updated_at": "2024-03-22T10:00:00Z"
    }
}
```

#### Error Responses

1. Missing Required Fields (400 Bad Request)
```json
{
    "status": "error",
    "message": "Validation failed",
    "errors": {
        "patient_id": ["This field is required"],
        "doctor_id": ["This field is required"],
        "session_type": ["This field is required"]
    }
}
```

2. Invalid Session Type (400 Bad Request)
```json
{
    "status": "error",
    "message": "Validation failed",
    "errors": {
        "session_type": ["Invalid choice. Valid choices are: Call, Chat, Recommendation"]
    }
}
```

3. Active Consultation Exists (400 Bad Request)
```json
{
    "status": "error",
    "message": "An active consultation already exists between this patient and doctor",
    "pipeline_id": 5
}
```

4. Server Error (500 Internal Server Error)
```json
{
    "status": "error",
    "message": "An unexpected error occurred",
    "error": "Error details"
}
```

### 2. Create Medical Questionnaire
Creates a new medical questionnaire for a patient.

#### Endpoint
```
POST /api/questionnaires/
```

#### Headers
```
Content-Type: application/json
```

#### Request Body
```json
{
    "nume_si_prenume_reprezentant_legal": "John Doe",  // Required, string, max_length=255
    "nume_si_prenume": "Jane Doe",                     // Required, string, max_length=255
    "data_nastere": "2000-01-01",                      // Required, date (YYYY-MM-DD)
    "greutate": 70.5,                                  // Required, decimal(5,2)
    "alergic_la_vreun_medicament": false,              // Required, boolean
    "la_ce_medicament_este_alergic": "Penicillin",     // Optional, string, max_length=255
    "febra": false,                                    // Required, boolean
    "tuse": false,                                     // Required, boolean
    "dificultati_respiratorii": false,                 // Required, boolean
    "astenie": false,                                  // Required, boolean
    "cefalee": false,                                  // Required, boolean
    "dureri_in_gat": false,                            // Required, boolean
    "greturi_varsaturi": false,                        // Required, boolean
    "diaree_constipatie": false,                       // Required, boolean
    "refuzul_alimentatie": false,                      // Required, boolean
    "iritatii_piele": false,                           // Required, boolean
    "nas_infundat": false,                             // Required, boolean
    "rinoree": false                                   // Required, boolean
}
```

#### Success Response (201 Created)
```json
{
    "status": "success",
    "message": "Questionnaire created successfully",
    "data": {
        "id": 1,
        "nume_si_prenume_reprezentant_legal": "John Doe",
        "nume_si_prenume": "Jane Doe",
        "data_nastere": "2000-01-01",
        "greutate": "70.50",
        "alergic_la_vreun_medicament": false,
        "la_ce_medicament_este_alergic": "Penicillin",
        "febra": false,
        "tuse": false,
        "dificultati_respiratorii": false,
        "astenie": false,
        "cefalee": false,
        "dureri_in_gat": false,
        "greturi_varsaturi": false,
        "diaree_constipatie": false,
        "refuzul_alimentatie": false,
        "iritatii_piele": false,
        "nas_infundat": false,
        "rinoree": false,
        "created_at": "2024-03-22T10:00:00Z"
    }
}
```

#### Error Responses

1. Missing Required Fields (400 Bad Request)
```json
{
    "status": "error",
    "message": "Validation failed",
    "errors": {
        "nume_si_prenume_reprezentant_legal": ["This field is required"],
        "nume_si_prenume": ["This field is required"],
        "data_nastere": ["This field is required"],
        "greutate": ["This field is required"]
    }
}
```

2. Invalid Date Format (400 Bad Request)
```json
{
    "status": "error",
    "message": "Validation failed",
    "errors": {
        "data_nastere": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD"]
    }
}
```

3. Invalid Decimal Value (400 Bad Request)
```json
{
    "status": "error",
    "message": "Validation failed",
    "errors": {
        "greutate": ["A valid number is required"]
    }
}
```

### 3. Status Update Endpoints
Updates the status of a consultation.

#### Endpoint
```
PUT /api/consultation/{id}/{action}/
```

#### Path Parameters
- `id`: Consultation ID (integer)
- `action`: One of the following:
  - `accept`
  - `reject`
  - `paymentPending`
  - `paymentCompleted`
  - `formPending`
  - `callReady`
  - `callStarted`
  - `callEnded`

#### Headers
```
Content-Type: application/json
```

#### Success Response (200 OK)
```json
{
    "status": "success",
    "message": "Status updated to {new_status}",
    "data": {
        "id": 1,
        "patient_id": 1,
        "doctor_id": 2,
        "session_type": "Call",
        "status": "new_status",
        "channel_name": "uuid-string",
        "created_at": "2024-03-22T10:00:00Z",
        "updated_at": "2024-03-22T10:00:00Z"
    }
}
```

#### Error Responses

1. Invalid Action (400 Bad Request)
```json
{
    "status": "error",
    "message": "Invalid action: {action}. Valid actions are: [accept, reject, paymentPending, paymentCompleted, formPending, callReady, callStarted, callEnded]"
}
```

2. Invalid Status Transition (400 Bad Request)
```json
{
    "status": "error",
    "message": "Cannot transition from {current_status} to {new_status}. Valid transitions are: {valid_transitions}",
    "current_status": "current_status"
}
```

3. Consultation Not Found (404 Not Found)
```json
{
    "status": "error",
    "message": "Consultation not found"
}
```

### 4. Form Submission
Submits a medical questionnaire for a consultation.

#### Endpoint
```
PUT /api/consultation/{id}/submit-form/
```

#### Path Parameters
- `id`: Consultation ID (integer)

#### Headers
```
Content-Type: application/json
```

#### Request Body
```json
{
    "questionnaire_id": 2  // Required, integer
}
```

#### Success Response (200 OK)
```json
{
    "status": "success",
    "message": "Form submitted successfully",
    "data": {
        "id": 1,
        "patient_id": 1,
        "doctor_id": 2,
        "session_type": "Call",
        "status": "FormSubmitted",
        "channel_name": "uuid-string",
        "questionnaire": {
            // Questionnaire details
        },
        "form_submitted_at": "2024-03-22T10:00:00Z",
        "created_at": "2024-03-22T10:00:00Z",
        "updated_at": "2024-03-22T10:00:00Z"
    }
}
```

#### Error Responses

1. Missing Questionnaire ID (400 Bad Request)
```json
{
    "status": "error",
    "message": "questionnaire_id is required"
}
```

2. Invalid Consultation State (400 Bad Request)
```json
{
    "status": "error",
    "message": "Form can only be submitted when consultation is in FormPending state",
    "current_status": "current_status"
}
```

3. Questionnaire Not Found (404 Not Found)
```json
{
    "status": "error",
    "message": "Questionnaire with ID {id} does not exist"
}
```

4. Questionnaire Already Linked (400 Bad Request)
```json
{
    "status": "error",
    "message": "This questionnaire is already linked to consultation ID {id}"
}
```

### 5. Current Consultation
Gets the current active consultation for a user.

#### Endpoint
```
GET /api/consultation/current/{user_type}/{user_id}/
```

#### Path Parameters
- `user_type`: Either "patient" or "doctor" (string)
- `user_id`: User ID (integer)

#### Success Response (200 OK)
```json
{
    "status": "success",
    "has_active_session": true,
    "data": {
        "id": 1,
        "patient_id": 1,
        "doctor_id": 2,
        "session_type": "Call",
        "status": "Requested",
        "channel_name": "uuid-string",
        "created_at": "2024-03-22T10:00:00Z",
        "updated_at": "2024-03-22T10:00:00Z"
    }
}
```

#### No Active Session Response (200 OK)
```json
{
    "status": "success",
    "has_active_session": false,
    "message": "No active consultation found"
}
```

#### Error Responses

1. Invalid User Type (400 Bad Request)
```json
{
    "status": "error",
    "message": "Invalid user type. Must be either patient or doctor"
}
```

## Status Transition Rules

### Valid State Transitions
```
REQUESTED → ACCEPTED/REJECTED
ACCEPTED → PAYMENT_PENDING
PAYMENT_PENDING → PAYMENT_COMPLETED
PAYMENT_COMPLETED → FORM_PENDING
FORM_PENDING → FORM_SUBMITTED
FORM_SUBMITTED → CALL_READY
CALL_READY → CALL_STARTED
CALL_STARTED → CALL_ENDED
```

### End States
- `REJECTED`
- `CALL_ENDED`

## Important Notes

1. **Timestamps**
   - All timestamps are in UTC
   - `created_at` and `updated_at` are automatically managed
   - Special timestamps (`payment_completed_at`, `form_submitted_at`, `call_started_at`, `call_ended_at`) are set when their respective statuses are reached

2. **Status Transitions**
   - Status transitions are strictly enforced
   - Invalid transitions will return a 400 Bad Request
   - The current status is included in error responses

3. **Questionnaire Rules**
   - Each consultation can only be linked to one questionnaire
   - A questionnaire can only be linked to one consultation
   - Questionnaire submission is only allowed in the `FORM_PENDING` state

4. **Active Consultations**
   - Active consultations are those that haven't reached the `CALL_ENDED` state
   - The API returns 200 OK for successful operations, even when no active session is found

5. **Error Handling**
   - All error responses include a descriptive message
   - Status-related errors include the current status in the response
   - Validation errors include specific field errors

6. **Database Constraints**
   - Foreign key constraints ensure data integrity
   - Indexes optimize query performance
   - Default values are provided for required fields

7. **Security**
   - Currently, all endpoints are accessible without authentication
   - Future versions may implement authentication and authorization 