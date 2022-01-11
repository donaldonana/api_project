from rest_framework import serializers

from rest_api import models



class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""

    def __init__(self, *args, **kwargs):
        super(UserProfileSerializer, self).__init__(*args, **kwargs)
        if self.context["request"].method == "PUT":
            self.fields.pop("password")

    class Meta:

        model = models.UserProfile
        fields = fields = ('id', 'email', 'last_name', 'first_name','password', 'phone')
        extra_kwargs = {
            'password' : {
                'write_only' : True,
                'style' : {
                    'input_type' : 'password'
                }
            }
        }

    def create(self, validated_data):
        """create the return new user"""

        user = models.UserProfile.objects.create_user(
            email =  validated_data['email'],
            last_name =  validated_data['last_name'],
            phone =  validated_data['phone'],
            password = validated_data['password']
        )

        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = models.UserProfile

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



