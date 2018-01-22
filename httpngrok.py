
''' The ngrok product has to be started before the script runs. We recommend doing it at startup
We just did by adding a new line into the crontab system. '''


import os                                                # Library for OS commands
import json                                              # Library for JSON format
import requests                                          # Library for requests commands. It will be used in our API product
import socket                                            # Library for testing the connection to the Internet
import time                                              # Library for time functions like sleeps and son on
import smtplib                                           # Library to work with emails
from email.MIMEMultipart import MIMEMultipart            # Library to send emails with a subject line, sender and reciever
from email.MIMEText import MIMEText                      # Library to send emails in a plain text
from email.MIMEBase import MIMEBase
from email import encoders


"""
This functions checks connection to Google DNS server
If DNS server is reachable on port 53, then it means that
the internet is up and running
"""
def internet_connected(host="8.8.8.8", port=53):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(10)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        pass
    return False
    

'''                                   Variables Initialization                   '''

test_ngrok = 0     # This variable checks when monitoring ngrok in order to get its actual public IP through API
count = 0
connected = False  # It has not been checked the internet connection yet.
emailmsg = ""
msg = ""

while (True):
    if (internet_connected):
        # If previously internet was disconnected, then print message
        if not connected:
            print "Internet is up!"
            connected = True
            while test_ngrok == 0:
                ''' URL for ngrok base API. 
                    As the header says, ngrok has to be started before running for this script to work. '''

                url = 'http://localhost:4040/api/tunnels'

                ''' This lines will get the JSON respond from the API. '''

                r = requests.get(url)
                r = r.json()

                ''' We need to get the actual public url.
                Since r is a dict data type, we can iterate it with a for loop and save it in the msg variable. '''

                for i in r['tunnels']:
                    msg = msg + i['public_url'] +'\n'       # This will concatenate with the first value of msg in order to show the final message.
                print msg                                   # Final value of msg. This will be sent to the pre-configured mail

                ''' Converting the unicode format of msg to a plain string. 
                    The block which will send the email has to send a plain string variable not an unicode one.'''

                msg = str(msg)
                emailmsg = msg     # Saving the msg value into emailmsg
                if not emailmsg == "" : 
                    test_ngrok = 1     # Ngrok is tested now.

                    ''' Block to send the email with the actual ngrok public IP '''

                    fromaddr = "a@gmail.com"                                   # Sender email                        
                    toaddr = "b@gmail.com"                                     # Reciever email 
                    msg = MIMEMultipart()                                      # Subject Line, From and To specs
                    msg['From'] = fromaddr
                    msg['To'] = toaddr
                    msg['Subject'] = "Location - Your actual IP Address is"       
                    msg.attach(MIMEText(emailmsg, 'plain'))                 # Type of message .This one is a plane and pure text.
                    server = smtplib.SMTP('smtp.gmail.com', 587)            # SMTP Email settings. In this case is GMAIL.
                    server.starttls()                                       # Security setting for the email account
                    server.login(fromaddr, "Passwd")                        # Password of the sender email
                    text = msg.as_string()                                  # Setting the msg variable as a string
                    server.sendmail(fromaddr, toaddr, text)                 # Sending email 
                    server.quit()

        # Wait for 10 seconds before checking for internet connectivity
        time.sleep(10)
    else:
        # If previously internet connected, then print message
        if connected:
            print "Internet is down..."
            connected = False
            emailmsg = ""  
            test_ngrok = 0
        msg = ""
        print "Exiting... Bye!"