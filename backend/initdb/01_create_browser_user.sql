-- Convenience user for phpMyAdmin/browser access without a password.
CREATE USER IF NOT EXISTS 'browser_nopass'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON arpra_voc.* TO 'browser_nopass'@'%';
FLUSH PRIVILEGES;
