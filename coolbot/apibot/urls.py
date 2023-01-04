from django.urls import path, include
from .views import BotUserApiView, FeedbackApiView

urlpatterns = [
    path('botuser/', BotUserApiView.as_view(),name="bot-user"),
    path('feed/',FeedbackApiView.as_view(), name="feedback-user")
]
