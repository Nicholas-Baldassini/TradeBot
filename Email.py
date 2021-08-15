import smtplib, ssl

port = 465  # For SSL
port = 587
password = "BoomJohn_123"
email = "DelTheFunkiestHomoSapien@gmail.com"
smtp_server = "smtp.gmail.com"

boom = "6479962879@fido.ca"
john = "6473823566@msg.telus.com"
Anthony = "6474662879@fido.ca"

# Create a secure SSL context
context = ssl.create_default_context()

message = """
EARTH TO JOHNY

This could be our crypto notification system, automatic message system,
I used an email service for this.
"""


def send_email(target: str, text: str):
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, target, text)
        # TODO: Send email here


def send_ssl_email(target: str, text: str):
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(email, password)
        server.sendmail(email, target, text)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

send_ssl_email(boom, message)
