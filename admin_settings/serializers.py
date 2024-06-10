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

    def __init__(self, *arg, **kwargs):
        fields = kwargs.pop('fields', None)
        super(Admin_settingsSerializer, self).__init__(*arg, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

