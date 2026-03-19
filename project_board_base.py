import json
import uuid
import os 
from datetime import datetime
from utils.storage import read_data, write_data

BOARD_FILE = "boards.json"
TASK_FILE = "tasks.json"


class ProjectBoardBase:

    def create_board(self, request: str):
        try:
            data = json.loads(request)
            boards = read_data(BOARD_FILE)

            if len(data["name"]) > 64 or len(data["description"]) > 128:
                raise Exception("Invalid length")

            if any(b["name"] == data["name"] and b["team_id"] == data["team_id"] for b in boards):
                raise Exception("Board name must be unique per team")

            board = {
                "id": str(uuid.uuid4()),
                "name": data["name"],
                "description": data["description"],
                "team_id": data["team_id"],
                "status": "OPEN",
                "creation_time": data["creation_time"]
            }

            boards.append(board)
            write_data(BOARD_FILE, boards)

            return json.dumps({"id": board["id"]})

        except Exception as e:
            return json.dumps({"error": str(e)})

    def close_board(self, request: str) -> str:
        try:
            data = json.loads(request)

            boards = read_data(BOARD_FILE)
            tasks = read_data(TASK_FILE)

            board = next((b for b in boards if b["id"] == data["id"]), None)
            if not board:
                raise Exception("Board not found")

            board_tasks = [t for t in tasks if t["board_id"] == board["id"]]

            if any(t["status"] != "COMPLETE" for t in board_tasks):
                raise Exception("All tasks must be COMPLETE")

            board["status"] = "CLOSED"
            board["end_time"] = datetime.now().isoformat()

            write_data(BOARD_FILE, boards)

            return json.dumps({"message": "Board closed"})

        except Exception as e:
            return json.dumps({"error": str(e)})

    def add_task(self, request: str) -> str:
        try:
            data = json.loads(request)

            boards = read_data(BOARD_FILE)
            tasks = read_data(TASK_FILE)

            board = next((b for b in boards if b["id"] == data["board_id"]), None)
            if not board:
                raise Exception("Board not found")

            if board["status"] != "OPEN":
                raise Exception("Board is closed")

            if len(data["title"]) > 64 or len(data["description"]) > 128:
                raise Exception("Invalid length")

            if any(t["title"] == data["title"] and t["board_id"] == board["id"] for t in tasks):
                raise Exception("Task title must be unique per board")

            task = {
                "id": str(uuid.uuid4()),
                "title": data["title"],
                "description": data["description"],
                "board_id": board["id"],
                "user_id": data["user_id"],
                "status": "OPEN",
                "creation_time": data["creation_time"]
            }

            tasks.append(task)
            write_data(TASK_FILE, tasks)

            return json.dumps({"id": task["id"]})

        except Exception as e:
            return json.dumps({"error": str(e)})

    def update_task_status(self, request: str):
        try:
            data = json.loads(request)
            tasks = read_data(TASK_FILE)

            task = next((t for t in tasks if t["id"] == data["id"]), None)
            if not task:
                raise Exception("Task not found")

            task["status"] = data["status"]

            write_data(TASK_FILE, tasks)

            return json.dumps({"message": "Task updated"})

        except Exception as e:
            return json.dumps({"error": str(e)})

    def list_boards(self, request: str) -> str:
        try:
            data = json.loads(request)
            boards = read_data(BOARD_FILE)

            result = [
                {"id": b["id"], "name": b["name"]}
                for b in boards
                if b["team_id"] == data["id"] and b["status"] == "OPEN"
            ]

            return json.dumps(result)

        except Exception as e:
            return json.dumps({"error": str(e)})

    def export_board(self, request: str) -> str:
        try:
            data = json.loads(request)

            boards = read_data(BOARD_FILE)
            tasks = read_data(TASK_FILE)

            board = next((b for b in boards if b["id"] == data["id"]), None)
            if not board:
                raise Exception("Board not found")

            board_tasks = [t for t in tasks if t["board_id"] == board["id"]]

            os.makedirs("out", exist_ok=True)

            filename = f"board_{board['id']}.txt"
            filepath = os.path.join("out", filename)

            # ✅ write inside out/
            with open(filepath, "w") as f:
                f.write("=" * 50 + "\n")
                f.write(f"BOARD: {board['name']}\n")
                f.write("=" * 50 + "\n\n")

                f.write(f"Description : {board['description']}\n")
                f.write(f"Status      : {board['status']}\n")
                f.write(f"Created At  : {board['creation_time']}\n")
                f.write(f"Total Tasks : {len(board_tasks)}\n\n")

                f.write("-" * 50 + "\n")
                f.write("TASK LIST\n")
                f.write("-" * 50 + "\n")

                for i, t in enumerate(board_tasks, 1):
                    f.write(f"\n{i}. {t['title']}\n")
                    f.write(f"   Description : {t['description']}\n")
                    f.write(f"   Status      : {t['status']}\n")
                    f.write(f"   Assigned To : {t['user_id']}\n")

                f.write("\n" + "=" * 50)

            return json.dumps({"out_file": filename})

        except Exception as e:
            return json.dumps({"error": str(e)})
        

# class ProjectBoardBase:
#     """
#     A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
#     """

#     # create a board
#     def create_board(self, request: str):
#         """
#         :param request: A json string with the board details.
#         {
#             "name" : "<board_name>",
#             "description" : "<description>",
#             "team_id" : "<team id>"
#             "creation_time" : "<date:time when board was created>"
#         }
#         :return: A json string with the response {"id" : "<board_id>"}

#         Constraint:
#          * board name must be unique for a team
#          * board name can be max 64 characters
#          * description can be max 128 characters
#         """
#         pass

#     # close a board
#     def close_board(self, request: str) -> str:
#         """
#         :param request: A json string with the user details
#         {
#           "id" : "<board_id>"
#         }

#         :return:

#         Constraint:
#           * Set the board status to CLOSED and record the end_time date:time
#           * You can only close boards with all tasks marked as COMPLETE
#         """
#         pass

#     # add task to board
#     def add_task(self, request: str) -> str:
#         """
#         :param request: A json string with the task details. Task is assigned to a user_id who works on the task
#         {
#             "title" : "<board_name>",
#             "description" : "<description>",
#             "user_id" : "<team id>"
#             "creation_time" : "<date:time when task was created>"
#         }
#         :return: A json string with the response {"id" : "<task_id>"}

#         Constraint:
#          * task title must be unique for a board
#          * title name can be max 64 characters
#          * description can be max 128 characters

#         Constraints:
#         * Can only add task to an OPEN board
#         """
#         pass

#     # update the status of a task
#     def update_task_status(self, request: str):
#         """
#         :param request: A json string with the user details
#         {
#             "id" : "<task_id>",
#             "status" : "OPEN | IN_PROGRESS | COMPLETE"
#         }
#         """
#         pass

#     # list all open boards for a team
#     def list_boards(self, request: str) -> str:
#         """
#         :param request: A json string with the team identifier
#         {
#           "id" : "<team_id>"
#         }

#         :return:
#         [
#           {
#             "id" : "<board_id>",
#             "name" : "<board_name>"
#           }
#         ]
#         """
#         pass

#     def export_board(self, request: str) -> str:
#         """
#         Export a board in the out folder. The output will be a txt file.
#         We want you to be creative. Output a presentable view of the board and its tasks with the available data.
#         :param request:
#         {
#           "id" : "<board_id>"
#         }
#         :return:
#         {
#           "out_file" : "<name of the file created>"
#         }
#         """
#         pass

