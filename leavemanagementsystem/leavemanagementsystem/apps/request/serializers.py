from rest_framework import serializers
from .models import Request


class RequestSerializer(serializers.ModelSerializer):
    """Class for serializing the user profile"""

    def __init__(self, *args, **kwargs):
        super(RequestSerializer, self).__init__(*args, **kwargs)

        for field in self.fields:
            error_messages = self.fields[field].error_messages
            error_messages['null'] = error_messages['blank'] \
                = error_messages['required'] \
                = 'Please fill in the {} field.'.format(field)

    id = serializers.CharField(required=False)
    requestor = serializers.CharField(source='requestor_id')
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    description = serializers.CharField(required=False)

    number_of_days = serializers.CharField(required=False)

    class Meta:
        model = Request
        fields = '__all__'

    def create(self, data, *args):
        """
        Method enables the creation of a request detail.
        """
        return Request.objects.create(**data)
