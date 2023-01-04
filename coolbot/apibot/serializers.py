from rest_framework.serializers import ModelSerializer
from .models import BotUser, Feedback

class BotUserSerializer(ModelSerializer):
    class Meta:
        model = BotUser
        fields = ('user_id', "name", "username", "create_at")


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = ( "user_id", "create_at", "body")