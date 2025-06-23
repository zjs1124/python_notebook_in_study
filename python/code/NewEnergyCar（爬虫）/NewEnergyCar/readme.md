# 1、建表语句
-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS car_data;
USE car_data;

-- 创建城市表
CREATE TABLE IF NOT EXISTS cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(50) NOT NULL UNIQUE
);

-- 插入城市数据
INSERT INTO cities (city_name) VALUES ('北京'), ('上海'), ('杭州'), ('南京'), ('合肥');

-- 创建表 car_beijing
CREATE TABLE IF NOT EXISTS car_beijing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_name VARCHAR(255) NULL,
    cards_unit VARCHAR(255) NULL,
    price VARCHAR(255) NULL,
    price_tax VARCHAR(255) NULL,
    gearbox VARCHAR(255) NULL,
    fuel_type VARCHAR(255) NULL,
    cltc_pure_electricity_endurance_mileage VARCHAR(255) NULL,
    release_time VARCHAR(255) NULL,
    annual_inspection_expiration VARCHAR(255) NULL,
    insurance_expiration VARCHAR(255) NULL,
    warranty_expiration VARCHAR(255) NULL,
    transfer_times VARCHAR(255) NULL,
    standard_fast_charge VARCHAR(255) NULL,
    engine VARCHAR(255) NULL,
    vehicle_level VARCHAR(255) NULL,
    vehicle_color VARCHAR(255) NULL,
    drive_mode VARCHAR(255) NULL,
    standard_capacity VARCHAR(255) NULL,
    standard_slow_charge VARCHAR(255) NULL,
    configuration_highlights_text VARCHAR(255) NULL,
    city_id INT NULL DEFAULT 1
);

-- 创建表 car_shanghai
CREATE TABLE IF NOT EXISTS car_shanghai (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_name VARCHAR(255) NULL,
    cards_unit VARCHAR(255) NULL,
    price VARCHAR(255) NULL,
    price_tax VARCHAR(255) NULL,
    gearbox VARCHAR(255) NULL,
    fuel_type VARCHAR(255) NULL,
    cltc_pure_electricity_endurance_mileage VARCHAR(255) NULL,
    release_time VARCHAR(255) NULL,
    annual_inspection_expiration VARCHAR(255) NULL,
    insurance_expiration VARCHAR(255) NULL,
    warranty_expiration VARCHAR(255) NULL,
    transfer_times VARCHAR(255) NULL,
    standard_fast_charge VARCHAR(255) NULL,
    engine VARCHAR(255) NULL,
    vehicle_level VARCHAR(255) NULL,
    vehicle_color VARCHAR(255) NULL,
    drive_mode VARCHAR(255) NULL,
    standard_capacity VARCHAR(255) NULL,
    standard_slow_charge VARCHAR(255) NULL,
    configuration_highlights_text VARCHAR(255) NULL,
    city_id INT NULL DEFAULT 2
);

-- 创建表 car_hangzhou
CREATE TABLE IF NOT EXISTS car_hangzhou (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_name VARCHAR(255) NULL,
    cards_unit VARCHAR(255) NULL,
    price VARCHAR(255) NULL,
    price_tax VARCHAR(255) NULL,
    gearbox VARCHAR(255) NULL,
    fuel_type VARCHAR(255) NULL,
    cltc_pure_electricity_endurance_mileage VARCHAR(255) NULL,
    release_time VARCHAR(255) NULL,
    annual_inspection_expiration VARCHAR(255) NULL,
    insurance_expiration VARCHAR(255) NULL,
    warranty_expiration VARCHAR(255) NULL,
    transfer_times VARCHAR(255) NULL,
    standard_fast_charge VARCHAR(255) NULL,
    engine VARCHAR(255) NULL,
    vehicle_level VARCHAR(255) NULL,
    vehicle_color VARCHAR(255) NULL,
    drive_mode VARCHAR(255) NULL,
    standard_capacity VARCHAR(255) NULL,
    standard_slow_charge VARCHAR(255) NULL,
    configuration_highlights_text VARCHAR(255) NULL,
    city_id INT NULL DEFAULT 3
);

-- 创建表 car_nanjing
CREATE TABLE IF NOT EXISTS car_nanjing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_name VARCHAR(255) NULL,
    cards_unit VARCHAR(255) NULL,
    price VARCHAR(255) NULL,
    price_tax VARCHAR(255) NULL,
    gearbox VARCHAR(255) NULL,
    fuel_type VARCHAR(255) NULL,
    cltc_pure_electricity_endurance_mileage VARCHAR(255) NULL,
    release_time VARCHAR(255) NULL,
    annual_inspection_expiration VARCHAR(255) NULL,
    insurance_expiration VARCHAR(255) NULL,
    warranty_expiration VARCHAR(255) NULL,
    transfer_times VARCHAR(255) NULL,
    standard_fast_charge VARCHAR(255) NULL,
    engine VARCHAR(255) NULL,
    vehicle_level VARCHAR(255) NULL,
    vehicle_color VARCHAR(255) NULL,
    drive_mode VARCHAR(255) NULL,
    standard_capacity VARCHAR(255) NULL,
    standard_slow_charge VARCHAR(255) NULL,
    configuration_highlights_text VARCHAR(255) NULL,
    city_id INT NULL DEFAULT 4
);

-- 创建表 car_hefei
CREATE TABLE IF NOT EXISTS car_hefei (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_name VARCHAR(255) NULL,
    cards_unit VARCHAR(255) NULL,
    price VARCHAR(255) NULL,
    price_tax VARCHAR(255) NULL,
    gearbox VARCHAR(255) NULL,
    fuel_type VARCHAR(255) NULL,
    cltc_pure_electricity_endurance_mileage VARCHAR(255) NULL,
    release_time VARCHAR(255) NULL,
    annual_inspection_expiration VARCHAR(255) NULL,
    insurance_expiration VARCHAR(255) NULL,
    warranty_expiration VARCHAR(255) NULL,
    transfer_times VARCHAR(255) NULL,
    standard_fast_charge VARCHAR(255) NULL,
    engine VARCHAR(255) NULL,
    vehicle_level VARCHAR(255) NULL,
    vehicle_color VARCHAR(255) NULL,
    drive_mode VARCHAR(255) NULL,
    standard_capacity VARCHAR(255) NULL,
    standard_slow_charge VARCHAR(255) NULL,
    configuration_highlights_text VARCHAR(255) NULL,
    city_id INT NULL DEFAULT 5
);



# hive数仓分层
