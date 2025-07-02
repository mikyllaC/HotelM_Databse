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

            # Create HOTEL_SETTINGS table for configuration
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS HOTEL_SETTINGS (
                    SETTING_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    HOTEL_ID INTEGER NOT NULL,
                    SETTING_KEY TEXT NOT NULL,
                    SETTING_VALUE TEXT NOT NULL,
                    SETTING_TYPE TEXT DEFAULT 'TEXT',
                    DESCRIPTION TEXT,
                    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (HOTEL_ID) REFERENCES HOTEL(HOTEL_ID),
                    UNIQUE(HOTEL_ID, SETTING_KEY)
                )
            """)

            conn.commit()

    def create_default_hotel(self):
        """Add a new hotel to the database with default settings"""
        with get_connection() as conn:
            cursor = conn.cursor()

            # Insert hotel
            cursor.execute("""
                INSERT OR IGNORE INTO HOTEL (HOTEL_NAME, ADDRESS, FLOORS, PHONE_NUMBER, EMAIL, WEBSITE, LOGO_PATH)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ("The Reverie Hotel", "123 Default St", 6, "123-456-7890", "email@example.com", "www.example.com",
                  "default_logo.png"))

            hotel_id = cursor.lastrowid if cursor.lastrowid else 1

            # Insert default settings
            default_settings = [
                ('TAX_RATE', '0.12', 'DECIMAL', 'Default tax rate (12%)'),
                ('CURRENCY', 'USD', 'TEXT', 'Hotel currency'),
                ('CHECK_IN_TIME', '15:00', 'TIME', 'Standard check-in time'),
                ('CHECK_OUT_TIME', '11:00', 'TIME', 'Standard check-out time'),
                ('CANCELLATION_HOURS', '24', 'INTEGER', 'Hours before check-in for free cancellation'),
                ('LATE_CHECKOUT_FEE', '50.00', 'DECIMAL', 'Late checkout fee'),
                ('EARLY_CHECKIN_FEE', '25.00', 'DECIMAL', 'Early check-in fee'),
                ('NO_SHOW_CHARGE', '100', 'DECIMAL', 'No-show charge percentage'),
                ('DEPOSIT_REQUIRED', 'true', 'BOOLEAN', 'Require deposit for reservations'),
                ('DEPOSIT_AMOUNT', '50.00', 'DECIMAL', 'Default deposit amount'),
                ('MAX_OCCUPANCY_BUFFER', '2', 'INTEGER', 'Max additional guests allowed'),
                ('SERVICE_CHARGE', '0.10', 'DECIMAL', 'Service charge rate (10%)'),
                ('BUSINESS_HOURS_START', '06:00', 'TIME', 'Business hours start'),
                ('BUSINESS_HOURS_END', '23:00', 'TIME', 'Business hours end')
            ]

            for key, value, type_, desc in default_settings:
                cursor.execute("""
                    INSERT OR IGNORE INTO HOTEL_SETTINGS 
                    (HOTEL_ID, SETTING_KEY, SETTING_VALUE, SETTING_TYPE, DESCRIPTION)
                    VALUES (?, ?, ?, ?, ?)
                """, (hotel_id, key, value, type_, desc))

            conn.commit()
            log("Default hotel with settings created successfully.")

    def get_hotel_setting(self, hotel_id, setting_key):
        """Get a specific hotel setting"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SETTING_VALUE, SETTING_TYPE 
                FROM HOTEL_SETTINGS 
                WHERE HOTEL_ID = ? AND SETTING_KEY = ?
            """, (hotel_id, setting_key))
            result = cursor.fetchone()

            if result:
                value, type_ = result
                # Convert based on type
                if type_ == 'DECIMAL':
                    return float(value)
                elif type_ == 'INTEGER':
                    return int(value)
                elif type_ == 'BOOLEAN':
                    return value.lower() in ('true', '1', 'yes')
                else:
                    return value
            return None

    def update_hotel_setting(self, hotel_id, setting_key, setting_value, setting_type='TEXT', description=None):
        """Update or insert a hotel setting"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO HOTEL_SETTINGS 
                (HOTEL_ID, SETTING_KEY, SETTING_VALUE, SETTING_TYPE, DESCRIPTION, UPDATED_AT)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (hotel_id, setting_key, str(setting_value), setting_type, description))
            conn.commit()
            log(f"Hotel setting {setting_key} updated to {setting_value}")

    def get_all_hotel_settings(self, hotel_id):
        """Get all settings for a hotel"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SETTING_KEY, SETTING_VALUE, SETTING_TYPE, DESCRIPTION 
                FROM HOTEL_SETTINGS 
                WHERE HOTEL_ID = ?
                ORDER BY SETTING_KEY
            """, (hotel_id,))
            return cursor.fetchall()

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