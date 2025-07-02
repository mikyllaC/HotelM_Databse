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
                    IMAGE, DESCRIPTION
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
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

    def get_room_by_id(self, room_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ROOM WHERE ROOM_ID = ?", (room_id,))
            room = cursor.fetchone()
            if room:
                # Get column names from cursor description
                columns = [column[0] for column in cursor.description]
                # Create a dictionary with column names as keys
                room_dict = {columns[i]: room[i] for i in range(len(columns))}
                return room_dict
            else:
                log(f"No room found with ID {room_id}.")
                return None


    def get_room_type_by_id(self, room_type_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ROOM_TYPE WHERE ROOM_TYPE_ID = ?", (room_type_id,))
            room_type = cursor.fetchone()
            if room_type:
                # Get column names from cursor description
                columns = [column[0] for column in cursor.description]
                # Create a dictionary with column names as keys
                room_type_dict = {columns[i]: room_type[i] for i in range(len(columns))}
                return room_type_dict
            else:
                log(f"No room type found with ID {room_type_id}.")
                return None

    def get_room_data_with_type(self, room_id: int):
        """Fetch room data from the database including the room type name"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, rt.TYPE_NAME 
                FROM ROOM r
                JOIN ROOM_TYPE rt ON r.ROOM_TYPE_ID = rt.ROOM_TYPE_ID
                WHERE r.ROOM_ID = ?
            """, (room_id,))
            room_data = cursor.fetchone()

            if room_data:
                # Convert to dictionary
                columns = [column[0] for column in cursor.description]
                room_dict = {columns[i]: room_data[i] for i in range(len(columns))}
                return room_dict
            else:
                log(f"No room found with ID {room_id}.")
                return None


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

    def update_room(self, room_data: dict):
        """Update a room's information in the database"""
        log(f"[DEBUG] Attempting to update room with data: {room_data}")

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE ROOM SET 
                    ROOM_NUMBER = ?, 
                    ROOM_TYPE_ID = ?, 
                    FLOOR = ?, 
                    STATUS = ?, 
                    NOTES = ? 
                WHERE ROOM_ID = ?
            """, (
                room_data["ROOM_NUMBER"],
                room_data["ROOM_TYPE_ID"],
                room_data["FLOOR"],
                room_data["STATUS"],
                room_data["NOTES"],
                room_data["ROOM_ID"]
            ))
            conn.commit()

            log(f"Room updated successfully with ID: {room_data['ROOM_ID']}")
            return True


    def update_amenity(self, amenity_id: int, new_name: str):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE ROOM_AMENITY SET AMENITY_NAME = ? WHERE AMENITY_ID = ?", (new_name, amenity_id))
            conn.commit()
            log(f"Amenity with ID {amenity_id} updated to '{new_name}' successfully.")


    def delete_amenity(self, amenity_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ROOM_AMENITY WHERE AMENITY_ID = ?", (amenity_id,))
            conn.commit()
            log(f"Amenity with ID {amenity_id} deleted successfully.")

    def get_room_types_for_amenity(self, amenity_id: int):
        """Get all room types that use a specific amenity"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT rt.ROOM_TYPE_ID, rt.TYPE_NAME 
                FROM ROOM_TYPE rt
                JOIN ROOM_TYPE_AMENITY_MAP rtam ON rt.ROOM_TYPE_ID = rtam.ROOM_TYPE_ID
                WHERE rtam.AMENITY_ID = ?
            """, (amenity_id,))
            room_types = cursor.fetchall()
            return room_types

    def get_amenity_by_id(self, amenity_id: int):
        """Get details of a specific amenity by ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ROOM_AMENITY WHERE AMENITY_ID = ?", (amenity_id,))
            amenity = cursor.fetchone()
            if amenity:
                columns = [column[0] for column in cursor.description]
                amenity_dict = {columns[i]: amenity[i] for i in range(len(columns))}
                return amenity_dict
            else:
                log(f"No amenity found with ID {amenity_id}.")
                return None

    # Hard Delete Functions
    def hard_delete_room(self, room_id: int):
        """Permanently delete a room from the database"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Check if room exists and get details for logging
                room = self.get_room_by_id(room_id)
                if not room:
                    log(f"Cannot delete room: Room with ID {room_id} not found.")
                    return False

                # Check for active reservations (if reservation table exists)
                try:
                    cursor.execute("SELECT COUNT(*) FROM RESERVATION WHERE ROOM_ID = ? AND STATUS NOT IN ('Cancelled', 'Completed')", (room_id,))
                    active_reservations = cursor.fetchone()[0]
                    if active_reservations > 0:
                        log(f"Cannot delete room {room['ROOM_NUMBER']}: Has {active_reservations} active reservations.")
                        return False
                except:
                    # Reservation table might not exist, continue with deletion
                    pass

                # Delete the room
                cursor.execute("DELETE FROM ROOM WHERE ROOM_ID = ?", (room_id,))

                if cursor.rowcount > 0:
                    conn.commit()
                    log(f"Room {room['ROOM_NUMBER']} (ID: {room_id}) permanently deleted from database.")
                    return True
                else:
                    log(f"Failed to delete room with ID {room_id}.")
                    return False

        except Exception as e:
            log(f"Error deleting room {room_id}: {str(e)}")
            return False

    def hard_delete_room_type(self, room_type_id: int):
        """Permanently delete a room type from the database"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Check if room type exists
                room_type = self.get_room_type_by_id(room_type_id)
                if not room_type:
                    log(f"Cannot delete room type: Room type with ID {room_type_id} not found.")
                    return False

                # Check if any rooms are using this room type
                cursor.execute("SELECT COUNT(*) FROM ROOM WHERE ROOM_TYPE_ID = ?", (room_type_id,))
                rooms_count = cursor.fetchone()[0]
                if rooms_count > 0:
                    log(f"Cannot delete room type '{room_type['TYPE_NAME']}': {rooms_count} rooms are still using this type.")
                    return False

                # Delete amenity mappings first
                cursor.execute("DELETE FROM ROOM_TYPE_AMENITY_MAP WHERE ROOM_TYPE_ID = ?", (room_type_id,))

                # Delete the room type
                cursor.execute("DELETE FROM ROOM_TYPE WHERE ROOM_TYPE_ID = ?", (room_type_id,))

                if cursor.rowcount > 0:
                    conn.commit()
                    log(f"Room type '{room_type['TYPE_NAME']}' (ID: {room_type_id}) permanently deleted from database.")
                    return True
                else:
                    log(f"Failed to delete room type with ID {room_type_id}.")
                    return False

        except Exception as e:
            log(f"Error deleting room type {room_type_id}: {str(e)}")
            return False

    def hard_delete_amenity(self, amenity_id: int):
        """Permanently delete an amenity from the database"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Check if amenity exists
                amenity = self.get_amenity_by_id(amenity_id)
                if not amenity:
                    log(f"Cannot delete amenity: Amenity with ID {amenity_id} not found.")
                    return False

                # Delete all mappings first
                cursor.execute("DELETE FROM ROOM_TYPE_AMENITY_MAP WHERE AMENITY_ID = ?", (amenity_id,))

                # Delete the amenity
                cursor.execute("DELETE FROM ROOM_AMENITY WHERE AMENITY_ID = ?", (amenity_id,))

                if cursor.rowcount > 0:
                    conn.commit()
                    log(f"Amenity '{amenity['AMENITY_NAME']}' (ID: {amenity_id}) permanently deleted from database.")
                    return True
                else:
                    log(f"Failed to delete amenity with ID {amenity_id}.")
                    return False

        except Exception as e:
            log(f"Error deleting amenity {amenity_id}: {str(e)}")
            return False

    # Enhanced Search and Filter Functions
    def search_rooms(self, search_query="", status_filter="All", floor_filter="All", room_type_filter="All"):
        """Enhanced search and filter function for rooms"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                # Build the base query
                query = """
                    SELECT r.*, rt.TYPE_NAME 
                    FROM ROOM r
                    LEFT JOIN ROOM_TYPE rt ON r.ROOM_TYPE_ID = rt.ROOM_TYPE_ID
                    WHERE 1=1
                """
                params = []

                # Add search filter
                if search_query and search_query.strip():
                    query += " AND (LOWER(r.ROOM_NUMBER) LIKE LOWER(?) OR LOWER(rt.TYPE_NAME) LIKE LOWER(?) OR LOWER(r.NOTES) LIKE LOWER(?))"
                    search_param = f"%{search_query.strip()}%"
                    params.extend([search_param, search_param, search_param])

                # Add status filter
                if status_filter and status_filter != "All":
                    query += " AND r.STATUS = ?"
                    params.append(status_filter)

                # Add floor filter
                if floor_filter and floor_filter != "All":
                    query += " AND r.FLOOR = ?"
                    params.append(int(floor_filter))

                # Add room type filter
                if room_type_filter and room_type_filter != "All":
                    query += " AND rt.TYPE_NAME = ?"
                    params.append(room_type_filter)

                query += " ORDER BY r.ROOM_NUMBER"

                cursor.execute(query, params)
                rooms = cursor.fetchall()

                # Convert to list of dictionaries
                columns = [column[0] for column in cursor.description]
                room_dicts = []
                for room in rooms:
                    room_dict = {columns[i]: room[i] for i in range(len(columns))}
                    room_dicts.append(room_dict)

                log(f"Search returned {len(room_dicts)} rooms with filters: search='{search_query}', status='{status_filter}', floor='{floor_filter}', type='{room_type_filter}'")
                return room_dicts

        except Exception as e:
            log(f"Error searching rooms: {str(e)}")
            return []

    def get_unique_floors(self):
        """Get list of unique floor numbers for filter dropdown"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT FLOOR FROM ROOM ORDER BY FLOOR")
                floors = cursor.fetchall()
                return [str(floor[0]) for floor in floors]
        except Exception as e:
            log(f"Error getting unique floors: {str(e)}")
            return []

    def get_unique_statuses(self):
        """Get list of unique room statuses for filter dropdown"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT STATUS FROM ROOM ORDER BY STATUS")
                statuses = cursor.fetchall()
                return [status[0] for status in statuses]
        except Exception as e:
            log(f"Error getting unique statuses: {str(e)}")
            return []

    def get_unique_room_type_names(self):
        """Get list of unique room type names for filter dropdown"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT TYPE_NAME FROM ROOM_TYPE ORDER BY TYPE_NAME")
                types = cursor.fetchall()
                return [type_name[0] for type_name in types]
        except Exception as e:
            log(f"Error getting unique room types: {str(e)}")
            return []


if __name__ == "__main__":
    main()