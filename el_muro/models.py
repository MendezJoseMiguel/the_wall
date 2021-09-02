from __future__ import unicode_literals
from django.db import models

class UsersManager(models.Manager):

    def basic_validator(self,postData):
        errors={}

        if len(postData['first_name']) < 4:
            errors['first_name'] = "El nombre de usuario debe tener al menos 3 letras"

        if len(postData['last_name']) < 4:
            errors['last_name'] = "El nombre de usuario debe tener al menos 3 letras"

        if len(postData['email']) < 4:
            errors['email'] = "El email de usuario debe tener al menos 4 letras"

        if len(postData['password']) < 6:
            errors['password'] = "La contraseña de usuario debe tener al menos 6 caracteres"

        if postData['password'] != postData['password_confirm']:
            errors['password'] = "Ambas contraseñas deben ser iguales"


        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    allowed = models.BooleanField(default=True)
    avatar = models.URLField(
        default = "https://png.pngtree.com/png-vector/20191026/ourlarge/pngtree-avatar-vector-icon-white-background-png-image_1870181.jpg"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

    def __repr__(self) -> str:
        return f'{self.id}:{self.first_name}: {self.last_name}: {self.email}'

class Post(models.Model):
    post = models.TextField(null=True, blank=True)
    user = models.ForeignKey(Users, related_name = "posts", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __repr__(self) -> str:
        return f'{self.message}: {self.user_id}'

class Comments(models.Model):
    comments = models.TextField(max_length=255)
    user = models.ForeignKey(Users,related_name="comments",on_delete= models.CASCADE)
    post = models.ForeignKey(Post,related_name="comments",on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f'{self.comments}: {self.user_id}: {self.message_id}'