from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.decorators import action

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Create a new conversation with a list of participant user IDs"""
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response({"error": "participants field is required."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        participants = CustomUser.objects.filter(id__in=participant_ids)
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Send a new message to an existing conversation"""
        conversation_id = request.data.get("conversation")
        content = request.data.get("content")

        if not conversation_id or not content:
            return Response(
                {"error": "Both conversation and content are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
