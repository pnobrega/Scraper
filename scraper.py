import requests
from bs4 import BeautifulSoup
import smtplib
from time import sleep

URL = 'https://www.currys.ie/ieen/computing/laptops/laptops/asus-rog-strix-g731gu-17-3-gaming-laptop-intel-core-i7-gtx-1660-ti-512-gb-ssd-10194921-pdt.html'

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

    if(converted_price > 1500):
        send_mail()

    print(item_title)
    print(item_price_with_currency)
    print(converted_price)

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('ericspk6@gmail.com', 'htvvanefdbggwhka')

    subject = 'Price fell down!'
    body = 'Check the link https://www.currys.ie/ieen/computing/laptops/laptops/asus-rog-strix-g731gu-17-3-gaming-laptop-intel-core-i7-gtx-1660-ti-512-gb-ssd-10194921-pdt.html'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'ericspk6@gmail.com',
        'prteccom@gmail.com',
        msg
    )
    print('Email has been sent!')

    server.quit()

while(True):
    check_price()
    sleep(360)
