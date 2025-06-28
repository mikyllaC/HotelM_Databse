from utils.helpers import log, get_connection

def main():
    # Example usage
    hotel_model = HotelModel()

    hotel_model.create_default_hotel()



class HotelModel:
    def __init__(self):
        self.create_hotel_table()


    def create_hotel_table(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS HOTEL (
                    HOTEL_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    HOTEL_NAME TEXT NOT NULL UNIQUE,
                    ADDRESS TEXT NOT NULL,
                    FLOORS INTEGER DEFAULT 1,
                    PHONE_NUMBER TEXT,
                    EMAIL TEXT,
                    WEBSITE TEXT,
                    LOGO_PATH TEXT,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            log("Hotel table created successfully.")


    def create_default_hotel(self):
        """Add a new hotel to the database"""#
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO HOTEL (HOTEL_NAME, ADDRESS, FLOORS, PHONE_NUMBER, EMAIL, WEBSITE, LOGO_PATH)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ("The Reverie Hotel", "123 Default St", 6, "123-456-7890", "email@example.com", "www.example.com",
                  "default_logo.png"))


    def get_hotel_info(self, hotel_id):
        """Retrieve hotel information by ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM HOTEL WHERE HOTEL_ID=?", (hotel_id,))
            hotel_info = cursor.fetchone()
            if hotel_info:
                return {
                    "HOTEL_ID": hotel_info[0],
                    "HOTEL_NAME": hotel_info[1],
                    "ADDRESS": hotel_info[2],
                    "FLOORS": hotel_info[3],
                    "PHONE_NUMBER": hotel_info[4],
                    "EMAIL": hotel_info[5],
                    "WEBSITE": hotel_info[6],
                    "LOGO_PATH": hotel_info[7],
                    "CREATED_AT": hotel_info[8],
                    "UPDATED_AT": hotel_info[9]
                }
            else:
                log(f"Hotel with ID {hotel_id} not found.")
                return None


    def update_hotel_info(self, hotel_id, hotel_data):
        """Update hotel information"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE HOTEL SET 
                    HOTEL_NAME=?, ADDRESS=?, FLOORS=?, PHONE_NUMBER=?, 
                    EMAIL=?, WEBSITE=?, LOGO_PATH=?, UPDATED_AT=CURRENT_TIMESTAMP 
                WHERE HOTEL_ID=?
            """, (
                hotel_data["HOTEL_NAME"],
                hotel_data["ADDRESS"],
                hotel_data["FLOORS"],
                hotel_data["PHONE_NUMBER"],
                hotel_data["EMAIL"],
                hotel_data["WEBSITE"],
                hotel_data["LOGO_PATH"],
                hotel_id
            ))
            conn.commit()
            log(f"Hotel {hotel_id} updated successfully.")



if __name__ == "__main__":
    main()