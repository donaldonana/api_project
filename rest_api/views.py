from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters , generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions,
)



from rest_api import serializers
from rest_api import models, permissions

# Create your views here.
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser




class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating user profile"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('nom', 'email',)
    parser_classes = (MultiPartParser,FormParser)

    def get_user(self, id):
        try:
            return models.UserProfile.objects.get(id=id)
        except models.UserProfile.DoesNotExist:
            return HttpResponseBadRequest(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['patch'],
        url_path='remove_users_from_abonnements' ,
        detail=True,
        serializer_class=serializers.AbonnementManagementSerializer)
    def remove_users_from_abonnements(self,  request , pk=None):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            id_remove = serializer.data.get("user_id")


            user = self.get_user(int(id_remove))
            request.user.abonnements.remove(user)
            user.abonne.remove(request.user)

            request.user.save()
            user.save()
            response = {
                    "status": "success",
                    "code": status.HTTP_204_NO_CONTENT,
                    "message": "remove user successfully",
                    "data": [],
                }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['patch'],
        url_path='add_users_to_abonnements' ,
        detail=True,
        serializer_class=serializers.AbonnementManagementSerializer)
    def add_users_from_abonnements(self,  request , pk=None):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            id_add = serializer.data.get("user_id")


            user = self.get_user(int(id_add))
            print(user)
            request.user.abonnements.add(user)
            user.abonne.add(request.user)

            request.user.save()
            user.save()
            response = {
                    "status": "success",
                    "code": status.HTTP_204_NO_CONTENT,
                    "message": "user add successfully",
                    "data": [],
                }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApiView(ObtainAuthToken):

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "name" : user.name, "phone": user.phone})


class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = serializers.ChangePasswordSerializer
    model = models.UserProfile
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# ==========================================================================================


class DocumentViewSet(viewsets.ModelViewSet):
    """Handle creating and updating user profile"""
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('categorie__nom',)
    search_fields = ('descriptions', 'contenu','titre', 'tags')
    ordering_fields = ('titre', 'categorie','date', 'id')
    parser_classes = (MultiPartParser,FormParser)
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.UpdateOwnProfile,)
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name', 'email',)

class LikeViewSet(viewsets.ModelViewSet):
    """docstring for LikeViewSet"""
    serializer_class = serializers.LikeSerializer
    queryset = models.Like.objects.all()


class CommentaireViewSet(viewsets.ModelViewSet):
    """docstring for LikeViewSet"""
    serializer_class = serializers.CommentaireSerializer
    queryset = models.Commentaire.objects.all()
    authentication_classes = (TokenAuthentication,)
    
    


            


    
        