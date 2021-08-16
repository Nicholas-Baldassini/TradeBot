import smtplib, ssl

port = 465  # For SSL
# port = 587
password = "BoomJohn_123"
email = "DelTheFunkiestHomoSapien@gmail.com"
smtp_server = "smtp.gmail.com"

boom = "6479962879@fido.ca"
john = "6473823566@msg.telus.com"
Anthony = "6474662879@fido.ca"

# Create a secure SSL context
context = ssl.create_default_context()

message = """

We are going to be fucking millionaires
8====)

I have the program pretty much set up but I need to install it
on my desktop so we can run it 24/7, maybe tonight.

8===============================)
"""


def send_email(target: str, text: str):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, target, text)
        # TODO: Send email here



send_email(john, message)
