from twilio.rest import Client
from django.conf import settings

# Initialize Twilio client
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def make_call(to_number, message):
    """
    Make an outbound call with a text-to-speech message
    """
    try:
        call = client.calls.create(
            twiml=f'<Response><Say>{message}</Say></Response>',
            to=to_number,
            from_=settings.TWILIO_PHONE_NUMBER
        )
        return call.sid
    except Exception as e:
        print(f"Error making call: {e}")
        return None

def send_sms(to_number, message):
    """
    Send an SMS message
    """
    try:
        message = client.messages.create(
            body=message,
            to=to_number,
            from_=settings.TWILIO_PHONE_NUMBER
        )
        return message.sid
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None