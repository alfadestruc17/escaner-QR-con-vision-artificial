from datetime import datetime, date, time
from typing import Optional, Tuple, Dict

class QRCodeModel:
    def __init__(self, db):
        self.db = db

    def create_qr(self, qr_data: str, created_by: str) -> int:
        try:
            query = """
                INSERT INTO qr_codes (qr_data, created_by)
                VALUES (%s, %s)
            """
            self.db.cursor.execute(query, (qr_data, created_by))
            self.db.conn.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            raise Exception(f"Error creating QR code: {e}")

    def get_qr_by_data(self, qr_data: str) -> Optional[Dict]:
        try:
            query = """
                SELECT id, qr_data, created_by, creation_date 
                FROM qr_codes 
                WHERE qr_data = %s
            """
            self.db.cursor.execute(query, (qr_data,))
            result = self.db.cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'qr_data': result[1],
                    'created_by': result[2],
                    'creation_date': result[3]
                }
            return None
        except Exception as e:
            raise Exception(f"Error retrieving QR code: {e}")

    def record_scan(self, qr_id: int, location: str, qr_data: Dict) -> int:
        try:
            query = """
                INSERT INTO scans (qr_id, scan_location, scan_data)
                VALUES (%s, %s, %s)
            """
            formatted_data = (
                f"Data: {qr_data['qr_data']}\n"
                f"Created by: {qr_data['created_by']}\n"
                f"Created on: {qr_data['creation_date'].strftime('%Y-%m-%d %H:%M:%S')}"
            )
            self.db.cursor.execute(query, (qr_id, location, formatted_data))
            self.db.conn.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            raise Exception(f"Error recording scan: {e}")

    def record_entry(self, qr_id: int, qr_data: Dict) -> Tuple[bool, str]:
        try:
            current_date = date.today()
            current_time = datetime.now().time()

            # Check if entry exists
            query = """
                SELECT entry_id FROM entries 
                WHERE qr_id = %s AND entry_date = %s
            """
            self.db.cursor.execute(query, (qr_id, current_date))
            existing_entry = self.db.cursor.fetchone()

            if existing_entry:
                return False, "Entry already recorded for today"

            # Record new entry
            query = """
                INSERT INTO entries (qr_id, entry_date, entry_time, entry_data)
                VALUES (%s, %s, %s, %s)
            """
            formatted_data = (
                f"Data: {qr_data['qr_data']}\n"
                f"Created by: {qr_data['created_by']}\n"
                f"Created on: {qr_data['creation_date'].strftime('%Y-%m-%d %H:%M:%S')}"
            )
            self.db.cursor.execute(query, (qr_id, current_date, current_time, formatted_data))
            self.db.conn.commit()
            return True, "Entry recorded successfully"
        except Exception as e:
            raise Exception(f"Error recording entry: {e}")