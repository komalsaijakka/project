from django.contrib import admin
from django.urls import path
from core.views import (
    home,
    how_it_works,
    your_journey,
    what_makes_us_different,
    about,
    psycho_education,
    signin,
    chatbot_reply,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("how-it-works/", how_it_works, name="how_it_works"),
    path("your-journey/", your_journey, name="your_journey"),
    path("what-makes-us-different/", what_makes_us_different, name="what_makes_us_different"),
    path("about/", about, name="about"),
    path("psycho-education/", psycho_education, name="psycho_education"),
    path("signin/", signin, name="signin"),
    path("chatbot-reply/", chatbot_reply, name="chatbot_reply"),
]
