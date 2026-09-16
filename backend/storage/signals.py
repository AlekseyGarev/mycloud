import logging

from django.db.models.signals import post_delete
from django.dispatch import receiver
from storage.models import File

logger = logging.getLogger("storage")


@receiver(post_delete, sender=File)
def delete_file_from_storage(sender, instance, **kwargs):
    if not instance.file:
        return
    try:
        instance.file.delete(save=False)
    except Exception:
        logger.exception("Не удалось удалить физический файл %s", instance.file.name)
