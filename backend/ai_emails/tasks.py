from celery import shared_task
import openai
import imaplib
import email
from email.header import decode_header
import smtplib
from django.conf import settings

@shared_task
def fetch_emails(user_id, email_account, password):
    # This task would fetch emails from the user's account
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_account, password)
        mail.select("inbox")
        
        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        
        email_ids = messages[0].split()
        
        emails_data = []
        
        for e_id in email_ids:
            # Fetch the email
            status, msg_data = mail.fetch(e_id, '(RFC822)')
            
            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    # Decode email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    # Decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding if encoding else "utf-8")
                    
                    # Get email body
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    emails_data.append({
                        'subject': subject,
                        'sender': From,
                        'body': body
                    })
        
        mail.close()
        mail.logout()
        
        # Process each email with AI
        for email_data in emails_data:
            ai_reply.delay(user_id, email_data)
        
        return f"Fetched {len(emails_data)} emails"
        
    except Exception as e:
        return f"Error fetching emails: {e}"

@shared_task
def ai_reply(user_id, email_data):
    try:
        # Analyze the email content
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI receptionist. Analyze this email and generate an appropriate response."},
                {"role": "user", "content": f"Email subject: {email_data['subject']}\n\nEmail body: {email_data['body']}"}
            ]
        )
        
        analysis = response.choices[0].message.content
        
        # Categorize the email
        category_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Categorize this email as 'general', 'urgent', 'spam', or 'appointment'."},
                {"role": "user", "content": f"Email subject: {email_data['subject']}\n\nEmail body: {email_data['body']}"}
            ]
        )
        
        category = category_response.choices[0].message.content.lower()
        
        # Save the email to the database
        from .models import EmailMessage
        from users.models import UserProfile
        
        user_profile = UserProfile.objects.get(id=user_id)
        
        email_obj = EmailMessage.objects.create(
            user=user_profile,
            subject=email_data['subject'],
            body=email_data['body'],
            sender=email_data['sender'],
            category=category
        )
        
        # Generate a reply if needed
        if category != 'spam':
            reply_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI receptionist. Write a professional response to this email."},
                    {"role": "user", "content": f"Email subject: {email_data['subject']}\n\nEmail body: {email_data['body']}"}
                ]
            )
            
            reply = reply_response.choices[0].message.content
            
            # Send the reply (in a real implementation)
            # send_email.delay(email_data['sender'], f"Re: {email_data['subject']}", reply)
            
            return f"Processed email from {email_data['sender']} and generated reply"
        
        return f"Processed spam email from {email_data['sender']}"
        
    except Exception as e:
        return f"Error processing email: {e}"