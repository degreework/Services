from django.db import models
from model_utils.managers import InheritanceManager


class Material(models.Model):
    
    title = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    objects = InheritanceManager()
    
    def __str__(self):
        return self.title

class MaterialFile(Material):
    file = models.FileField()

    class Meta:
        verbose_name = "MaterialFile"
        verbose_name_plural = "MaterialFiles"
        permissions = (("can_view", "Can view MaterialFile"),)


class MaterialLink(Material):
    url = models.URLField()

    class Meta:
        verbose_name = "MaterialLink"
        verbose_name_plural = "MaterialLinks"
        permissions = (("can_view", "Can view MaterialLink"),)
