from rest_framework import serializers
from dbmodels.models import Movements

class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movements
        fields = '__all__'
        read_only_fields = ['id', 'token', 'date']