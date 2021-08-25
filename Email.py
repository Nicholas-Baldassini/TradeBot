import smtplib, ssl
import InformationExtract as IE
port = 465  # For SSL

password = IE.Email_Password[0]
email = IE.Email_Sender[0]
boom = IE.Email_Destination[0]
john = IE.Email_Destination[1]
jp = IE.Email_Destination[2]

smtp_server = "smtp.gmail.com"

# Create a secure SSL context
context = ssl.create_default_context()
message = "\tThis is a test! Snap me if you received this message, the bot is pretty much ready -boom"


def send_email(targets: list, text: str):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        for target in targets:
            server.sendmail(email, target, text)


if __name__ == "__main__":
    send_email([boom], message)
