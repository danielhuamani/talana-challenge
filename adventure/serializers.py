from rest_framework import serializers


class JourneySerializer(serializers.Serializer):
    name = serializers.CharField()
    passengers = serializers.IntegerField()


class JourneyStopSerializer(serializers.Serializer):
    end = serializers.DateField()