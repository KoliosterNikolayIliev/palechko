from django.contrib.auth.models import User
from django.db import models

from accounts.models import UserProfile


class Item(models.Model):
    ITEM_TYPES = (
        ('pic', 'Drawing'),
        ('mod', 'Hand-made model'),

    )

    CATEGORY_TYPES = (
        ('Other', 'Other'),
        ('Nature', 'Nature'),
        ('Family', 'Family'),
        ('Animals', 'Animals'),
        ('Christmas', 'Christmas'),
        ('Easter', 'Easter'),
        ('City', 'City'),
        ('Fun', 'Fun'),

    )

    type = models.CharField(max_length=7, choices=ITEM_TYPES, default=None)
    category = models.CharField(max_length=20, choices=CATEGORY_TYPES, default='Other')
    name = models.CharField(max_length=30, blank=False)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='items')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.id}; {self.name}; {self.date_created};'


class Like(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(max_length=2)


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
