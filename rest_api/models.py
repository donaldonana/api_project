from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from djongo import models
# from djangotoolbox.fields import EmbeddedModelField
from django.utils import timezone

# Create your models here.


class UserProfileManager(BaseUserManager):
    """manager for user profiles"""

    def create_user(self, email, nom, phone, password=None):
        """create the new user profile"""
        if not email:
            raise ValueError("User most have a email")

        # email = self.normalize_email(email)
        user = self.model(email=email, nom=nom , phone = phone)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, nom, phone, password):
        """create and save superuser with given detail"""
        user = self.create_user(email, nom, phone, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin, models.Model):


    TYPE = (

    ('lecteur', 'Lecteur'),
    ('auteur', 'Auteur'),
    ('visiteur', 'Visiteur'),
    ('admin', 'Admin'),

    ) 

    email = models.EmailField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255, blank = True)
    phone = models.CharField(max_length=255, unique=True)
    Pays = models.CharField(max_length=255, blank = True)
    avatar = models.ImageField(upload_to="images/%Y/%m/%d", blank=True, null=True)
    Type = models.CharField(max_length=25, choices=TYPE)
    # avatar = models.CharField(max_length = 255, blank = True)
    # avatar = models.FileField(upload_to="images/%Y/%m/%d", blank=True, null=True)
    # settings = JSONField(null=True, blank=True)
    abonnements  = models.ManyToManyField('self', 
        symmetrical = False , 
        related_name = "abonnement", 
        blank = True)

    # abonnes   = models.ForeignKey('self', related_name = "abonne", on_delete=models.CASCADE, null = True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["nom", "phone"]

    def get_last_name(self):

        return self.last_name


class Categorie(models.Model):
    """docstring for categorie"""
    CATEGORIE = (

    ('actualité', 'Actualité'),
    ('affaire', 'Affaire'),
    ('sport et loisir', 'Sport et Loisir'),

    )

    nom = models.CharField(max_length=25, choices=CATEGORIE, unique = True)

    def __str__(self):
        return self.nom

class Commentaire(models.Model):
    """docstring for Commentaires"""
    user = models.ForeignKey(UserProfile,
     on_delete=models.CASCADE,
     related_name = "comment_user"
     )

    date = models.DateTimeField(default = timezone.now)
    texte = models.TextField()

    def __str__(self):
        return "Commentaire de " + self.user.nom 
   
class Like(models.Model):
    """docstring for Likes"""
    user = models.ForeignKey(UserProfile, 
        on_delete=models.CASCADE,
        related_name = "like_user")
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.nom + " à liker " 


class Document(models.Model):
    """docstring for Document"""

    TYPE = (

    ('ArtMag', 'magazine/journal'),
    ('livre', 'Livre')

    )


    titre = models.CharField(max_length=255, default = "NAN")
    categorie = models.ForeignKey(Categorie, 
        on_delete = models.CASCADE,
        blank = True)
    descriptions = models.TextField(blank = True)
    date = models.DateTimeField(default = timezone.now)
    contenu = models.TextField(blank=True)
    tags = models.CharField(max_length=300, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    commentaires = models.ManyToManyField(Commentaire,
        
        related_name = "comment_doc",
        blank= True
     )
    likes = models.ManyToManyField(Like,
        
        related_name = "like_doc",
        blank= True
     )
    # -   Image de couverture
    # -   Abonnements
    # -   Parutions
    Type =  models.CharField(max_length=25, choices=TYPE)

    def __str__(self):
        return self.titre



class Lecture(models.Model):
    """docstring for Lecture"""
    date = models.DateTimeField(auto_now=True)
    document = models.ForeignKey(Document, 
        on_delete=models.CASCADE,
        related_name = "doclecture")
    user = models.ForeignKey(UserProfile,
     on_delete=models.CASCADE,
     related_name = "userlecture")
    def __str__(self):
        return self.document.titre





    

    

    # def __str__(self):
    #     return self.articlemagazine.titre



# class Repost(models.Model):
#     """docstring for Repost"""
#     articlemagazine = models.ForeignKey(Document, 
#         on_delete=models.CASCADE, 
#         related_name = "articlerepost")
#     user = models.ForeignKey(UserProfile, 
#         on_delete=models.CASCADE,
#         related_name = "userrepost")
#     date = models.DateTimeField(auto_now=True)
#     likes = models.ManyToManyField(
#         UserProfile,
#         through='LikeRepost',
#         related_name = "likesrepost"
#         )
#     commentaires = models.ManyToManyField(
#                     UserProfile,
#                     # through='Commentaires'
#                     related_name = "commentRepost")
#     def __str__(self):
#         return self.articlemagazine.titre





 
    

# class Reponse(models.Model):
#     """docstring for Reponses"""
#     user = models.ForeignKey(UserProfile, 
#         on_delete=models.CASCADE,
#         related_name = "userreponses")
#     commentaires = models.ForeignKey(Commentaire,
#      on_delete=models.CASCADE,
#      related_name = "commentreponses")
#     texte = models.CharField(max_length = 300)
#     date = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return self.commentaires.texte
    
        
    
        

    
