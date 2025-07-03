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

    def create_default_hotel(self):
        """Add a new hotel to the database"""
        with get_connection() as conn:
            cursor = conn.cursor()

            # Insert hotel
            cursor.execute("""
                INSERT OR IGNORE INTO HOTEL (HOTEL_NAME, ADDRESS, FLOORS, PHONE_NUMBER, EMAIL, WEBSITE, LOGO_PATH)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ("The Reverie Hotel", "123 Default St", 6, "123-456-7890", "email@example.com", "www.example.com",
                  "default_logo.png"))

            hotel_id = cursor.lastrowid if cursor.lastrowid else 1
            log(f"Default hotel created with ID: {hotel_id}")
            conn.commit()


    def get_hotel_info(self, hotel_id):
        """Get basic hotel information"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM HOTEL WHERE HOTEL_ID = ?
            """, (hotel_id,))
            result = cursor.fetchone()

            if result:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, result))
            return None

    def update_hotel_info(self, hotel_id, hotel_data):
        """Update basic hotel information"""
        with get_connection() as conn:
            cursor = conn.cursor()

            updates = []
            params = []

            allowed_fields = ['HOTEL_NAME', 'ADDRESS', 'FLOORS', 'PHONE_NUMBER', 'EMAIL', 'WEBSITE', 'LOGO_PATH']

            for field in allowed_fields:
                if field in hotel_data:
                    updates.append(f"{field} = ?")
                    params.append(hotel_data[field])

            if updates:
                updates.append("UPDATED_AT = CURRENT_TIMESTAMP")
                params.append(hotel_id)

                cursor.execute(f"""
                    UPDATE HOTEL 
                    SET {', '.join(updates)}
                    WHERE HOTEL_ID = ?
                """, params)
                conn.commit()
                log(f"Hotel {hotel_id} information updated successfully")
                return True
            return False



if __name__ == "__main__":
    main()