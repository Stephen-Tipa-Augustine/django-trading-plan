from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class InfoFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Info
        fields = '__all__'


class ActualReturnsFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActualReturns
        fields = '__all__'
