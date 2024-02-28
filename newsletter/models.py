from django.db import models

class Newsletter(models.model):
    email = models.EmailField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.mail
