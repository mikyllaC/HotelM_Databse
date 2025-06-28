from utils.helpers import log, get_connection


def main():
    room_model = RoomModel()

    # sample_room_type_data = {
    #     "TYPE_NAME": "Standard Room",
    #     "BED_TYPE": "Queen",
    #     "CAPACITY": 2,  # Base adult capacity
    #     "EXTRA_CAPACITY": 1,  # Extra capacity for additional guests
    #     "BASE_PRICE": 99.99,  # Base rate per night
    #     "EXTRA_ADULT_RATE": 25.0,  # Cost for extra adult
    #     "EXTRA_CHILD_RATE": 15.0,  # Cost for extra child
    #     "IMAGE": "standard_room.jpg",
    #     "DESCRIPTION": "Comfortable standard room with one queen bed"
    # }
    # room_type_id = room_model.add_room_type(sample_room_type_data)
    #
    # sample_room_data = {
    #     "ROOM_NUMBER": "101",
    #     "ROOM_TYPE_ID": room_type_id,
    #     "FLOOR": 1,
    #     "STATUS": "Available",
    #     "NOTES": "Newly renovated"
    # }
    # room_id = room_model.add_room(sample_room_data)
    # amenity_id = room_model.add_amenity("Air Conditioning")
    # room_model.assign_amenity_to_room(room_id, amenity_id)


