from django.db import models


class Book(models.Model):

    name = models.CharField('Название', max_length=100)
    author_name = models.CharField('Имя автора', max_length=100)
    is_published = models.BooleanField('Опубликовано', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.name
