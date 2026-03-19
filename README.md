# Project Management Tool

## Overview

This project is a simple team-based project management tool built using core Python.
It provides APIs to manage:

* Users
* Teams
* Project Boards
* Tasks within boards

All APIs accept and return JSON strings, making the system easy to test and extend.

---

## Design Approach

The problem focuses on implementing APIs using base classes and file-based storage.
To keep the solution clean and aligned with requirements:

* All APIs are implemented directly inside the provided base classes
* JSON files are used for persistence instead of a database
* A common utility is used for file operations
* Each method includes proper error handling using `try-except`

The goal was to keep the solution simple, readable, and maintainable without over-engineering.

---

## Project Structure

```id="2r7n7p"
projectManagement_App/
│
├── user_base.py              # User management APIs
├── team_base.py              # Team management APIs
├── project_board_base.py     # Board & task APIs
│
├── utils/
│   └── storage.py            # Common file read/write utility
│
├── db/                       # Local JSON storage (auto-created)
│   ├── users.json
│   ├── teams.json
│   ├── boards.json
│   └── tasks.json
│
├── out/                      # Exported board files (.txt)
│
└── main.py (optional)        # Test script to run APIs
```

---

## Features

### User Management

* Create user (unique name)
* List all users
* Get user details
* Update display name
* Get teams of a user

---

### Team Management

* Create team (unique name)
* Update team details
* Add users to team (max 50 at a time)
* Remove users from team
* List users in a team
* List all teams

---

### Project Board Management

* Create board (unique per team)
* Add tasks to board
* Update task status (OPEN / IN_PROGRESS / COMPLETE)
* Close board (only when all tasks are COMPLETE)
* List open boards for a team

---

### Export Feature

* Export a board into a `.txt` file
* Includes board details and task list in a readable format

---

## Data Storage

All data is stored locally using JSON files:

* `users.json`
* `teams.json`
* `boards.json`
* `tasks.json`

A common utility (`read_data`, `write_data`) is used to manage file operations.

---

## Error Handling

Each API is wrapped in `try-except` to ensure:

* The application does not crash
* Errors are returned in a consistent JSON format

Example:

```id="slq7st"
{
  "error": "User not found"
}
```

---

## Assumptions

* IDs are generated using UUID
* File storage is single-user (no concurrency handling)
* Input JSON is expected to be valid
* No authentication or authorization is implemented

---

## How to Run

1. Ensure Python is installed
2. Create a `db/` folder (or it will be auto-created)
3. Run APIs using a Python script

Example:

```python id="a4s1c4"
from user_base import UserBase
import json

user = UserBase()

response = user.create_user(json.dumps({
    "name": "john",
    "display_name": "John Doe"
}))

print(response)
```

---

## Future Improvements

* Add concurrency handling for file operations
* Convert APIs into REST services (Django/Flask)
* Use a database like PostgreSQL or SQLite
* Add authentication and role-based access

---

## Summary

This solution focuses on clean design, simplicity, and correctness.
It follows the given requirements closely while keeping the code modular and easy to understand.
