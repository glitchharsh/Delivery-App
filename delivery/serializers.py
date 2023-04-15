from rest_framework import serializers
from delivery.models import TransportRequest, RiderTravelInfo

class TransportRequestSerializer(serializers.ModelSerializer):
    # serializer for the requests model

    requested_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.CharField(read_only=True)
    class Meta:
        model = TransportRequest
        fields = '__all__'

class RiderTravelInfoSerializer(serializers.ModelSerializer):
    # serializer for the rides model

    status = serializers.CharField(read_only=True)
    class Meta:
        model = RiderTravelInfo
        fields = '__all__'

class RiderTravelInfoWriteSerializer(RiderTravelInfoSerializer):
    # extends RiderTravelInfoSerializer but hides the rider info

    uploaded_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
