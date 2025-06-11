CREATE TABLE credentials (
	credential_id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
	user_id INT(11),
	username VARCHAR(255),
	password VARCHAR(255),
	role VARCHAR(255),
	is_enabled TINYINT(1) DEFAULT 0,
	is_account_non_expired TINYINT(1) DEFAULT 1,
	is_account_non_locked TINYINT(1) DEFAULT 1,
	is_credentials_non_expired TINYINT(1) DEFAULT 1,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);