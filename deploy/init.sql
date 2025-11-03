-- Database initialization script for development
-- Creates the existing schema structure

CREATE DATABASE IF NOT EXISTS move_acces CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE move_acces;

-- 1) Users table
CREATE TABLE IF NOT EXISTS users (
  user_id           INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nom               VARCHAR(80)      NOT NULL,
  prenom            VARCHAR(80)      NOT NULL,
  date_naissance    DATE             NOT NULL,
  rue               VARCHAR(120)     NOT NULL,
  npa               CHAR(4)          NOT NULL,
  localite          VARCHAR(80)      NOT NULL,
  tel               VARCHAR(24)      NULL,
  email             VARCHAR(254)     NOT NULL UNIQUE,
  created_at        DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at        DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 2) Access app table (login credentials)
CREATE TABLE IF NOT EXISTS acces_app (
  email          VARCHAR(254)  NOT NULL,
  password_hash  VARCHAR(255)  NOT NULL,
  PRIMARY KEY (email),
  CONSTRAINT fk_accesapp_user_email
    FOREIGN KEY (email) REFERENCES users(email)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 3) Subscriptions table
CREATE TABLE IF NOT EXISTS abonnement (
  abo_id             BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  abo_id_actual      VARCHAR(64)   NULL UNIQUE,
  user_id            INT UNSIGNED  NOT NULL,
  abo_state          ENUM('active','paused','expired','canceled','pending') NOT NULL DEFAULT 'pending',
  abo_name           VARCHAR(80)   NOT NULL,
  abo_date_start     DATE          NULL,
  abo_date_creation  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  abo_date_stop      DATE          NULL,
  abo_duration       INT UNSIGNED  NULL,
  abo_renew          TINYINT(1)    NOT NULL DEFAULT 0,
  abo_price          DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  abo_discount       DECIMAL(5,2)  NOT NULL DEFAULT 0.00,
  abo_slices         INT UNSIGNED  NULL,
  abo_price_finances DECIMAL(10,2) NULL,
  created_at         DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at         DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_abonnement_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  INDEX idx_abon_user_state (user_id, abo_state),
  INDEX idx_abon_stop (abo_date_stop)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 4) Audit logs table (NEW - created by backend)
CREATE TABLE IF NOT EXISTS audit_logs (
  id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id       INT UNSIGNED  NULL,
  action        VARCHAR(100)  NOT NULL,
  ip_address    VARCHAR(45)   NULL,
  user_agent    TEXT          NULL,
  details       TEXT          NULL,
  created_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_audit_user (user_id),
  INDEX idx_audit_action (action),
  INDEX idx_audit_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
