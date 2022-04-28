from habitation.ads.models import AD
from rest_framework import serializers



class ADSerializer(serializers.ModelSerializer):
    class Meta:
        model = AD
        fields = '__all__'