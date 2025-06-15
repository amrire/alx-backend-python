from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id is None:
        return  # Skip new messages

    try:
        original = Message.objects.get(id=instance.id)
        if original.content != instance.content:
            MessageHistory.objects.create(
                message=original,
                old_content=original.content
            )
            instance.edited = True  # Mark message as edited
    except Message.DoesNotExist:
        pass
    
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete any notifications linked to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories related to messages from/to this user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
