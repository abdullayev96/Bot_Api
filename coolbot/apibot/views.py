from .models import BotUser, Feedback
from .serializers import BotUserSerializer, FeedbackSerializer
from rest_framework.generics import  ListCreateAPIView



class BotUserApiView(ListCreateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer

class FeedbackApiView(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer