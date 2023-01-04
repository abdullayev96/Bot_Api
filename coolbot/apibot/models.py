from django.db import models

class BotUser(models.Model):
    user_id =models.CharField(max_length=100)
    name= models.CharField(max_length=100)
    username = models.CharField(max_length=200, null=True, blank=True)
    create_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Feedback(models.Model):
    user_id = models.CharField(max_length=200, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.body)