class RoomModel:
    def __init__(self):
        self.create_room_table()


    def create_room_table(self):
        with get_connection() as conn:
            cursor = conn.cursor()

            # Create ROOM_TYPE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ROOM_TYPE (
                    ROOM_TYPE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    TYPE_NAME TEXT NOT NULL UNIQUE,
                    BED_TYPE TEXT NOT NULL,
                    BASE_ADULT_NUM INTEGER NOT NULL,
                    BASE_CHILD_NUM INTEGER DEFAULT 0,
                    EXTRA_ADULT_NUM INTEGER NOT NULL,
                    EXTRA_CHILD_NUM INTEGER DEFAULT 0,
                    MAX_OCCUPANCY INTEGER NOT NULL,
                    BASE_RATE REAL NOT NULL,
                    EXTRA_ADULT_RATE REAL NOT NULL,
                    EXTRA_CHILD_RATE REAL NOT NULL,
                    IMAGE TEXT,
                    DESCRIPTION TEXT
                )""")
            # Create ROOM table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ROOM (
                    ROOM_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ROOM_NUMBER TEXT NOT NULL UNIQUE,
                    ROOM_TYPE_ID INTEGER NOT NULL,
                    FLOOR INTEGER NOT NULL,
                    STATUS TEXT DEFAULT 'Available',
                    NOTES TEXT,
                    FOREIGN KEY (ROOM_TYPE_ID) REFERENCES ROOM_TYPE(ROOM_TYPE_ID)
                )""")
            # Master list of all possible amenities
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ROOM_AMENITY (
                    AMENITY_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    AMENITY_NAME TEXT NOT NULL UNIQUE
                )""")
            # # Mapping table to link ROOM and ROOM_AMENITY
            # cursor.execute("""
            #     CREATE TABLE IF NOT EXISTS ROOM_AMENITY_MAP (
            #         ROOM_ID INTEGER NOT NULL,
            #         AMENITY_ID INTEGER NOT NULL,
            #         FOREIGN KEY (ROOM_ID) REFERENCES ROOM(ROOM_ID),
            #         FOREIGN KEY (AMENITY_ID) REFERENCES ROOM_AMENITY(AMENITY_ID),
            #         PRIMARY KEY (ROOM_ID, AMENITY_ID)
            #     )""")
            # Mapping table to link ROOM_TYPE and ROOM_AMENITY
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ROOM_TYPE_AMENITY_MAP (
                    ROOM_TYPE_ID INTEGER NOT NULL,
                    AMENITY_ID INTEGER NOT NULL,
                    FOREIGN KEY (ROOM_TYPE_ID) REFERENCES ROOM_TYPE(ROOM_TYPE_ID),
                    FOREIGN KEY (AMENITY_ID) REFERENCES ROOM_AMENITY(AMENITY_ID),
                    PRIMARY KEY (ROOM_TYPE_ID, AMENITY_ID)
                )""")
            conn.commit()
            log("Room tables created successfully.")


    def add_room_type(self, room_type_data: dict):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ROOM_TYPE (
                    TYPE_NAME, BED_TYPE, BASE_ADULT_NUM, BASE_CHILD_NUM,
                    EXTRA_ADULT_NUM, EXTRA_CHILD_NUM, MAX_OCCUPANCY,
                    BASE_RATE, EXTRA_ADULT_RATE, EXTRA_CHILD_RATE,
                    IMAGE, DESCRIPTION
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                room_type_data["TYPE_NAME"],
                room_type_data["BED_TYPE"],
                room_type_data.get("BASE_ADULT_NUM", 0),
                room_type_data.get("BASE_CHILD_NUM", 0),
                room_type_data.get("EXTRA_ADULT_NUM", 0),
                room_type_data.get("EXTRA_CHILD_NUM", 0),
                room_type_data.get("MAX_OCCUPANCY",
                    room_type_data.get("BASE_ADULT_NUM", 0) +
                    room_type_data.get("BASE_CHILD_NUM", 0) +
                    room_type_data.get("EXTRA_ADULT_NUM", 0) +
                    room_type_data.get("EXTRA_CHILD_NUM", 0)
                ),
                room_type_data.get("BASE_RATE", 0.0),
                room_type_data.get("EXTRA_ADULT_RATE", 0.0),
                room_type_data.get("EXTRA_CHILD_RATE", 0.0),
                room_type_data.get("IMAGE", ""),
                room_type_data.get("DESCRIPTION", "")
            ))
            conn.commit()
            log(f"Room type {room_type_data['TYPE_NAME']} added successfully.")
            return cursor.lastrowid  # Return the ID of the newly created room type


    def add_room(self, room_data: dict):
        log(f"[DEBUG] Adding room with data: {room_data}")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ROOM (
                    ROOM_NUMBER, ROOM_TYPE_ID, FLOOR, STATUS, NOTES
                ) VALUES (?, ?, ?, ?, ?)""", (
                room_data["ROOM_NUMBER"],
                room_data["ROOM_TYPE_ID"],
                room_data.get("FLOOR", 1),
                room_data.get("STATUS", "Available"),
                room_data.get("NOTES", "")
            ))
            conn.commit()
            log(f"Room {room_data['ROOM_NUMBER']} added successfully.")
            return cursor.lastrowid  # Return the ID of the newly created room


    def add_amenity(self, amenity_name: str):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ROOM_AMENITY (AMENITY_NAME) 
                VALUES (?)""", (amenity_name,))
            conn.commit()

            cursor.execute("""
            SELECT AMENITY_ID 
            FROM ROOM_AMENITY 
            WHERE AMENITY_NAME = ?
            """, (amenity_name,))

            result = cursor.fetchone()
            log(f"Amenity '{amenity_name}' added successfully.")
            return result[0] if result else None


    def assign_amenity_to_room(self, room_id: int, amenity_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO ROOM_AMENITY_MAP (ROOM_ID, AMENITY_ID)
                VALUES (?, ?)""", (room_id, amenity_id))
            conn.commit()
            log(f"Amenity ID {amenity_id} assigned to Room ID {room_id} successfully.")


    def assign_amenity_to_room_type(self, room_type_id: int, amenity_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO ROOM_TYPE_AMENITY_MAP (ROOM_TYPE_ID, AMENITY_ID)
                VALUES (?, ?)""", (room_type_id, amenity_id))
            conn.commit()
            log(f"Amenity ID {amenity_id} assigned to Room Type ID {room_type_id} successfully.")


    def get_all_rooms(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ROOM")
            rooms = cursor.fetchall()
            log(f"Retrieved {len(rooms)} rooms from the database.")
            return rooms


    def get_all_room_types(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ROOM_TYPE")
            room_types = cursor.fetchall()
            log(f"Retrieved {len(room_types)} room types from the database.")
            return room_types


    def get_all_amenities(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ROOM_AMENITY")
            amenities = cursor.fetchall()
            log(f"Retrieved {len(amenities)} amenities from the database.")
            return amenities


    def get_room_type_by_id(self, room_type_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ROOM_TYPE WHERE ROOM_TYPE_ID = ?", (room_type_id,))
            room_type = cursor.fetchone()
            if room_type:
                return {
                    "ROOM_TYPE_ID": room_type[0],
                    "TYPE_NAME": room_type[1],
                    "BED_TYPE": room_type[2],
                    "CAPACITY": room_type[3],
                    "EXTRA_CAPACITY": room_type[4],
                    "BASE_PRICE": room_type[5],
                    "IMAGE": room_type[6],
                    "DESCRIPTION": room_type[7]
                }
            else:
                log(f"No room type found with ID {room_type_id}.")
                return None


    # def get_amenities_for_room(self, room_id: int):
    #     with get_connection() as conn:
    #         cursor = conn.cursor()
    #         cursor.execute("""
    #             SELECT a.AMENITY_NAME
    #             FROM ROOM_AMENITY a
    #             JOIN ROOM_AMENITY_MAP m ON a.AMENITY_ID = m.AMENITY_ID
    #             WHERE m.ROOM_ID = ?
    #         """, (room_id,))
    #         amenities = cursor.fetchall()
    #         #log(f"Retrieved {len(amenities)} amenities for Room ID {room_id}.")
    #         return [amenity[0] for amenity in amenities]


    def get_amenities_for_room_type(self, room_type_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.AMENITY_NAME 
                FROM ROOM_AMENITY a
                JOIN ROOM_TYPE_AMENITY_MAP m ON a.AMENITY_ID = m.AMENITY_ID
                WHERE m.ROOM_TYPE_ID = ?
            """, (room_type_id,))
            amenities = cursor.fetchall()
            return [amenity[0] for amenity in amenities]


if __name__ == "__main__":
    main()