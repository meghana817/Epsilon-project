import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class SMSSender:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            print("Warning: Twilio credentials not configured. SMS functionality disabled.")
    
    def send_sms(self, to_number, message):
        """Send SMS message to specified number"""
        if not self.client:
            print(f"SMS would be sent to {to_number}: {message}")
            return False
        
        try:
            # Ensure phone number is in proper format
            if not to_number.startswith('+'):
                to_number = '+1' + to_number.replace('-', '').replace(' ', '')
            
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            print(f"SMS sent successfully to {to_number}. SID: {message_obj.sid}")
            return True
            
        except Exception as e:
            print(f"Error sending SMS to {to_number}: {e}")
            return False
    
    def send_bulk_sms(self, recipients, message):
        """Send SMS to multiple recipients"""
        results = []
        for recipient in recipients:
            success = self.send_sms(recipient, message)
            results.append({
                'recipient': recipient,
                'success': success
            })
        return results
    
    def validate_phone_number(self, phone_number):
        """Validate phone number format"""
        if not phone_number:
            return False
        
        # Remove common separators
        clean_number = phone_number.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        
        # Check if it's a valid US number
        if clean_number.startswith('+1'):
            clean_number = clean_number[2:]
        elif clean_number.startswith('1'):
            clean_number = clean_number[1:]
        
        return len(clean_number) == 10 and clean_number.isdigit() 