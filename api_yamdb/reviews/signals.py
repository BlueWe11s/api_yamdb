from django.db.models import Avg
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Review


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_average_rating(sender, instance, **kwargs):
    '''
    Обновляет средний рейтинг произведения при добавлении/удалении отзыва.
    '''
    title = instance.title
    reviews = title.reviews.all()
    if reviews.exists():
        title.average_rating = reviews.aggregate(Avg('score'))['score__avg']
    else:
        title.average_rating = 0
    title.save()
