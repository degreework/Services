from django.db import models

from forum.models import Ask


class Module(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    photo = models.ImageField(upload_to='uploads/%Y/%m/%d',
                               blank=True,
                               null=True,
                               )
    

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"

    def __str__(self):
        return u"%s" % self.name


class Forum_wrap(models.Model):
    module = models.ForeignKey(Module)
    ask = models.ForeignKey(Ask)

    class Meta:
        verbose_name = "Forum_wrap"
        verbose_name_plural = "Forum_wraps"

    def __str__(self):
        return u"%s - %s" % (self.module.name, self.ask.title)
    

from activitie.models import ActivitieParent

class Activitie_wrap(models.Model):
    module = models.ForeignKey(Module)
    activitie = models.ForeignKey(ActivitieParent)

    class Meta:
        verbose_name = "Activitie_wrap"
        verbose_name_plural = "Activitie_wraps"

    def __str__(self):
        return u"%s - %s" % (self.module.name, self.activitie) 


from waliki.models import Page

class Wiki_wrap(models.Model):
    module = models.ForeignKey(Module)
    page = models.ForeignKey(Page)

    class Meta:
        verbose_name = "Wiki_wrap"
        verbose_name_plural = "wiki_wraps"

    def __str__(self):
        return u"%s - %s" % (self.module.name, self.page) 


from quiz.models import Quiz

class Quiz_wrap(models.Model):
    """docstring for Quiz_wrap"""
    module = models.ForeignKey(Module)
    quiz = models.ForeignKey(Quiz)

    class Meta:
        verbose_name = "Quiz_wrap"
        verbose_name_plural = "Quiz_wraps"

    def __str__(self):
        return u"%s -" % (self.module.name) 
