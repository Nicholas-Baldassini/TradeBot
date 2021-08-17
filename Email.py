import smtplib, ssl

port = 465  # For SSL
password = "AgainWithTheMaestro123"
email = "bottrader00002@gmail.com"
smtp_server = "smtp.gmail.com"

boom = "6479962879@fido.ca"
john = "6473823566@msg.telus.com"
Anthony = "6474662879@fido.ca"
Selena = "6478844347@msg.telus.com"

# Create a secure SSL context
context = ssl.create_default_context()

message = """
\t
8-----
"""


def send_email(target: str, text: str):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, target, text)


if __name__ == "__main__":
    send_email(Selena, message)
