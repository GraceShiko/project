from datetime import datetime, timezone
from decimal import Decimal

from rest_framework import serializers

from measurements.models import GpsMeasurement


class GpsMeasurementSerializer(serializers.Serializer):

    lat = serializers.CharField()
    long = serializers.CharField()
    level = serializers.CharField()

    def validate_lat(self, value):
        value = Decimal(value)
        if abs(value) >= 180.:
            raise serializers.ValidationError('Latitude is incorrect: {}'.format(value));
        return value

    def validate_long(self, value):
        value = Decimal(value)
        if abs(value) >= 90.:
            raise serializers.ValidationError('Longitude is incorrect: {}'.format(value));
        return value

    def validate_level(self, value):
        value = Decimal(value)
        if abs(value) > 600:
            raise serializers.ValidationError('level is incorrect: {}'.format(value));
        return value


    def create(self, validated_data):
        obj, created = GpsMeasurement.objects.get_or_create(
            device=self.context['device'],
            latitude=validated_data['lat'],
            longitude=validated_data['long'],
            water_level=validated_data['level'],
            date_collected=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        )

        return obj

