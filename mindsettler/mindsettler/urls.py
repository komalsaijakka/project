from django.contrib import admin
from django.urls import path
from core.views import (
    home,
    how_it_works,
    what_makes_us_different,
    your_journey,
    chatbot_reply,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("how-it-works/", how_it_works, name="how_it_works"),
    path("what-makes-us-different/", what_makes_us_different, name="what_makes_us_different"),
    path("your-journey/", your_journey, name="your_journey"),
    path("chatbot-reply/", chatbot_reply, name="chatbot_reply"),
]
