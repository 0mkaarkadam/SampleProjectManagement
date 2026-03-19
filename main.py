import json
from user_base import UserBase
from team_base import TeamBase
from project_board_base import ProjectBoardBase

user_api = UserBase()
team_api = TeamBase()
board_api = ProjectBoardBase()


# 🔹 1. Create User
u1 = json.loads(user_api.create_user(json.dumps({
    "name": "john",
    "display_name": "John Doe"
})))

print("User:", u1)


# 🔹 2. Create Team
t1 = json.loads(team_api.create_team(json.dumps({
    "name": "Backend Team",
    "description": "Handles APIs",
    "admin": u1["id"]
})))

print("Team:", t1)


# 🔹 3. Create Board
b1 = json.loads(board_api.create_board(json.dumps({
    "name": "Sprint 1",
    "description": "Initial sprint",
    "team_id": t1["id"],
    "creation_time": "2026-03-19T10:00:00"
})))

print("Board:", b1)


# 🔹 4. Add Task
task1 = json.loads(board_api.add_task(json.dumps({
    "title": "Build API",
    "description": "Create user APIs",
    "board_id": b1["id"],
    "user_id": u1["id"],
    "creation_time": "2026-03-19T11:00:00"
})))

print("Task:", task1)


# 🔹 5. Update Task Status → COMPLETE
print(board_api.update_task_status(json.dumps({
    "id": task1["id"],
    "status": "COMPLETE"
})))


# 🔹 6. Close Board (only works if all tasks COMPLETE)
print(board_api.close_board(json.dumps({
    "id": b1["id"]
})))


# 🔹 7. Export Board (THIS CREATES FILE IN out/)
export_response = json.loads(board_api.export_board(json.dumps({
    "id": b1["id"]
})))

print("Export:", export_response)


# 🔹 8. Show file location
print(f"Board exported to: out/{export_response['out_file']}")