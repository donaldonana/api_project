from django.contrib import admin
from rest_api import models


admin.site.register(models.UserProfile)
admin.site.register(models.Document)
admin.site.register(models.Categorie)
admin.site.register(models.Commentaire)
# admin.site.register(models.CommentaireRepost)
# admin.site.register(models.LikeArticlesMag)
admin.site.register(models.Like)
# admin.site.register(models.LikeCommentaireRepost)
# admin.site.register(models.LikeRepost)
# admin.site.register(models.Repost)
admin.site.register(models.Lecture)
# admin.site.register(models.Reponse)
