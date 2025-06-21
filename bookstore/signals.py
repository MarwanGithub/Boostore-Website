from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Book, BookImage

@receiver(pre_save, sender=Book)
def delete_old_book_cover_on_update(sender, instance, **kwargs):
    """
    Deletes the old cover image file from Cloudinary when a Book's cover_image is updated.
    """
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.cover_image and instance.cover_image != old_instance.cover_image:
            old_instance.cover_image.delete(save=False)
    except sender.DoesNotExist:
        # This happens when creating a new object.
        pass

@receiver(post_delete, sender=Book)
def delete_book_cover_on_delete(sender, instance, **kwargs):
    """
    Deletes the cover image file from Cloudinary when a Book is deleted.
    """
    if instance.cover_image:
        instance.cover_image.delete(save=False)

@receiver(pre_save, sender=BookImage)
def delete_old_book_image_on_update(sender, instance, **kwargs):
    """
    Deletes the old image file from Cloudinary when a BookImage's image is updated.
    """
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.image and instance.image != old_instance.image:
            old_instance.image.delete(save=False)
    except sender.DoesNotExist:
        pass

@receiver(post_delete, sender=BookImage)
def delete_book_image_on_delete(sender, instance, **kwargs):
    """
    Deletes the image file from Cloudinary when a BookImage is deleted.
    """
    if instance.image:
        instance.image.delete(save=False) 