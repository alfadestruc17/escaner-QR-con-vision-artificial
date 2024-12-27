import mysql.connector
import logging
from datetime import datetime
from models.config import DB_CONFIG

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            self._create_tables()
            self._add_data_columns()
        except mysql.connector.Error as err:
            logging.error(f"Database connection error: {err}")
            raise

    def _create_tables(self):
        try:
            # QR codes table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS qr_codes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    qr_data VARCHAR(255) NOT NULL,
                    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    created_by VARCHAR(100)
                )
            """)

            # Scans table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    scan_id INT AUTO_INCREMENT PRIMARY KEY,
                    qr_id INT,
                    scan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    scan_location VARCHAR(100),
                    FOREIGN KEY (qr_id) REFERENCES qr_codes(id)
                )
            """)

            # Entry records table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    entry_id INT AUTO_INCREMENT PRIMARY KEY,
                    qr_id INT,
                    entry_date DATE,
                    entry_time TIME,
                    FOREIGN KEY (qr_id) REFERENCES qr_codes(id),
                    UNIQUE KEY unique_entry (qr_id, entry_date)
                )
            """)
            
            self.conn.commit()
        except mysql.connector.Error as err:
            logging.error(f"Error creating tables: {err}")
            raise

    def _add_data_columns(self):
        try:
            # Add scan_data column to scans table if it doesn't exist
            self.cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name = 'scans' 
                AND column_name = 'scan_data'
            """)
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    ALTER TABLE scans
                    ADD COLUMN scan_data TEXT
                """)

            # Add entry_data column to entries table if it doesn't exist
            self.cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name = 'entries' 
                AND column_name = 'entry_data'
            """)
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    ALTER TABLE entries
                    ADD COLUMN entry_data TEXT
                """)

            self.conn.commit()
        except mysql.connector.Error as err:
            logging.error(f"Error adding data columns: {err}")
            raise

    def close(self):
        self.cursor.close()
        self.conn.close()