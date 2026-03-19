import json
import uuid
from datetime import datetime
from utils.storage import read_data, write_data

FILE = "teams.json"


class TeamBase:

    def create_team(self, request: str) -> str:
        try:
            data = json.loads(request)
            teams = read_data(FILE)

            if len(data["name"]) > 64 or len(data["description"]) > 128:
                raise Exception("Invalid length")

            if any(t["name"] == data["name"] for t in teams):
                raise Exception("Team name must be unique")

            team = {
                "id": str(uuid.uuid4()),
                "name": data["name"],
                "description": data["description"],
                "admin": data["admin"],
                "users": [data["admin"]],
                "creation_time": datetime.now().isoformat()
            }

            teams.append(team)
            write_data(FILE, teams)

            return json.dumps({"id": team["id"]})

        except Exception as e:
            return json.dumps({"error": str(e)})

    def list_teams(self) -> str:
        try:
            return json.dumps(read_data(FILE))
        except Exception as e:
            return json.dumps({"error": str(e)})

    def describe_team(self, request: str) -> str:
        try:
            data = json.loads(request)
            teams = read_data(FILE)

            team = next((t for t in teams if t["id"] == data["id"]), None)
            if not team:
                raise Exception("Team not found")

            return json.dumps(team)

        except Exception as e:
            return json.dumps({"error": str(e)})

    def update_team(self, request: str) -> str:
        try:
            data = json.loads(request)
            teams = read_data(FILE)

            team = next((t for t in teams if t["id"] == data["id"]), None)
            if not team:
                raise Exception("Team not found")

            update_data = data["team"]

            if len(update_data["name"]) > 64 or len(update_data["description"]) > 128:
                raise Exception("Invalid length")

            if any(t["name"] == update_data["name"] and t["id"] != team["id"] for t in teams):
                raise Exception("Team name must be unique")

            team.update(update_data)
            write_data(FILE, teams)

            return json.dumps({"message": "Updated"})

        except Exception as e:
            return json.dumps({"error": str(e)})

    def add_users_to_team(self, request: str):
        try:
            data = json.loads(request)
            teams = read_data(FILE)

            team = next((t for t in teams if t["id"] == data["id"]), None)
            if not team:
                raise Exception("Team not found")

            if len(data["users"]) > 50:
                raise Exception("Max 50 users allowed")

            team["users"] = list(set(team["users"] + data["users"]))
            write_data(FILE, teams)

            return json.dumps({"message": "Users added"})

        except Exception as e:
            return json.dumps({"error": str(e)})

    def remove_users_from_team(self, request: str):
        try:
            data = json.loads(request)
            teams = read_data(FILE)

            team = next((t for t in teams if t["id"] == data["id"]), None)
            if not team:
                raise Exception("Team not found")

            team["users"] = [u for u in team["users"] if u not in data["users"]]
            write_data(FILE, teams)

            return json.dumps({"message": "Users removed"})

        except Exception as e:
            return json.dumps({"error": str(e)})

    def list_team_users(self, request: str):
        try:
            data = json.loads(request)

            teams = read_data(FILE)
            users = read_data("users.json")

            team = next((t for t in teams if t["id"] == data["id"]), None)
            if not team:
                raise Exception("Team not found")

            result = [u for u in users if u["id"] in team["users"]]

            return json.dumps(result)

        except Exception as e:
            return json.dumps({"error": str(e)})

# class TeamBase:
#     """
#     Base interface implementation for API's to manage teams.
#     For simplicity a single team manages a single project. And there is a separate team per project.
#     Users can be
#     """

#     # create a team
#     def create_team(self, request: str) -> str:
#         """
#         :param request: A json string with the team details
#         {
#           "name" : "<team_name>",
#           "description" : "<some description>",
#           "admin": "<id of a user>"
#         }
#         :return: A json string with the response {"id" : "<team_id>"}

#         Constraint:
#             * Team name must be unique
#             * Name can be max 64 characters
#             * Description can be max 128 characters
#         """
#         pass

#     # list all teams
#     def list_teams(self) -> str:
#         """
#         :return: A json list with the response.
#         [
#           {
#             "name" : "<team_name>",
#             "description" : "<some description>",
#             "creation_time" : "<some date:time format>",
#             "admin": "<id of a user>"
#           }
#         ]
#         """
#         pass

#     # describe team
#     def describe_team(self, request: str) -> str:
#         """
#         :param request: A json string with the team details
#         {
#           "id" : "<team_id>"
#         }

#         :return: A json string with the response

#         {
#           "name" : "<team_name>",
#           "description" : "<some description>",
#           "creation_time" : "<some date:time format>",
#           "admin": "<id of a user>"
#         }

#         """
#         pass

#     # update team
#     def update_team(self, request: str) -> str:
#         """
#         :param request: A json string with the team details
#         {
#           "id" : "<team_id>",
#           "team" : {
#             "name" : "<team_name>",
#             "description" : "<team_description>",
#             "admin": "<id of a user>"
#           }
#         }

#         :return:

#         Constraint:
#             * Team name must be unique
#             * Name can be max 64 characters
#             * Description can be max 128 characters
#         """
#         pass

#     # add users to team
#     def add_users_to_team(self, request: str):
#         """
#         :param request: A json string with the team details
#         {
#           "id" : "<team_id>",
#           "users" : ["user_id 1", "user_id2"]
#         }

#         :return:

#         Constraint:
#         * Cap the max users that can be added to 50
#         """
#         pass

#     # add users to team
#     def remove_users_from_team(self, request: str):
#         """
#         :param request: A json string with the team details
#         {
#           "id" : "<team_id>",
#           "users" : ["user_id 1", "user_id2"]
#         }

#         :return:

#         Constraint:
#         * Cap the max users that can be added to 50
#         """
#         pass

#     # list users of a team
#     def list_team_users(self, request: str):
#         """
#         :param request: A json string with the team identifier
#         {
#           "id" : "<team_id>"
#         }

#         :return:
#         [
#           {
#             "id" : "<user_id>",
#             "name" : "<user_name>",
#             "display_name" : "<display name>"
#           }
#         ]
#         """
#         pass

