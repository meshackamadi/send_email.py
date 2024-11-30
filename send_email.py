
import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

#setting up my environment
from dotenv import load_dotenv 

#setting up the mail provider server
PORT = 587
EMAIL_SERVER = "smtp.gmail.com"

#loading the environment variables, get the path to the current directory
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")




#creating the text message
def send_email(subject, reciever_email, name, due_date, invoice_no, amount):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("DataThink", f"{sender_email}"))
    msg["BCC"] = sender_email
    
    #setting up the email body
    msg.set_content(
        f"""\
        Hi{name}
        I hope this mail finds you well, a quick note to remmind you that an amount of {amount} USD is due.
        in respect of {invoice_no} and {due_date}
        Best regards,
        DataThink
        """
    )
    # Add the html version. This converts the message into a multipart/alternative.
    #container, with the original text message as the first part and the new html
    # message as the second part.
    msg.add_alternative(
        f"""\
    <html>
      <body>
          <p>Hi {name}, </p>
          <p>I hope this mail finds you well. a quick note to remind you that an amount of <strong>{amount} USD</strong> is due.
          in respect of {invoice_no} and <strong>{due_date}</strong></p>
          <p>Best regards</p>
          <p>DataThink</p>
      </body>
    </html>
    """,
        subtype="html",           
    )
    
    #Interact with SMTP server
    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, reciever_email, msg.as_string())
        
        
    if __name__ == "__main__":
        send_email(
            subject="Testing work",
            name="Mesh",
            reciever_email="meshackamadi20@gmail.com",
            due_date="11, sep 2024",
            invoice_no="INV-10-23-990",
            amount="7",
            
        )
        
