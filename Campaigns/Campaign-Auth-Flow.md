# Campaign API Authentication Flow

## Ideal Authentication & API Flow

```mermaid
sequenceDiagram
    participant Script as Apps Script
    participant Auth as Auth Server<br/>staging.auth.curebase.com
    participant API as Campaigns API<br/>staging.campaigns.walgreens.curebase.com

    Note over Script: Configured with<br/>client_id + client_secret

    Script->>Auth: POST /api/v1/oauth/token
    Note right of Script: grant_type: client_credentials<br/>client_id: xxx<br/>client_secret: xxx

    Auth-->>Script: 200 OK
    Note left of Auth: access_token: eyJ...<br/>expires_in: 900<br/>token_type: Bearer

    Script->>API: POST /api/v1/recipients/bulk
    Note right of Script: Authorization: Bearer [token]<br/>Content-Type: application/json<br/>Body: [{recipient, journey}, ...]

    API-->>Script: 201 Created
    Note left of API: recipients: [id1, id2]<br/>journeys: [id1, id2]
```

## Request/Response Flow

```mermaid
flowchart TD
    subgraph step1 [Step 1: Get Token]
        A[Script starts] --> B[POST /oauth/token]
        B --> C{Response 200?}
        C -->|Yes| D[Extract access_token]
        C -->|No| E[Handle auth error]
    end

    subgraph step2 [Step 2: Call API]
        D --> F[Build request payload]
        F --> G["POST /recipients/bulk"]
        G --> H{Response 201?}
        H -->|Yes| I[Success - IDs returned]
        H -->|No| J[Handle API error]
    end
```

## Data Flow

```mermaid
flowchart LR
    subgraph input [Input]
        A[client_id]
        B[client_secret]
        C[Recipient Data]
        D[Campaign ID]
    end

    subgraph process [Process]
        E[Get Access Token]
        F[Format Request Body]
        G[POST to Bulk API]
    end

    subgraph output [Output]
        H[Recipient IDs]
        I[Journey IDs]
    end

    A --> E
    B --> E
    E --> G
    C --> F
    D --> F
    F --> G
    G --> H
    G --> I
```

---

## Required Credentials

| Item | Description | Where to Get |
|------|-------------|--------------|
| `client_id` | OAuth client identifier | Request from platform team |
| `client_secret` | OAuth client secret | Request from platform team |
| `campaignId` | Target campaign for journeys | From Campaigns UI or GET /api/v1/campaigns |

## API Endpoints

| Purpose | Method | URL |
|---------|--------|-----|
| Get Token | POST | `https://staging.auth.curebase.com/api/v1/oauth/token` |
| Bulk Recipients | POST | `https://staging.campaigns.walgreens.curebase.com/api/v1/recipients/bulk` |

## Request Body Schema (Bulk Recipients)

```json
[
  {
    "recipient": {
      "customerId": "required-external-id",
      "email": "user@example.com",
      "firstName": "First",
      "lastName": "Last",
      "phone": "+15551234567",
      "status": "ACTIVE",
      "tags": ["tag1", "tag2"],
      "communicationPreferences": {
        "optIn": true
      }
    },
    "journey": {
      "campaignId": "required-campaign-id",
      "status": "NOT_STARTED"
    }
  }
]
```

