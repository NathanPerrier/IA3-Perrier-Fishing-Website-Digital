from django.db import models


class Routes(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    previous_url = models.CharField(max_length=255)
    current_url = models.CharField(max_length=255)
    time_spent = models.FloatField()
    method = models.CharField(max_length=10, default='GET')
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        db_table = 'routes'
        verbose_name = 'Routes'
        verbose_name_plural = 'User Routes'
        
    def __str__(self):
        return self.current_url

class LoginLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
class UserLocationLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_location_log'
        verbose_name = 'User Location Log'
        verbose_name_plural = 'User Location Logs'
        
    def __str__(self):
        return self.user