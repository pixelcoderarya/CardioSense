-- CardioSense Database Schema (3NF)

CREATE DATABASE IF NOT EXISTS cardiosense;
USE cardiosense;

-- 1. PATIENT Table
CREATE TABLE IF NOT EXISTS PATIENT (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file VARCHAR(50) DEFAULT 'manual_entry',
    notes TEXT
);

-- 2. HEART_SOUND Table
CREATE TABLE IF NOT EXISTS HEART_SOUND (
    sound_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    s1_duration_sec FLOAT NOT NULL,
    s1_amplitude FLOAT NOT NULL,
    s1_area FLOAT NOT NULL,
    s2_duration_sec FLOAT NOT NULL,
    s2_amplitude FLOAT NOT NULL,
    s2_area FLOAT NOT NULL,
    systole_duration_sec FLOAT NOT NULL,
    diastole_duration_sec FLOAT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id) ON DELETE CASCADE
);

-- 3. MODEL_REGISTRY Table
CREATE TABLE IF NOT EXISTS MODEL_REGISTRY (
    model_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL UNIQUE,
    accuracy FLOAT NOT NULL,
    roc_auc FLOAT NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. PREDICTION Table
CREATE TABLE IF NOT EXISTS PREDICTION (
    pred_id INT AUTO_INCREMENT PRIMARY KEY,
    sound_id INT NOT NULL,
    rf_probability FLOAT NOT NULL,
    xgb_probability FLOAT NOT NULL,
    lgbm_probability FLOAT NOT NULL,
    ensemble_probability FLOAT NOT NULL,
    final_risk_level VARCHAR(20) NOT NULL, -- HIGH, MODERATE, LOW
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sound_id) REFERENCES HEART_SOUND(sound_id) ON DELETE CASCADE
);

-- 5. PREDICTION_LOG Table (for Audit Trail via Triggers)
CREATE TABLE IF NOT EXISTS PREDICTION_LOG (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    pred_id INT NOT NULL,
    final_risk_level VARCHAR(20) NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TRIGGER: Auto-log to PREDICTION_LOG after INSERT on PREDICTION
DELIMITER //
CREATE TRIGGER trg_after_prediction_insert
AFTER INSERT ON PREDICTION
FOR EACH ROW
BEGIN
    INSERT INTO PREDICTION_LOG (pred_id, final_risk_level)
    VALUES (NEW.pred_id, NEW.final_risk_level);
END;
//
DELIMITER ;

-- VIEW: HIGH_RISK_VIEW
CREATE OR REPLACE VIEW HIGH_RISK_VIEW AS
SELECT 
    p.patient_id, 
    hs.sound_id, 
    pr.ensemble_probability, 
    pr.predicted_at
FROM PATIENT p
JOIN HEART_SOUND hs ON p.patient_id = hs.patient_id
JOIN PREDICTION pr ON hs.sound_id = pr.sound_id
WHERE pr.final_risk_level = 'HIGH';
