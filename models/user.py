

class User:
    def __init__(self, username):
        self.username = username
        self.role = "admin"             # placeholder

    def authenticate(self, password):
        # Temporary: hardcoded check
        return self.username == "admin" and password == "password"

    def get_role(self):
        return self.role