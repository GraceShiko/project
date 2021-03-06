from django.db import models

from devices.models import Device


class GpsMeasurement(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='gps_measurement_set')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    water_level = models.DecimalField(max_digits=6, decimal_places=2,default=0.0)
    date_collected = models.DateTimeField()
    date_received = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['date_collected']),
            models.Index(fields=['device', 'date_collected']),
        ]
        ordering = [
            '-date_collected',
        ]

    def __str__(self):
        return 'GPS measurement for device {}: {} {} {} {}'.format(
            self.device,
            self.date_collected,
            self.latitude,
            self.longitude,
            self.water_level,
        )

