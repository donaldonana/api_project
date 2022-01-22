from rest_framework import serializers

from rest_api import models



# for nested self-referential
class AbonnementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ( 'id', 'email', 'nom', 'prenom', 'phone')
      
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""

    def __init__(self, *args, **kwargs):
        super(UserProfileSerializer, self).__init__(*args, **kwargs)
        if self.context["request"].method == "PUT":
            self.fields.pop("password")

    abonnements = AbonnementsSerializer(many = True, read_only = True)


    class Meta:

        model = models.UserProfile
        fields = ('id', 'email', 'nom', 'prenom','password', 'phone', 'abonnements')
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
            nom =  validated_data['nom'],
            # abonnements = validated_data['abonnements'],
            phone =  validated_data['phone'],
            password = validated_data['password']
        )

        return user



class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    model = models.UserProfile
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



class DocumentSerializer(serializers.ModelSerializer):
    """docstring for DocuemntSerializer"""

    class Meta:

        model = models.Document
        fields = ('id', 
            'titre', 
            'categorie', 
            'descriptions',
            'date', 
            'contenu', 
            'Type',
            'tags',
            'user')


class LikeSerializer(serializers.ModelSerializer):
    """docstring for DocuemntSerializer"""

    class Meta:

        model = models.Like
        fields = ('id', 
            'user', 
            'document')

class CommentaireSerializer(serializers.ModelSerializer):
    """docstring for DocuemntSerializer"""

    class Meta:

        model = models.Commentaire
        fields = ('id', 
            'user', 
            'document')


        
    
        