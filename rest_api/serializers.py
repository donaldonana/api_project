from rest_framework import serializers

from rest_api import models



# for nested self-referential
class AbonnementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ( 'id', 'email', 'nom', 'phone')
      
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if self.context["request"].method == "PUT":
            self.fields.pop("password")
        if "data" in kwargs.keys():  
            self.f = kwargs["data"]

    abonnements = AbonnementsSerializer(many = True, read_only = True)
    abonne = AbonnementsSerializer(many = True, read_only = True)
    

    class Meta:

        model = models.UserProfile
        fields = ('id', 'email', 'nom', 'prenom', 'phone', 'avatar', 
            'password', 'abonnements', 'abonne', 'Type', 'Pays' )
        extra_kwargs = {
            'password' : {
                'write_only' : True,
                'style' : {
                    'input_type' : 'password'
                }
            }, 
        }
    


    def create(self, validated_data):
        """create the return new user"""
        if self.f is not None:
            allowed = set(self.f.keys())
            existing = set(self.fields)
            for field_name in existing - allowed:
                validated_data[field_name] = None

        user = models.UserProfile.objects.create_user(
            email =  validated_data['email'],
            nom =  validated_data['nom'],
            avatar = validated_data['avatar'],
            phone =  validated_data['phone'],
            Type = validated_data["Type"],
            Pays = validated_data["Pays"],
            prenom = validated_data['prenom'],
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


class AbonnementManagementSerializer(serializers.Serializer):
    """
    Serializer for Abonnement Management.
    """
    user_id = serializers.IntegerField(required=True)



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
            'user',
            'commentaires',
            'likes')

        extra_kwargs = {
            'commentaires' : {
                'read_only' : True,
                
            },

            'likes' : {
                'read_only' : True,
                
            }
        }


class LikeSerializer(serializers.ModelSerializer):
    """docstring for DocuemntSerializer"""

    class Meta:

        model = models.Like
        fields = ('id', 
            'user', 
            'date',
            )

class CommentaireSerializer(serializers.ModelSerializer):
    """docstring for DocuemntSerializer"""

    class Meta:

        model = models.Commentaire
        fields = ('id', 
            'user', 
            'date',
            'texte'
            )


        
    
        