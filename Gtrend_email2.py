# -*- coding: utf-8 -*-
"""

"""
from typing import List, Any

import matplotlib.backends.backend_pdf
from email.message import EmailMessage
import smtplib
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pandas as pd
import os
from pandas.plotting import register_matplotlib_converters

# TRIVIAL datetime converter for matplotlib
register_matplotlib_converters()

if not os.path.exists('Trend_data'):
    os.makedirs('Trend_data')
if not os.path.exists('Trend_data\image'):
    os.makedirs('Trend_data\image')

if not os.path.exists('Trend_data\image2'):
    os.makedirs('Trend_data\image2')

drtr1="Trend_data/"
drtr2="Trend_data/image/"
drtr3="Trend_data/image2/"

# Gather data and flatten (same as last time)
df = pd.read_csv('kw_list2.csv')

key_list: List[Any] = list(df.values.flatten())

# set counter for index i
i = 0

# matplotlib pdf library object / save name as result.pdf
pdf = matplotlib.backends.backend_pdf.PdfPages("result.pdf")

# set a while loop for items in key_list until every item is explored
while i < len(key_list):
    # set figure size to 10inch x 10 inch
    fig1 = plt.figure(figsize=(12, 10 ))

    # set plot_num = ( col row index ) 3 col 2 row 1 index
    plot_num = 321

    for j in range(0,6):
        # loop escaper for last item
        if i == len(key_list):
            break

        print(i)

        try:
            # drawing is same as last time / note that we are calling from list key_list with index i
            pytrends = TrendReq(hl='en-EN', tz=360)
            pytrends.build_payload([key_list[i]], cat=0, timeframe='today 5-y', geo='', gprop='')
            data = pytrends.interest_over_time()
            data['12MA'] = data[key_list[i]].rolling(window=52, min_periods=0).mean()
            data['3MA'] = data[key_list[i]].rolling(window=13, min_periods=0).mean()
            data['YoY'] = data['12MA'] - data['12MA'].shift(1)
            data['3MYoY'] = (data['3MA'] - data['3MA'].shift(52)) / data['3MA'].shift(52)

            jrow= (j // 2)*2
            jcol = j % 2
            # Here we create a subplot that is included in the figure with the position of plot_num
            ax1 = plt.subplot2grid((6, 2), (jrow, jcol), rowspan=1, colspan=1)
            plt.title(key_list[i])
            ax2 = plt.subplot2grid((6, 2), (jrow+1, jcol), rowspan=1, colspan=1, sharex=ax1)
            ax2.xaxis_date()

            # Draw charts
            ax1.plot(data.index, data[key_list[i]])
            ax1.plot(data.index, data['3MA'])
            ax1.plot(data.index, data['12MA'])
            ax1.grid(True, linestyle='-.', linewidth=0.5)
            ax1.set_xticklabels([])

            ax2.plot(data.index, data['YoY'], color='white', alpha=0)
            ax2.fill_between(data.index, 0, data['YoY'], where=(data['YoY'] > 0), color='red', alpha=0.3)
            ax2.fill_between(data.index, 0, data['YoY'], where=(data['YoY'] < 0), color='blue', alpha=0.3)
            ax2.grid(True, axis='x', linestyle='-.', linewidth=0.5)

            ax3 = ax2.twinx()
            ax3.plot(data.index, data['3MYoY'])

            plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
            plt.tight_layout()

            # increment total index number and
            # increment plot_num -> to draw on next position
            plot_num = plot_num + 1
            print(key_list[i], " - successfully retrieved")
            i = i + 1

        except:
            print(key_list[i], " - No data returned")
            i = i + 1
    # save the figure
    pdf.savefig(fig1)

#save pdf by closing
pdf.close()

#
# # we will have to move input password part to top because this runs after the data processing
# # Enable input of password on commandline
# passwd = input("Password: ")
#
#
# # Try catch exception
# # Tries first, if error go to except
# try:
#     # smtp = simple mail transfer protocol
#
#     smtp_gmail= smtplib.SMTP('smtp.gmail.com', 587)
#     smtp_gmail.ehlo()
#
#     # Start secure connection
#     smtp_gmail.starttls()
#
#     # input login ID and Password
#     smtp_gmail.login('dennis.hc.yoo@gmail.com', passwd)
#
#     # make Emailmessage object
#     msg = EmailMessage()
#
#     msg['Subject'] = "This is the title"
#     msg.set_content("email auto_sending test / the content of the mail can be string")
#     msg['From'] = 'dennis.hc.yoo@gmail.com'
#     msg['To'] = 'lead21c@gmail.com', 'back0413@gmail.com'
#
#     #attach file named result.pdf
#     file = './result.pdf'
#     fp = open(file, 'rb')
#     file_data = fp.read()
#     msg.add_attachment(file_data, maintype='application/pdf', subtype='pdf', filename='result.pdf')
#
#     #send out email
#     smtp_gmail.send_message(msg)
#
#     print( "sent email! ")
#
# except:
#     print ('Something went wrong...')



# You can ignore this part  / another way of sending email
#"""
#    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#    smtp.login('hottaem410@gmail.com', passwd)
#    msg = MIMEText("meesgae")
#    msg['Subject'] = 'TEST'
#    smtp.sendmail('hottaem410@gmail.com', 'taemin410@gmail.com', msg.as_string())
#    smtp.quit()
#    """
