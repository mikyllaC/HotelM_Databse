from database.db_manager import DBManager
from utils.session import Session

class User:
    def __init__(self, employee_id):
        self.employee_id = employee_id


    def login(self, password):
        self.db_manager = DBManager()
        user_record = self.db_manager.get_user_credentials(employee_id=self.employee_id)

        if not user_record:
            return False  # employee not found
        if user_record['STATUS'] != 'active':
            return False  # deactivated account
        if user_record['PASSWORD'] != password:
            return False  # incorrect password

        self.populate_from_record(user_record)

        Session.current_user = self
        return True


    def populate_from_record(self, user_record):
        self.first_name = user_record["FIRST_NAME"]
        self.last_name = user_record["LAST_NAME"]
        self.position = user_record["POSITION"]
        self.status = user_record["STATUS"]
        self.email = user_record["EMAIL"]