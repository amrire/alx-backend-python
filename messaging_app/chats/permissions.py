from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipant(BasePermission):
    """
    Allow access only to conversation participants.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsMessageSenderOrParticipant(BasePermission):
    """
    Allow message access to the sender or participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.sender == request.user or 
            request.user in obj.conversation.participants.all()
        )
