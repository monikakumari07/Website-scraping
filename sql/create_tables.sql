CREATE DATABASE website_data;
USE website_data;

CREATE TABLE `website_data`.`website_info` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    robots_url VARCHAR(255),
    sitemap_url VARCHAR(255),
    contact_email VARCHAR(255),
    contact_address TEXT,
    contact_number VARCHAR(50),
    language VARCHAR(50),
    cms_mvc VARCHAR(100),
    category VARCHAR(100)
);
