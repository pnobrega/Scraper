import requests
from bs4 import BeautifulSoup
import smtplib
from time import sleep
import datetime
import csv

#link for the product
URL = 'https://www.currys.ie/ieen/computing/laptops/laptops/acer-nitro-5-an515-15-6-gaming-laptop-intel-core-i5-gtx-1660-ti-1-tb-hdd-128-ssd-10194231-pdt.html'

#your user agent (google for "My User Agent")
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    item_title = soup.find(
        'h1',attrs={'class':'page-title'}
        ).get_text().strip(
        ).replace('\n', '')    

    try :
            item_price_with_currency = soup.find(
                'strong',attrs={'data-key':'current-price'}
                ).get_text().strip(
                )
    except:
            item_price_with_currency ='£0.0'


    converted_price = float(item_price_with_currency[1:6].replace(',',''))

    if(converted_price < 1500):
        send_mail()

    today = datetime.datetime.now()
    today_time = today.strftime("%d/%m/%Y %H:%M")
    print(today_time)
    print(item_title)
    print(converted_price)

    with open('prices.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([today_time, converted_price, item_title])

#Connection to GMAIL (2 steps security)
def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('yourEmail@gmail.com', 'AppPasswordFromGoogleAccount')

    subject = 'Price fell down!'
    body = 'Check the link https://www.currys.ie/ieen/computing/laptops/laptops/acer-nitro-5-an515-15-6-gaming-laptop-intel-core-i5-gtx-1660-ti-1-tb-hdd-128-ssd-10194231-pdt.html'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'YourEmail@gmail.com', #from
        'EmailToreceiveMGS@gmail.com', #to
        msg #Mensage
    )
    print('Email has been sent!')

    server.quit()

while(True):
    check_price()
    sleep(30) #Sleep time to search in x seconds
