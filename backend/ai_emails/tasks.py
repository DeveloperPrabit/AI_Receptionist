from celery import shared_task
from django.conf import settings
from .models import EmailMessage
from users.models import UserProfile
from ai_utils.openai_integration import analyze_email_content, generate_email_reply


@shared_task
def process_incoming_email(user_id, email_data):
    """
    Process an incoming email using AI
    """
    try:
        # Analyze the email content
        category = analyze_email_content(email_data['subject'], email_data['body'])
        
        # Get user profile
        user_profile = UserProfile.objects.get(id=user_id)
        
        # Save the email to database
        email_obj = EmailMessage.objects.create(
            user=user_profile,
            subject=email_data['subject'],
            body=email_data['body'],
            sender=email_data['sender'],
            category=category
        )
        
        # Generate a reply if needed
        if category != 'spam':
            reply = generate_email_reply(email_data['subject'], email_data['body'], category)
            
            # In a real implementation, you would send the reply here
            # For now, we'll just store it
            email_obj.ai_reply = reply
            email_obj.save()
            
            return f"Processed email from {email_data['sender']} and generated reply"
        
        return f"Processed spam email from {email_data['sender']}"
        
    except Exception as e:
        return f"Error processing email: {e}"