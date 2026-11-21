# Smart Service Desk Management System

## Notice
Resolve Request is restricted to admin only.

- Menu option 4 is marked as admin-only.
- To resolve a ticket/request, login is required with:
  - Username: admin
  - Password: admin

## Overview
This project is a command-line Smart Service Desk system built with layered architecture.
It allows users to create, view, search, and resolve service requests (tickets), with data persisted in a JSON file.

## Features
- Create a new service request.
- View all service requests.
- Search a request by Request ID.
- Resolve a request (admin-only).
- Input validation for menu, request ID, and priority.
- Custom exceptions for business and input errors.
- File-based persistence using JSON.

## Menu
When you run the app, you get the following options:

1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request (for admin only)
5. Exit

## Admin-Only Resolve Flow
When option 4 is selected:
1. App asks for admin username.
2. App asks for admin password.
3. If credentials are not admin/admin, access is denied.
4. If credentials are valid, request resolution continues.

## Project Structure
```text
fractal-fs-assignment3/
|-- main.py
|-- README.md
|-- application/
|   `-- request_service.py
|-- data/
|   `-- requests.json
|-- domain/
|   |-- exceptions.py
|   `-- service_request.py
`-- infrastructure/
    `-- file_repository.py
```

## Layered Architecture
- Domain layer:
  - Contains core business model and rules.
  - File: domain/service_request.py
- Application layer:
  - Contains use-case orchestration and request workflows.
  - File: application/request_service.py
- Infrastructure layer:
  - Handles JSON storage and file operations.
  - File: infrastructure/file_repository.py
- Interface layer (CLI):
  - User interaction and menu handling.
  - File: main.py

## Business Rules
- Priority must be one of: LOW, MEDIUM, HIGH.
- Status can be OPEN or RESOLVED.
- A request already marked RESOLVED cannot be resolved again.
- Request ID must be a positive number when searching/resolving.

## Custom Exceptions
Defined in domain/exceptions.py:
- DuplicateRequestIdError
- RequestNotFoundError
- InvalidPriorityError
- RequestAlreadyResolvedError
- InvalidMenuChoiceError

## Data Persistence
- All requests are saved in data/requests.json.
- On app startup, existing requests are loaded from the same file.
- Changes are persisted immediately after create/resolve actions.

## How To Run
1. Open terminal in the project root.
2. Run:

```bash
python main.py
```

If your system uses python3, run:

```bash
python3 main.py
```

## Example Usage
```text
===SMART SERVICE DESK SYSTEM===
1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request (for admin only)
5. Exit
```

## Tech Stack
- Python 3
- JSON file storage
- Object-oriented design

## Repository Notes
- Branch-based workflow was used during development.
- Feature changes were merged into development, then into main.
