import openai
from django.conf import settings

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY

def analyze_email_content(subject, body):
    """
    Analyze email content and categorize it
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI receptionist. Analyze this email and categorize it as 'general', 'urgent', 'spam', or 'appointment'."},
                {"role": "user", "content": f"Subject: {subject}\n\nBody: {body}"}
            ]
        )
        category = response.choices[0].message.content.strip().lower()
        return category
    except Exception as e:
        print(f"Error analyzing email: {e}")
        return "general"

def generate_email_reply(subject, body, category):
    """
    Generate an automated reply for the email
    """
    try:
        system_message = {
            "general": "You are an AI receptionist. Write a friendly and professional response to this general inquiry email.",
            "urgent": "You are an AI receptionist. Write a prompt and professional response to this urgent email.",
            "appointment": "You are an AI receptionist. Write a clear and helpful response regarding appointment scheduling.",
            "spam": "You are an AI receptionist. Write a generic response to what appears to be spam."
        }.get(category, "You are an AI receptionist. Write a professional response to this email.")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Subject: {subject}\n\nBody: {body}"}
            ]
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        print(f"Error generating email reply: {e}")
        return "Thank you for your email. We will get back to you soon."

def analyze_call_transcript(transcript):
    """
    Analyze call transcript to determine caller intent
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI receptionist. Analyze the call transcript and determine the caller's intent."},
                {"role": "user", "content": transcript}
            ]
        )
        analysis = response.choices[0].message.content
        return analysis
    except Exception as e:
        print(f"Error analyzing call transcript: {e}")
        return "Unable to analyze call at this time."