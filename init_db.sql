CREATE DATABASE IF NOT EXISTS tracking_system DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE tracking_system;

CREATE TABLE IF NOT EXISTS apps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app_name VARCHAR(100) NOT NULL COMMENT '应用名称',
    app_key VARCHAR(64) UNIQUE NOT NULL COMMENT '应用Key',
    app_secret VARCHAR(128) NOT NULL COMMENT '应用密钥',
    description TEXT COMMENT '应用描述',
    status TINYINT DEFAULT 1 COMMENT '状态:1-启用,0-禁用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_app_key (app_key),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='应用表';

CREATE TABLE IF NOT EXISTS tracking_events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    app_key VARCHAR(64) NOT NULL COMMENT '应用Key',
    user_id VARCHAR(64) COMMENT '用户ID',
    device_id VARCHAR(128) NOT NULL COMMENT '设备ID',
    event_type VARCHAR(50) NOT NULL COMMENT '事件类型',
    event_name VARCHAR(100) NOT NULL COMMENT '事件名称',
    properties JSON COMMENT '事件属性',
    page_url VARCHAR(500) COMMENT '页面URL',
    referrer VARCHAR(500) COMMENT '来源页面',
    platform VARCHAR(20) COMMENT '平台',
    os_version VARCHAR(50) COMMENT '系统版本',
    app_version VARCHAR(50) COMMENT '应用版本',
    ip VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT 'User Agent',
    event_time DATETIME NOT NULL COMMENT '事件时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_app_key_time (app_key, event_time),
    INDEX idx_event_type_time (event_type, event_time),
    INDEX idx_user_id (user_id),
    INDEX idx_device_id (device_id),
    INDEX idx_event_time (event_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='埋点事件表';