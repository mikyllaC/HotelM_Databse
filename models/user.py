from database.db_manager import DBManager
from utils.session import Session

class User:
    def __init__(self, employee_id):
        self.db_manager = DBManager

        self.employee_id = employee_id
        self.full_name = None
        self.status = None
        self.position = None


    def login(self, password):
        