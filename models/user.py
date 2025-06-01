from database.db_manager import DBManager

class User:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.db = DBManager()


    def authenticate(self, password):
        # Temporary: hardcoded check
        return self.employee_id == "SM001" and password == "password"


    def get_position(self):
        return self.position