# -*- coding: utf-8 -*-
"""
emailpdf.py

focuses are on implementing functions that
1. produce pdf file with 6 graphs per page
2. send the pdf on local storage to online email

Notes:
    * password protection is temporary
    * Gmail is protected by some scheme, so we might have to create secondary gmail password
    or enable gmail account to approve less secure apps
    https://myaccount.google.com/lesssecureapps?utm_source=google-account&utm_medium=web
    * I will talk about this later on


Author : Hailey Lee
Version : 0.1

"""
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.backends.backend_pdf
from pandas.plotting import register_matplotlib_converters
from email.message import EmailMessage
import smtplib
import time


# TRIVIAL datetime converter for matplotlib
register_matplotlib_converters()

# Gather data and flatten (same as last time)
df = pd.read_csv(r'C:\Users\taemi\dev\PytrendsProj\kw_list.csv')

key_list = list(df.values.flatten())

# set counter for index i
i = 0

# matplotlib pdf library object / save name as result.pdf
pdf = matplotlib.backends.backend_pdf.PdfPages(r"C:\Users\taemi\dev\PytrendsProj\result.pdf")

# set a while loop for items in key_list until every item is explored
while i < len(key_list):
    # set figure size to 10inch x 10 inch
    fig1 = plt.figure(figsize=(10, 10))

    # set plot_num = ( col row index ) 3 col 2 row 1 index
    plot_num = 321
    for j in range(0,6):
        # loop escaper for last item
        if i == len(key_list):
            break

        print(i)

        # drawing is same as last time / note that we are calling from list key_list with index i
        pytrends = TrendReq(hl='en-EN', tz=360)
        try:

            pytrends.build_payload([key_list[i]], cat=0, timeframe='today 5-y', geo='', gprop='')
            data = pytrends.interest_over_time()
            data['12MA'] = data[key_list[i]].rolling(window=52, min_periods=0).mean()

            #TODO here we have to define a filter function to select an index i

            #filter( data ) which return true or false
            # if true then, plot as usual , else : skip plot and decrement index of plot_num


            # Here we create a subplot that is included in the figure with the position of plot_num
            plt.subplot(plot_num)
            plt.plot(data.index, data[key_list[i]], data['12MA'])
            plt.ylabel('Volume')
            plt.title(key_list[i])

            # increment total index number and
            # increment plot_num -> to draw on next position
            plot_num = plot_num + 1
            i = i + 1
        except:
            i = i + 1

    #save the figure
    pdf.savefig(fig1)
#save pdf by closing
pdf.close()

print("hello")

exit()

# we will have to move input password part to top because this runs after the data processing
# Enable input of password on commandline
#passwd = input("Password: ")
passwd="lstksszvnatnuebd"


# Try catch exception
# Tries first, if error go to except
try:
    # smtp = simple mail transfer protocol

    smtp_gmail= smtplib.SMTP('smtp.gmail.com', 587)
    smtp_gmail.ehlo()

    # Start secure connection
    smtp_gmail.starttls()

    # input login ID and Password
    smtp_gmail.login('hottaem410@gmail.com', passwd)

    # make Emailmessage object
    msg = EmailMessage()

    msg['Subject'] = "This is the title"
    msg.set_content("the content of the mail can be string")
    msg['From'] = 'hottaem410@gmail.com'
    msg['To'] = 'taemin410@gmail.com, hottaem410@gmail.com'

    #attach file named result.pdf
    file = './result.pdf'
    fp = open(file, 'rb')
    file_data = fp.read()
    msg.add_attachment(file_data, maintype='application/pdf', subtype='pdf', filename='result.pdf')

    #send out email
    smtp_gmail.send_message(msg)

    print( "sent email! ")

except:
    print ('Something went wrong...')

# You can ignore this part  / another way of sending email
"""
smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp.login('hottaem410@gmail.com', passwd)
msg = MIMEText("meesgae")
msg['Subject'] = 'TEST'
smtp.sendmail('hottaem410@gmail.com', 'taemin410@gmail.com', msg.as_string())
smtp.quit()
"""
