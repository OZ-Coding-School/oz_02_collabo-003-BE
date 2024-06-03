from rest_framework.serializers import ModelSerializer
from .models import AdminSetting

#/api/v1/adms/push/
class Admin_settingsSerializer(ModelSerializer):
    '''
    admin_settings serializer
    '''

    class Meta:
        model = AdminSetting
        fields = '__all__'

