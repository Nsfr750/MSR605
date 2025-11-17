# MSR605 Card Reader/Writer API Reference

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
  - [Card Operations](#card-operations)
  - [Template Management](#template-management)
  - [Batch Processing](#batch-processing)
  - [Device Management](#device-management)
- [Error Handling](#error-handling)
- [WebSocket API](#websocket-api)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)
  - [Python Client](#python-client)
  - [cURL Examples](#curl-examples)
- [Webhooks](#webhooks)
- [Troubleshooting](#troubleshooting)
- [CI/CD Integration (v2.4.5+)](#ci-cd-integration-v245)

## Overview

The MSR605 API provides a RESTful interface for interacting with the MSR605 Card Reader/Writer. The API allows you to:

- Read data from magnetic stripe cards
- Write data to magnetic stripe cards
- Manage card templates
- Process batch operations
- Monitor device status
- Handle real-time events

**Base URL**: `http://localhost:8000/api`
**Content-Type**: `application/json`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the `Authorization` header:

```http
Authorization: Bearer your_jwt_token_here
```

### Obtaining a Token

```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=admin&password=your_password
```

**Response**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## API Endpoints

### Card Operations

#### Read Card Data

```http
POST /api/card/read
Authorization: Bearer your_jwt_token_here
Content-Type: application/json

{
  "detect_format": true,
  "validate": true
}
```

**Parameters**

- `detect_format` (boolean): Auto-detect card format (default: true)
- `validate` (boolean): Validate card data (default: true)

**Response**

```json
{
  "tracks": [
    "%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?",
    ";1234567890123456=24011234567890123456?",
    ""
  ],
  "format": "ISO_7813",
  "valid": true,
  "validation_errors": {},
  "parsed": {
    "track1": {
      "primary_account_number": "1234567890123456",
      "name": "CARDHOLDER/NAME",
      "expiration_date": "2401",
      "service_code": "123",
      "discretionary_data": "4567890123456789"
    },
    "track2": {
      "primary_account_number": "1234567890123456",
      "expiration_date": "2401",
      "service_code": "123",
      "discretionary_data": "4567890123456789"
    },
    "track3": {}
  }
}
```

#### Write Card Data

```http
POST /api/card/write
Authorization: Bearer your_jwt_token_here
Content-Type: application/json

{
  "tracks": [
    "%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?",
    ";1234567890123456=24011234567890123456?",
    ""
  ],
  "format": "ISO_7813"
}
```

**Parameters**

- `tracks` (array): Array of track data (up to 3 tracks)
- `format` (string): Card format (e.g., "ISO_7813", "ISO_7811", "AAMVA")

**Response**

```json
{
  "success": true,
  "message": "Card written successfully",
  "tracks_written": 2,
  "format": "ISO_7813"
}
```

### Template Management

#### List Templates

```http
GET /api/templates
Authorization: Bearer your_jwt_token_here
```

**Response**

```json
{
  "templates": [
    {
      "name": "loyalty_card",
      "description": "Standard loyalty card format",
      "format": "ISO_7813",
      "created_at": "2023-11-17T15:30:00Z"
    },
    {
      "name": "access_control",
      "description": "Office access control card",
      "format": "ISO_7811",
      "created_at": "2023-11-16T10:15:00Z"
    }
  ]
}
```

#### Create Template

```http
POST /api/templates
Authorization: Bearer your_jwt_token_here
Content-Type: application/json

{
  "name": "new_template",
  "description": "New card template",
  "tracks": [
    "%B[PAN]^[NAME]^[YYMM][SERVICE]?",
    ";[PAN]=[YYMM][SERVICE]?",
    ""
  ],
  "format": "ISO_7813",
  "metadata": {
    "fields": {
      "PAN": {
        "type": "string",
        "required": true,
        "description": "Primary Account Number"
      },
      "NAME": {
        "type": "string",
        "required": true,
        "max_length": 26
      },
      "YYMM": {
        "type": "date",
        "format": "YYMM",
        "required": true
      },
      "SERVICE": {
        "type": "string",
        "default": "101"
      }
    }
  }
}
```

**Response**

```json
{
  "success": true,
  "message": "Template created successfully",
  "template": {
    "name": "new_template",
    "description": "New card template",
    "format": "ISO_7813",
    "created_at": "2023-11-17T16:45:00Z"
  }
}
```

### Batch Processing

#### Process Batch

```http
POST /api/batch
Authorization: Bearer your_jwt_token_here
Content-Type: application/json

{
  "operations": [
    {
      "type": "read",
      "id": "op1",
      "params": {
        "detect_format": true,
        "validate": true
      }
    },
    {
      "type": "write",
      "id": "op2",
      "params": {
        "template": "loyalty_card",
        "values": {
          "PAN": "9876543210987654",
          "NAME": "JOHN DOE",
          "YYMM": "2512"
        }
      },
      "depends_on": ["op1"]
    }
  ]
}
```

**Response**

```json
{
  "batch_id": "batch_12345",
  "status": "completed",
  "results": [
    {
      "operation_id": "op1",
      "status": "completed",
      "result": {
        "tracks": ["..."],
        "format": "ISO_7813",
        "valid": true
      }
    },
    {
      "operation_id": "op2",
      "status": "completed",
      "result": {
        "success": true,
        "message": "Card written successfully"
      }
    }
  ]
}
```

### Device Management

#### Get Device Status

```http
GET /api/device/status
Authorization: Bearer your_jwt_token_here
```

**Response**

```json
{
  "device": "MSR605",
  "firmware_version": "1.2.3",
  "status": "ready",
  "connected": true,
  "last_error": null,
  "battery_level": 85,
  "storage": {
    "total": 1048576,
    "used": 262144,
    "free": 786432
  },
  "uptime": 3600
}
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "invalid_request",
    "message": "Invalid request parameters",
    "details": {
      "field": "tracks",
      "issue": "required"
    },
    "request_id": "req_12345",
    "timestamp": "2023-11-17T17:30:00Z"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `invalid_request` | 400 | Invalid request parameters |
| `authentication_required` | 401 | Authentication required |
| `invalid_token` | 401 | Invalid or expired token |
| `insufficient_permissions` | 403 | Insufficient permissions |
| `device_busy` | 423 | Device is busy with another operation |
| `device_error` | 500 | Device communication error |
| `internal_error` | 500 | Internal server error |

## WebSocket API

For real-time notifications and events, connect to the WebSocket endpoint:

```
ws://localhost:8000/ws
```

### Events

#### Card Swipe Event

```json
{
  "event": "card_swipe",
  "timestamp": "2023-11-17T18:00:00Z",
  "data": {
    "tracks": ["..."],
    "format": "ISO_7813"
  }
}
```

#### Device Status Update

```json
{
  "event": "device_status",
  "timestamp": "2023-11-17T18:01:00Z",
  "data": {
    "status": "ready",
    "battery_level": 85
  }
}
```

## Rate Limiting

- **Rate Limit**: 100 requests per minute per IP

- **Headers**:

  - `X-RateLimit-Limit`: Request limit per time window
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Time when the limit resets (UTC timestamp)

## Examples

### Python Client

```python
import requests
from requests.auth import HTTPBasicAuth

class MSR605Client:
    def __init__(self, base_url="http://localhost:8000", username="admin", password="password"):
        self.base_url = base_url
        self.token = self._authenticate(username, password)
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def _authenticate(self, username, password):
        response = requests.post(
            f"{self.base_url}/token",
            data={"username": username, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        return response.json()["access_token"]
    
    def read_card(self, detect_format=True, validate=True):
        response = requests.post(
            f"{self.base_url}/api/card/read",
            json={"detect_format": detect_format, "validate": validate},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def write_card(self, tracks, card_format=None):
        data = {"tracks": tracks}
        if card_format:
            data["format"] = card_format
            
        response = requests.post(
            f"{self.base_url}/api/card/write",
            json=data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Example usage
if __name__ == "__main__":
    client = MSR605Client(username="admin", password="your_password")
    
    # Read a card
    card_data = client.read_card()
    print(f"Read card: {card_data['format']}")
    
    # Write to a card
    tracks = [
        "%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?",
        ";1234567890123456=24011234567890123456?",
        ""
    ]
    result = client.write_card(tracks, "ISO_7813")
    print(f"Write result: {result['message']}")
```

### cURL Examples

#### Read Card

```bash
curl -X POST http://localhost:8000/api/card/read \
  -H "Authorization: Bearer your_jwt_token_here" \
  -H "Content-Type: application/json" \
  -d '{"detect_format": true, "validate": true}'
```

#### Write Card

```bash
curl -X POST http://localhost:8000/api/card/write \
  -H "Authorization: Bearer your_jwt_token_here" \
  -H "Content-Type: application/json" \
  -d '{"tracks": ["%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?", ";1234567890123456=24011234567890123456?", ""], "format": "ISO_7813"}'
```

## Webhooks

Configure webhooks to receive real-time notifications for card events:

```http
POST /api/webhooks
Authorization: Bearer your_jwt_token_here
Content-Type: application/json

{
  "url": "https://your-server.com/webhook/msr605",
  "events": ["card_swipe", "write_complete", "error"],
  "secret": "your_webhook_secret"
}
```

## CI/CD Integration (v2.4.5+)

### Overview
The MSR605 project now includes a comprehensive CI/CD pipeline using GitHub Actions, enabling automated testing, building, and deployment.

### Key Features
- **Automated Testing**
  - Runs on every push and pull request
  - Tests across Python 3.8, 3.9, and 3.10
  - Code coverage reporting via Codecov

- **Automated Builds**
  - Windows executable generation
  - Version-based artifact naming
  - Build artifact retention

- **Release Management**
  - Automatic release creation on version tags
  - Release notes generation
  - Pre-release support

### Workflow Configuration
The pipeline is configured in `.github/workflows/ci-cd.yml` and includes three main jobs:

1. **Test Job**
   - Runs unit and integration tests
   - Generates code coverage reports
   - Enforces code quality checks

2. **Build Job**
   - Creates Windows executables using PyInstaller
   - Handles version information and assets
   - Uploads build artifacts

3. **Release Job**
   - Triggers on version tags (v*.*.*)
   - Creates GitHub releases
   - Attaches build artifacts

### Local Development
To run the same checks locally:

```bash
# Run tests
pytest tests/ --cov=msr605 --cov-report=xml

# Build executable
pyinstaller --onefile --name MSR605 --icon=assets/icon.ico main.py
```

### Monitoring
- **Build Status**: [GitHub Actions](https://github.com/Nsfr750/MSR605/actions)
- **Code Coverage**: [Codecov](https://codecov.io/gh/Nsfr750/MSR605)
- **Releases**: [GitHub Releases](https://github.com/Nsfr750/MSR605/releases)

### Best Practices
1. Always create feature branches for new development
2. Open pull requests for code review
3. Ensure all tests pass before merging to main
4. Use semantic versioning for releases
5. Check build status before merging PRs

## Troubleshooting

### Common Issues

1. **Device Not Found**

   - Ensure the MSR605 is properly connected
   - Check device permissions
   - Restart the service

2. **Authentication Failures**

   - Verify username/password
   - Check token expiration
   - Ensure proper Authorization header format

3. **Card Read/Write Errors**

   - Clean the card reader head
   - Ensure proper card orientation
   - Check card format compatibility

## CI/CD Pipeline Setup

The MSR605 API includes built-in support for CI/CD pipelines to enable automated testing and deployment. This section outlines the recommended pipeline configuration.

### GitHub Actions Workflow

```yaml
name: MSR605 API CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      redis:
        image: redis
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
        pip install -e .
        
    - name: Run tests
      run: |
        pytest tests/ --cov=msr605 --cov-report=xml
      env:
        TESTING: "true"

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Add your deployment commands here
        # For example:
        # scp -r . user@production:/opt/msr605
        # ssh user@production "cd /opt/msr605 && docker-compose up -d --build"
      env:
        DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}