import ssl, smtplib
from email.message import EmailMessage
from app.common.variables import variables

class BookingService():
    def send_confirmation(self, to_email, name, date, time):
        msg = EmailMessage()
        msg["Subject"]="Interview Confirmation"
        msg["From"]=variables.SMTP_USER; msg["To"]=to_email
        msg.set_content(f"Hi {name},\nYour interview is booked for {date} at {time}.")
        ctx=ssl.create_default_context()
        with smtplib.SMTP_SSL(variables.SMTP_HOST, variables.SMTP_PORT,context=ctx) as server:
            server.login(variables.SMTP_USER, variables.SMTP_PASS); server.send_message(msg)
