from utils.helpers import log, get_connection
from datetime import datetime


def main():
    settings_model = SettingsModel()
    settings_model.create_default_settings()


class SettingsModel:
    def __init__(self):
        self.create_settings_tables()

    def create_settings_tables(self):
        """Create the settings tables"""
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS BILLING_SETTINGS (
                    BILLING_SETTING_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    SETTING_KEY TEXT NOT NULL UNIQUE,
                    SETTING_VALUE TEXT NOT NULL,
                    SETTING_TYPE TEXT DEFAULT 'DECIMAL',
                    DESCRIPTION TEXT,
                    IS_ACTIVE BOOLEAN DEFAULT 1,
                    CREATED_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UPDATED_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            log("Settings tables created successfully.")

    def create_default_settings(self):
        """Create default billing settings"""
        try:
            # Default billing settings
            default_billing_settings = [
                ('TAX_RATE', '0.12', 'DECIMAL', 'Default tax rate applied to all transactions (12%)'),
                ('SERVICE_CHARGE', '0.10', 'DECIMAL', 'Service charge applied to room bookings (10%)'),
                ('LATE_CHECKOUT_FEE', '50.00', 'DECIMAL', 'Fee charged for late checkout beyond standard time'),
                ('EARLY_CHECKIN_FEE', '25.00', 'DECIMAL', 'Fee charged for early check-in before standard time'),
                ('NO_SHOW_CHARGE', '100.00', 'DECIMAL', 'Charge applied when guest does not show up'),
                ('DEPOSIT_REQUIRED', 'true', 'BOOLEAN', 'Whether a deposit is required for new reservations'),
                ('DEPOSIT_AMOUNT', '50.00', 'DECIMAL', 'Fixed deposit amount required for reservations'),
                ('DEPOSIT_PERCENTAGE', '20.00', 'DECIMAL', 'Deposit as percentage of total booking amount'),
                ('PAYMENT_GRACE_PERIOD', '3', 'INTEGER', 'Number of days grace period for payment after checkout'),
                ('INVOICE_DUE_DAYS', '30', 'INTEGER', 'Number of days until invoice payment is due'),
                ('LATE_PAYMENT_FEE', '25.00', 'DECIMAL', 'Fee charged for payments made after due date'),
                ('REFUND_PROCESSING_DAYS', '7', 'INTEGER', 'Number of business days to process refunds'),
                ('CURRENCY_SYMBOL', '₱', 'TEXT', 'Currency symbol displayed in all financial transactions'),
                ('DECIMAL_PLACES', '2', 'INTEGER', 'Number of decimal places for currency display'),
                ('DEFAULT_EXTRA_ADULT_RATE', '25.00', 'DECIMAL', 'Default rate for extra adults when room type has no rate'),
                ('DEFAULT_EXTRA_CHILD_RATE', '15.00', 'DECIMAL', 'Default rate for extra children when room type has no rate'),
                ('AUTO_GENERATE_INVOICE', 'true', 'BOOLEAN', 'Automatically generate invoice when reservation is confirmed'),
                ('INVOICE_PREFIX', 'INV', 'TEXT', 'Prefix for invoice numbers'),
                ('PAYMENT_TOLERANCE', '0.01', 'DECIMAL', 'Tolerance for payment amount differences (rounding)')
            ]

            # Insert billing settings
            for key, value, type_, description in default_billing_settings:
                self.add_or_update_billing_setting(key, value, type_, description)

            log("Default settings created successfully")

        except Exception as e:
            log(f"Error creating default settings: {str(e)}", "ERROR")

    def add_or_update_billing_setting(self, key, value, setting_type='DECIMAL', description=None):
        """Add or update a billing setting"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO BILLING_SETTINGS 
                    (SETTING_KEY, SETTING_VALUE, SETTING_TYPE, DESCRIPTION, UPDATED_DATE)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (key, str(value), setting_type, description))
                conn.commit()
                log(f"Billing setting {key} updated to {value}")
                return True
        except Exception as e:
            log(f"Error updating billing setting {key}: {str(e)}", "ERROR")
            return False

    def get_billing_setting(self, key, default_value=None):
        """Get a billing setting value"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT SETTING_VALUE, SETTING_TYPE 
                    FROM BILLING_SETTINGS 
                    WHERE SETTING_KEY = ? AND IS_ACTIVE = 1
                """, (key,))
                result = cursor.fetchone()

                if result:
                    value, type_ = result
                    return self._convert_setting_value(value, type_)
                return default_value
        except Exception as e:
            log(f"Error getting billing setting {key}: {str(e)}", "ERROR")
            return default_value

    def get_all_billing_settings(self):
        """Get all billing settings"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT SETTING_KEY, SETTING_VALUE, SETTING_TYPE, DESCRIPTION
                    FROM BILLING_SETTINGS 
                    WHERE IS_ACTIVE = 1
                    ORDER BY SETTING_KEY
                """)
                return cursor.fetchall()
        except Exception as e:
            log(f"Error getting billing settings: {str(e)}", "ERROR")
            return []

    def get_settings_by_keys(self, keys, table='general'):
        """Get multiple settings by their keys"""
        try:
            if not keys:
                return {}

            placeholders = ','.join(['?' for _ in keys])

            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(f"""
                        SELECT SETTING_KEY, SETTING_VALUE, SETTING_TYPE 
                        FROM BILLING_SETTINGS 
                        WHERE SETTING_KEY IN ({placeholders}) AND IS_ACTIVE = 1
                    """, keys)

                results = {}
                for key, value, type_ in cursor.fetchall():
                    results[key] = self._convert_setting_value(value, type_)

                return results
        except Exception as e:
            log(f"Error getting settings by keys: {str(e)}", "ERROR")
            return {}

    def update_multiple_billing_settings(self, settings_dict):
        """Update multiple billing settings at once"""
        try:
            success_count = 0
            for key, value_data in settings_dict.items():
                if isinstance(value_data, dict):
                    value = value_data.get('value')
                    setting_type = value_data.get('type', 'DECIMAL')
                    description = value_data.get('description')
                else:
                    value = value_data
                    setting_type = self._infer_setting_type(value)
                    description = None

                if self.add_or_update_billing_setting(key, value, setting_type, description):
                    success_count += 1

            log(f"Updated {success_count}/{len(settings_dict)} billing settings")
            return success_count == len(settings_dict)
        except Exception as e:
            log(f"Error updating multiple billing settings: {str(e)}", "ERROR")
            return False

    def delete_billing_setting(self, key):
        """Delete a billing setting (set as inactive)"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE BILLING_SETTINGS 
                    SET IS_ACTIVE = 0, UPDATED_DATE = CURRENT_TIMESTAMP
                    WHERE SETTING_KEY = ?
                """, (key,))
                conn.commit()
                log(f"Billing setting {key} deleted")
                return cursor.rowcount > 0
        except Exception as e:
            log(f"Error deleting billing setting {key}: {str(e)}", "ERROR")
            return False

    def reset_to_defaults(self, category=None):
        """Reset settings to default values"""
        try:
            if category == 'billing' or category is None:
                # Reset billing settings
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM BILLING_SETTINGS")
                    conn.commit()

            # Recreate defaults
            self.create_default_settings()
            log(f"Settings reset to defaults for category: {category or 'all'}")
            return True
        except Exception as e:
            log(f"Error resetting settings: {str(e)}", "ERROR")
            return False

    def export_settings(self):
        """Export all settings to a dictionary"""
        try:
            export_data = {
                'billing_settings': {},
                'export_date': datetime.now().isoformat()
            }

            # Export billing settings
            billing_settings = self.get_all_billing_settings()
            for key, value, type_, description in billing_settings:
                export_data['billing_settings'][key] = {
                    'value': value,
                    'type': type_,
                    'description': description
                }

            return export_data
        except Exception as e:
            log(f"Error exporting settings: {str(e)}", "ERROR")
            return None

    def import_settings(self, settings_data):
        """Import settings from a dictionary"""
        try:
            billing_success = True

            if 'billing_settings' in settings_data:
                billing_success = self.update_multiple_billing_settings(settings_data['billing_settings'])

            return billing_success
        except Exception as e:
            log(f"Error importing settings: {str(e)}", "ERROR")
            return False

    def _convert_setting_value(self, value, setting_type):
        """Convert setting value to appropriate Python type"""
        try:
            if setting_type == 'BOOLEAN':
                return value.lower() in ('true', '1', 'yes', 'on')
            elif setting_type == 'INTEGER':
                return int(value)
            elif setting_type == 'DECIMAL':
                return float(value)
            else:
                return value
        except (ValueError, AttributeError):
            return value

    def _infer_setting_type(self, value):
        """Infer the setting type from the value"""
        if isinstance(value, bool):
            return 'BOOLEAN'
        elif isinstance(value, int):
            return 'INTEGER'
        elif isinstance(value, float):
            return 'DECIMAL'
        else:
            return 'TEXT'


if __name__ == "__main__":
    main()
