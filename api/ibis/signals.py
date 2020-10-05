import ibis.models as models

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=models.Donation)
def updatePersonScore(sender, instance, created, **kwargs):
    if not created:
        return

    # user score is defined as the unix time of their latest donation
    user = instance.user
    user.score = instance.created.timestamp()
    user.save()
