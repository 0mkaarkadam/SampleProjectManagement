import json
import uuid
from datetime import datetime
from utils.storage import read_data, write_data

FILE = "users.json"


class UserBase:

    def create_user(self, request: str) -> str:
        try:
            data = json.loads(request)
            users = read_data(FILE)

            if len(data["name"]) > 64 or len(data["display_name"]) > 64:
                raise Exception("Invalid length")

            if any(u["name"] == data["name"] for u in users):
                raise Exception("User name must be unique")

            user = {
                "id": str(uuid.uuid4()),
                "name": data["name"],
                "display_name": data["display_name"],
                "creation_time": datetime.now().isoformat()
            }

            users.append(user)
            write_data(FILE, users)

            return json.dumps({"id": user["id"]})

        except Exception as e:
            return json.dumps({"error": str(e)})

    def list_users(self) -> str:
        try:
            return json.dumps(read_data(FILE))
        except Exception as e:
            return json.dumps({"error": str(e)})

    def describe_user(self, request: str) -> str:
        try:
            data = json.loads(request)
            users = read_data(FILE)

            user = next((u for u in users if u["id"] == data["id"]), None)
            if not user:
                raise Exception("User not found")

            return json.dumps(user)

        except Exception as e:
            return json.dumps({"error": str(e)})

    def update_user(self, request: str) -> str:
        try:
            data = json.loads(request)
            users = read_data(FILE)

            user = next((u for u in users if u["id"] == data["id"]), None)
            if not user:
                raise Exception("User not found")

            update_data = data["user"]

            if "name" in update_data:
                raise Exception("User name cannot be updated")

            if len(update_data.get("display_name", "")) > 128:
                raise Exception("Invalid display name")

            user["display_name"] = update_data.get("display_name", user["display_name"])

            write_data(FILE, users)

            return json.dumps({"message": "Updated"})

        except Exception as e:
            return json.dumps({"error": str(e)})

    def get_user_teams(self, request: str) -> str:
        try:
            data = json.loads(request)

            teams = read_data("teams.json")

            result = [t for t in teams if data["id"] in t.get("users", [])]

            return json.dumps(result)

        except Exception as e:
            return json.dumps({"error": str(e)})

# class UserBase:
#     """
#     Base interface implementation for API's to manage users.
#     """

#     # create a user
#     def create_user(self, request: str) -> str:
#         """
#         :param request: A json string with the user details
#         {
#           "name" : "<user_name>",
#           "display_name" : "<display name>"
#         }
#         :return: A json string with the response {"id" : "<user_id>"}

#         Constraint:
#             * user name must be unique
#             * name can be max 64 characters
#             * display name can be max 64 characters
#         """
#         pass

#     # list all users
#     def list_users(self) -> str:
#         """
#         :return: A json list with the response
#         [
#           {
#             "name" : "<user_name>",
#             "display_name" : "<display name>",
#             "creation_time" : "<some date:time format>"
#           }
#         ]
#         """
#         pass

#     # describe user
#     def describe_user(self, request: str) -> str:
#         """
#         :param request: A json string with the user details
#         {
#           "id" : "<user_id>"
#         }

#         :return: A json string with the response

#         {
#           "name" : "<user_name>",
#           "description" : "<some description>",
#           "creation_time" : "<some date:time format>"
#         }

#         """
#         pass

#     # update user
#     def update_user(self, request: str) -> str:
#         """
#         :param request: A json string with the user details
#         {
#           "id" : "<user_id>",
#           "user" : {
#             "name" : "<user_name>",
#             "display_name" : "<display name>"
#           }
#         }

#         :return:

#         Constraint:
#             * user name cannot be updated
#             * name can be max 64 characters
#             * display name can be max 128 characters
#         """
#         pass

#     def get_user_teams(self, request: str) -> str:
#         """
#         :param request:
#         {
#           "id" : "<user_id>"
#         }

#         :return: A json list with the response.
#         [
#           {
#             "name" : "<team_name>",
#             "description" : "<some description>",
#             "creation_time" : "<some date:time format>"
#           }
#         ]
#         """
#         pass

