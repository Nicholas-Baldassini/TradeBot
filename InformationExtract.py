"""
This file is meant to extract the credentials needed to sign into trading view to scrape the data,
login to a gmail address to send notifications of buy/sell signals, send the notification to the
specified addresses, and locate the file location of the chromedriver needed for this program.
"""
Email_Sender = []
Email_Password = []
Email_Destination = []
Trading_View_User = []
Trading_View_Pass = []
Driver_Path = []

with open("InformationFile", "r") as f:
    for line in f:
        if line.strip() == "TRADING VIEW USERNAMES:":
            L = f.readline().strip()
            while L != "TRADING VIEW PASSWORDS:":
                # Record Trading View Usernames
                Trading_View_User.append(L[3:])
                L = f.readline().strip()
            L = f.readline().strip()
            while L != "EMAIL SENDER USERNAME:":
                # Record Trading View Passwords
                Trading_View_Pass.append(L[3:])
                L = f.readline().strip()
            L = f.readline().strip()
            while L != "EMAIL SENDER PASSWORD:":
                # Record Email Sender Username
                Email_Sender.append(L[3:])
                L = f.readline().strip()
            L = f.readline().strip()
            while L != "EMAIL RECEIVER:":
                # Record Email Sender Username
                Email_Password.append(L[3:])
                L = f.readline().strip()
            L = f.readline().strip()
            while L != "WEB DRIVER PATH:":
                # Record Email Sender Username
                Email_Destination.append(L[3:])
                L = f.readline().strip()
            L = f.readline().strip()
            while L != "":
                # Record Email Sender Username
                Driver_Path.append(L[3:])
                L = f.readline().strip()
Email_Password.pop(-1)
Email_Destination.pop(-1)
Email_Sender.pop(-1)
Trading_View_Pass.pop(-1)