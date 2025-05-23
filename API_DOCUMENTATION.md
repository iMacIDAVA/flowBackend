# Consultation Platform API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently, all endpoints are accessible without authentication (`AllowAny` permission class).

## Common Response Formats

### Success Response
```json
{
    "status": "success",
    "message": "Operation successful message",
    "data": {
        // Response data object
    }
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Error description",
    "current_status": "Current status" // for status-related errors
}
```

## Endpoints

### 1. Create Consultation Request
Creates a new consultation request between a patient and doctor.

- **URL**: `/consultation/request/`
- **Method**: `POST`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
      "patient_id": 1,        // Required, integer
      "doctor_id": 2,         // Required, integer
      "session_type": "Call"  // Required, enum: ["Call", "Chat", "Recommendation"]
  }
  ```
- **Success Response** (201 Created):
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
- **Error Responses**:
  - 400 Bad Request:
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
  - 400 Bad Request (Active Consultation):
    ```json
    {
        "status": "error",
        "message": "An active consultation already exists between this patient and doctor",
        "pipeline_id": 5
    }
    ```

### 2. Create Medical Questionnaire
Creates a new medical questionnaire for a patient.

- **URL**: `/questionnaires/`
- **Method**: `POST`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
      "nume_si_prenume_reprezentant_legal": "John Doe",  // Required, string
      "nume_si_prenume": "Jane Doe",                     // Required, string
      "data_nastere": "2000-01-01",                      // Required, date (YYYY-MM-DD)
      "greutate": 70.5,                                  // Required, decimal
      "alergic_la_vreun_medicament": false,              // Required, boolean
      "la_ce_medicament_este_alergic": "Penicillin",     // Optional, string
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
- **Success Response** (201 Created):
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

### 3. Status Update Endpoints
All status update endpoints follow the same pattern.

- **Method**: `PUT`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **URL Pattern**: `/consultation/{id}/{action}/`
- **Path Parameters**:
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

#### Special Case: Form Submission
- **URL**: `/consultation/{id}/submit-form/`
- **Request Body**:
  ```json
  {
      "questionnaire_id": 2  // Required, integer
  }
  ```

- **Success Response** (200 OK):
  ```json
  {
      "status": "success",
      "message": "Status updated to {new_status}",
      "data": {
          "id": 1,
          "status": "new_status",
          // Other consultation details
      }
  }
  ```

- **Error Responses**:
  - 400 Bad Request (Invalid Action):
    ```json
    {
        "status": "error",
        "message": "Invalid action: {action}. Valid actions are: [accept, reject, paymentPending, paymentCompleted, formPending, callReady, callStarted, callEnded]"
    }
    ```
  - 400 Bad Request (Invalid Transition):
    ```json
    {
        "status": "error",
        "message": "Cannot transition from {current_status} to {new_status}. Valid transitions are: {valid_transitions}",
        "current_status": "current_status"
    }
    ```
  - 404 Not Found:
    ```json
    {
        "status": "error",
        "message": "Consultation not found"
    }
    ```

### 4. Current Consultation
Gets the current active consultation for a user.

- **URL**: `/consultation/current/{user_type}/{user_id}/`
- **Method**: `GET`
- **Path Parameters**:
  - `user_type`: Either "patient" or "doctor" (string)
  - `user_id`: User ID (integer)
- **Success Response** (200 OK):
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
          // Other consultation details
      }
  }
  ```
- **No Active Session Response** (200 OK):
  ```json
  {
      "status": "success",
      "has_active_session": false,
      "message": "No active consultation found"
  }
  ```
- **Error Responses**:
  - 400 Bad Request:
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

## Notes
1. All timestamps are in UTC
2. Status transitions are strictly enforced
3. Each consultation can only be linked to one questionnaire
4. A questionnaire can only be linked to one consultation
5. Active consultations are those that haven't reached the CALL_ENDED state
6. The API returns 200 OK for successful operations, even when no active session is found
7. All error responses include a descriptive message
8. Status-related errors include the current status in the response 