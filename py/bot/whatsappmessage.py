import os
from dotenv import load_dotenv
from twilio.rest import Client 
load_dotenv()

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)
whatsapp_from = os.environ.get('TWILIO_FROM')
whatsapp_to = os.environ.get('TWILIO_TO')

message = client.messages.create(
  from_= whatsapp_from,
  body='Your appointment is coming up on July 21 at 3PM',
  to=whatsapp_to
)

print(message.sid)
