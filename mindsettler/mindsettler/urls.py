from django.contrib import admin
from django.urls import path, include
from core.views import (
    home,
    how_it_works,
    your_journey,
    what_makes_us_different,
    about,
    psycho_education,
    resources,
    contact,
    booking_view,
    history_view,
    privacy_policy,
    refund_policy,
    confidentiality_policy,
    chatbot_reply,
    signin,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", home, name="home"),
    path("signin/", signin, name="signin"),
    path("how-it-works/", how_it_works, name="how_it_works"),
    path("your-journey/", your_journey, name="your_journey"),
    path("what-makes-us-different/", what_makes_us_different, name="what_makes_us_different"),
    path("about/", about, name="about"),
    path("psycho-education/", psycho_education, name="psycho_education"),
    path("resources/", resources, name="resources"),
    path("contact/", contact, name="contact"),
    path("booking/", booking_view, name="booking"),
    path("history/", history_view, name="history"),
    path("legal/privacy/", privacy_policy, name="privacy_policy"),
    path("legal/refund/", refund_policy, name="refund_policy"),
    path("legal/confidentiality/", confidentiality_policy, name="confidentiality_policy"),
    path("chatbot-reply/", chatbot_reply, name="chatbot_reply"),
]
