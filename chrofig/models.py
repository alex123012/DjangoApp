from django.db import models


class TextFileModel(models.Model):

    title = models.CharField('Title for Graph', max_length=50,)
    min_time = models.IntegerField('Min time for graph',)
    max_time = models.IntegerField('Max time for graph',)
    file_field = models.FileField('Upload file(s)')

    def __str__(self):
        return self.title
