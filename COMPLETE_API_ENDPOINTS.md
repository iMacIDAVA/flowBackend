# Complete API Endpoints Documentation

## Database Tables

### 1. VideoCallPipeline
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
```

### 2. MedicalQuestionnaire
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
- **URL**: `POST /api/consultation/request/`
- **Description**: Creates a new consultation request
- **Input**:
```json
{
    "patient_id": 1,        // Required, integer
    "doctor_id": 2,         // Required, integer
    "session_type": "Call"  // Required, enum: ["Call", "Chat", "Recommendation"]
}
```
- **Success Output** (201):
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

### 2. Accept Consultation
- **URL**: `PUT /api/consultation/{id}/accept/`
- **Description**: Doctor accepts a consultation request
- **Input**: None (empty body)
- **Success Output** (200):
```json
{
    "status": "success",
    "message": "Status updated to Accepted",
    "data": {
        "id": 1,
        "status": "Accepted",
        // Other consultation details
    }
}
```

### 3. Reject Consultation
- **URL**: `PUT /api/consultation/{id}/reject/`
- **Description**: Doctor rejects a consultation request
- **Input**: None (empty body)
- **Success Output** (200):
```json
{
    "status": "success",
    "message": "Status updated to Rejected",
    "data": {
        "id": 1,
        "status": "Rejected",
        // Other consultation details
    }
}
```

### 4. Update Payment Status
- **URL**: `PUT /api/consultation/{id}/paymentPending/`
- **Description**: Updates consultation to payment pending state
- **Input**: None (empty body)
- **Success Output** (200):
```json
{
    "status": "success",
    "message": "Status updated to PaymentPending",
    "data": {
        "id": 1,
        "status": "PaymentPending",
        // Other consultation details
    }
}
```

### 5. Complete Payment
- **URL**: `PUT /api/consultation/{id}/paymentCompleted/`
- **Description**: Marks payment as completed
- **Input**: None (empty body)
- **Success Output** (200):
```json
{
    "status": "success",
    "message": "Status updated to PaymentCompleted",
    "data": {
        "id": 1,
        "status": "PaymentCompleted",
        "payment_completed_at": "2024-03-22T10:00:00Z",
        // Other consultation details
    }
}
```

### 6. Create Medical Questionnaire
- **URL**: `POST /api/questionnaires/`
- **Description**: Creates a new medical questionnaire
- **Input**:
```json
{
    "nume_si_prenume_reprezentant_legal": "John Doe",
    "nume_si_prenume": "Jane Doe",
    "data_nastere": "2000-01-01",
    "greutate": 70.5,
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
    "rinoree": false
}
```
- **Success Output** (201):
```json
{
    "status": "success",
    "message": "Questionnaire created successfully",
    "data": {
        "id": 1,
        // All questionnaire fields
        "created_at": "2024-03-22T10:00:00Z"
    }
}
```

### 7. Submit Form
- **URL**: `PUT /api/consultation/{id}/submit-form/`
- **Description**: Links a questionnaire to a consultation
- **Input**:
```json
{
    "questionnaire_id": 2  // Required, integer
}
```
- **Success Output** (200):
```json
{
    "status": "success",
    "message": "Form submitted successfully",
    "data": {
        "id": 1,
        "status": "FormSubmitted",
        "questionnaire": {
            // Questionnaire details
        },
        "form_submitted_at": "2024-03-22T10:00:00Z"
    }
}
```

### 8. Ready for Call
- **URL**: `PUT /api/consultation/{id}/callReady/`
- **Description**: Marks consultation as ready for call
- **Input**: None (empty body)
- **Success Output** (200):
```json
{
    "status": "success",
    "message": "Status updated to CallReady",
    "data": {
        "id": 1,
        "status": "CallReady",
        // Other consultation details
    }
}
```

### 9. Start Call
- **URL**: `PUT /api/consultation/{id}/callStarted/`
- **Description**: Marks consultation as started
- **Input**: None (empty body)
- **Success Output** (200):
```json
{
    "status": "success",
    "message": "Status updated to CallStarted",
    "data": {
        "id": 1,
        "status": "CallStarted",
        "call_started_at": "2024-03-22T10:00:00Z",
        // Other consultation details
    }
}
```

### 10. End Call
- **URL**: `PUT /api/consultation/{id}/callEnded/`
- **Description**: Marks consultation as ended
- **Input**: None (empty body)
- **Success Output** (200):
```json
{
    "status": "success",
    "message": "Status updated to CallEnded",
    "data": {
        "id": 1,
        "status": "CallEnded",
        "call_ended_at": "2024-03-22T10:00:00Z",
        // Other consultation details
    }
}
```

## Common Error Responses

### 1. Validation Error (400)
```json
{
    "status": "error",
    "message": "Validation failed",
    "errors": {
        "field_name": ["Error message"]
    }
}
```

### 2. Invalid Status Transition (400)
```json
{
    "status": "error",
    "message": "Cannot transition from {current_status} to {new_status}",
    "current_status": "current_status"
}
```

### 3. Not Found (404)
```json
{
    "status": "error",
    "message": "Resource not found"
}
```

### 4. Server Error (500)
```json
{
    "status": "error",
    "message": "An unexpected error occurred",
    "error": "Error details"
}
```

## Status Flow
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

## Important Notes

1. **Authentication**
   - Currently, all endpoints are accessible without authentication
   - Future versions will implement authentication

2. **Timestamps**
   - All timestamps are in UTC
   - Special timestamps are set automatically when status changes

3. **Status Transitions**
   - Strictly enforced
   - Invalid transitions return 400 Bad Request
   - Current status included in error responses

4. **Questionnaire Rules**
   - One-to-one relationship with consultations
   - Can only be submitted in FORM_PENDING state

5. **Active Consultations**
   - Defined as those not in CALL_ENDED state
   - Returns 200 OK even when no active session found 