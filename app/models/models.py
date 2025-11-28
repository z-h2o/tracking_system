from django.db import models
from datetime import datetime

class App(models.Model):
    """应用模型"""
    id = models.AutoField(primary_key=True)
    app_name = models.CharField(max_length=100, verbose_name='应用名称')
    app_key = models.CharField(max_length=64, unique=True, verbose_name='应用Key')
    app_secret = models.CharField(max_length=128, verbose_name='应用密钥')
    description = models.TextField(null=True, blank=True, verbose_name='应用描述')
    status = models.SmallIntegerField(default=1, verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = 'tracking'
        db_table = 'apps'
        verbose_name = '应用'
        verbose_name_plural = '应用'

class TrackingEvent(models.Model):
    """埋点事件模型"""
    id = models.BigAutoField(primary_key=True)
    app_key = models.CharField(max_length=64, verbose_name='应用Key', db_index=True)
    user_id = models.CharField(max_length=64, null=True, blank=True, verbose_name='用户ID', db_index=True)
    device_id = models.CharField(max_length=128, verbose_name='设备ID', db_index=True)
    event_type = models.CharField(max_length=50, verbose_name='事件类型', db_index=True)
    event_name = models.CharField(max_length=100, verbose_name='事件名称')
    properties = models.JSONField(null=True, blank=True, verbose_name='事件属性')
    page_url = models.CharField(max_length=500, null=True, blank=True, verbose_name='页面URL')
    referrer = models.CharField(max_length=500, null=True, blank=True, verbose_name='来源页面')
    platform = models.CharField(max_length=20, null=True, blank=True, verbose_name='平台')
    os_version = models.CharField(max_length=50, null=True, blank=True, verbose_name='系统版本')
    app_version = models.CharField(max_length=50, null=True, blank=True, verbose_name='应用版本')
    ip = models.CharField(max_length=45, null=True, blank=True, verbose_name='IP地址')
    user_agent = models.TextField(null=True, blank=True, verbose_name='User Agent')
    event_time = models.DateTimeField(verbose_name='事件时间', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        app_label = 'tracking'
        db_table = 'tracking_events'
        verbose_name = '埋点事件'
        verbose_name_plural = '埋点事件'
        indexes = [
            models.Index(fields=['app_key', 'event_time']),
            models.Index(fields=['event_type', 'event_time']),
        ]