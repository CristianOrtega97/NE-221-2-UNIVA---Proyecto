-- USER CREATION 
CREATE TABLE `leadmanager`.`user` 
( `id` INT NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(100) NOT NULL ,
  `user_name` VARCHAR(100) NOT NULL ,
  `password` VARCHAR(100) NOT NULL ,
  `role` SMALLINT NOT NULL ,
  `is_active` BOOLEAN NOT NULL DEFAULT TRUE ,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP on update CURRENT_TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)) ENGINE = InnoDB;

-- INSERT INTO USER
INSERT INTO `user` (`id`, `name`, `user_name`, `password`, `role`, `is_active`, `created_at`, `updated_at`)
VALUES (NULL, 'Emanuel Company', 'mezcal_company', '123456', '1', '1', current_timestamp(), current_timestamp());

INSERT INTO `user` (`id`, `name`, `user_name`, `password`, `role`, `is_active`, `created_at`, `updated_at`)
VALUES (NULL, 'Emanuel Agent', 'mezcal_agent', '123456', '2', '1', current_timestamp(), current_timestamp());

INSERT INTO `user` (`id`, `name`, `user_name`, `password`, `role`, `is_active`, `created_at`, `updated_at`)
VALUES (NULL, 'Emanuel Camarena', 'mezcal_admin', '123456', '3', '1', current_timestamp(), current_timestamp());

INSERT INTO `user` (`id`, `name`, `user_name`, `password`, `role`, `is_active`, `created_at`, `updated_at`) 
VALUES (NULL, 'Carlos Company', 'charles_company', '123456', '1', '1', current_timestamp(), NULL);
-- lEAD Table
CREATE TABLE `leadmanager`.`lead` 
( `id` INT NOT NULL AUTO_INCREMENT ,
  `first_name` VARCHAR(100) NOT NULL ,
  `last_name` VARCHAR(100) NOT NULL ,
  `phone` INT NOT NULL ,
  `insurance` BOOLEAN NOT NULL DEFAULT TRUE ,
  `company_id` INT NOT NULL,
  `is_active` BOOLEAN NOT NULL DEFAULT TRUE ,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ,
  `updated_at` TIMESTAMP on update CURRENT_TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ,
  PRIMARY KEY (`id`)) ENGINE = InnoDB;

-- FOREIGN KEY FOR Leads to user
ALTER TABLE `lead` ADD FOREIGN KEY (`company_id`) REFERENCES `user`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Insert Lead
INSERT INTO `lead` (`id`, `first_name`, `last_name`, `phone`, `insurance`, `company_id`, `is_active`, `created_at`, `updated_at`)
VALUES (NULL, 'John', 'Johnson', '1112223344', '1', '1', '1', current_timestamp(), NULL);

INSERT INTO `lead` (`id`, `first_name`, `last_name`, `phone`, `insurance`, `company_id`, `is_active`, `created_at`, `updated_at`)
VALUES (NULL, 'Juan', 'Perez', '1112223344', '1', '4', '1', current_timestamp(), NULL);

-- VIEW FOR LEADS
CREATE VIEW lead_view
AS
SELECT lead.id as 'id',
		lead.first_name as 'first_name',
        lead.last_name as 'last_name',
        lead.phone as 'phone',
        lead.insurance as 'insurance',
        lead.is_active as 'is_active',
        user.name AS 'company_name'
FROM lead
INNER JOIN user ON lead.company_id = user.id


-- VIEW FOR USERS
CREATE VIEW user_view
AS
SELECT * FROM user
