import mysql.connector
from mysql.connector import Error
import os

# Database configuration (using env vars or defaults)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "masteradmin")
DB_NAME = os.getenv("DB_NAME", "cardiosense")

def init_db():
    """Create tables if they don't exist."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r") as f:
            schema = f.read()
        
        # Split by semicolon and execute each command
        for command in schema.split(";"):
            if command.strip():
                cursor.execute(command)
        conn.commit()
        print("Database initialized successfully.")
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_db_connection():
    """Establish and return a MySQL connection."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def insert_prediction_transaction(patient_id, features, probabilities, final_risk):
    """
    Inserts data into PATIENT, HEART_SOUND, and PREDICTION tables atomically.
    Demonstrates MySQL Transactions with ROLLBACK.
    """
    conn = get_db_connection()
    if not conn:
        return False
        
    try:
        # Start transaction
        conn.autocommit = False
        cursor = conn.cursor()
        
        # 1. Insert Patient
        cursor.execute("INSERT INTO PATIENT (source_file, notes) VALUES (%s, %s)", ('api_input', 'New patient record via API'))
        actual_patient_id = cursor.lastrowid
        
        # 2. Insert Heart Sound Features
        hs_query = """
        INSERT INTO HEART_SOUND 
        (patient_id, s1_duration_sec, s1_amplitude, s1_area, s2_duration_sec, 
         s2_amplitude, s2_area, systole_duration_sec, diastole_duration_sec) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        hs_values = (
            actual_patient_id, features['s1_duration_sec'], features['s1_amplitude'], 
            features['s1_area'], features['s2_duration_sec'], features['s2_amplitude'], 
            features['s2_area'], features['systole_duration_sec'], features['diastole_duration_sec']
        )
        cursor.execute(hs_query, hs_values)
        sound_id = cursor.lastrowid
        
        # 3. Insert Prediction Results
        pred_query = """
        INSERT INTO PREDICTION 
        (sound_id, rf_probability, xgb_probability, lgbm_probability, 
         ensemble_probability, final_risk_level) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        pred_values = (
            sound_id, probabilities['rf'], probabilities['xgb'], 
            probabilities['lgbm'], probabilities['ensemble'], final_risk
        )
        cursor.execute(pred_query, pred_values)
        
        # Commit transaction
        conn.commit()
        return True
        
    except Error as e:
        print(f"Transaction Failed, Rolling Back: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_prediction_history(limit=50):
    """Fetches the most recent prediction records with patient and heart sound details."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT 
            p.id as patient_id,
            p.created_at,
            hs.s1_duration_sec,
            hs.s2_duration_sec,
            hs.systole_duration_sec,
            hs.diastole_duration_sec,
            pr.ensemble_probability,
            pr.final_risk_level
        FROM PATIENT p
        JOIN HEART_SOUND hs ON p.id = hs.patient_id
        JOIN PREDICTION pr ON hs.id = pr.sound_id
        ORDER BY p.created_at DESC
        LIMIT %s
        """
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error fetching history: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
