from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extend the default user model if needed later (e.g., avatar, status)."""
    pass

    def __str__(self):
        return self.username
   
    
class Conversation(models.Model):
    """Model representing a conversation between multiple users."""
    participants = models.ManyToManyField('CustomUser', related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} - Participants: {', '.join(user.username for user in self.participants.all())}"


class Message(models.Model):
    """Model representing a message sent within a conversation."""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='messages_sent')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} in Conversation {self.conversation.id}"
