from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
import os
from openai import OpenAI

# Create OpenAI client using environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))


def home(request: HttpRequest):
  return render(request, "core/home.html")


def how_it_works(request: HttpRequest):
  return render(request, "core/how_it_works.html")

def what_makes_us_different(request: HttpRequest):
    return render(request, "core/what_makes_us_different.html")


def chatbot_reply(request: HttpRequest):
  if request.method != "POST":
    return JsonResponse({"error": "POST required"}, status=405)

  user_message = request.POST.get("message", "")[:500]
  if not user_message:
    return JsonResponse({"reply": "Please type something so I can help."})

  try:
    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {
          "role": "system",
          "content": (
            "You are a gentle website guide for MindSettler, a psycho‑education "
            "and therapy platform in India. Explain services, sessions, and "
            "booking in a calm, human tone. Never give crisis, diagnostic, or "
            "medication advice. If the user asks about 'how it works', "
            "'process', or 'steps', briefly explain and then clearly invite "
            "them to open the How It Works page at /how-it-works/."
          ),
        },
        {"role": "user", "content": user_message},
      ],
    )
    text = completion.choices[0].message.content.strip()
  except Exception:
    text = "Sorry, something went wrong while talking to the assistant."

  return JsonResponse({"reply": text})
