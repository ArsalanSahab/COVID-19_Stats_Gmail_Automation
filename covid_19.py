######### IMPORTS #############
import smtplib
import time
import schedule
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tabulate import tabulate



# INITIALISING COUNTRY AND CHROMEDRIVER
Country = 'Country Name'
driver = webdriver.Chrome('/Path/To/ChromeDriver')

def get_data(Country):
    
    
    driver.get('https://www.worldometers.info/coronavirus/')
    
    # Gettting Table Data
    table = driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
    xpath = "//td[contains(text(), '%s')]"% Country
    
    # Check if country in Table
    try:

        searched_country = table.find_element_by_xpath(xpath)
        row = searched_country.find_element_by_xpath("./..")

    except:

        searched_country = table.find_element_by_link_text(Country)
        row = searched_country.find_element_by_xpath("../..")

    col_data = row.find_elements_by_tag_name("td")
    data_val = [x.text for x in col_data]

    # Convert Data into a Table
    data_keys = ['Country', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths','Total Recovered','Active Cases','Critical','Total Cases per million']
    data_dict = dict(zip(data_keys,data_val))
    
    return data_dict

def send_mail(data_dict):
    
    # Gmail Setup
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('email adrress', 'password')

    # Recipients to send mail to
    recipients = ['list','of','recipients']


    for recipient in recipients :
    
            # Subject
            subject = 'COVID-19 stats in your Country'
            
            # Body
            text = """ COVID-19 Latest Statistics in your Country (Note : This is an Automated Email)
            
            {table}
            Regards,
            YourName"""
            
            html = """
            <html>
            <head>
            <style> 
            table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
            th, td {{ padding: 5px; }}
            </style>
            </head>
            <body><p> COVID-19 Latest Statistics in your Country (Note : This is an automated email)
            
            </p>
            {table}
            <p>Regards,</p>
            <p>Yourname</p>
            </body></html>
            """
            
            text = text.format(table=tabulate(data_dict.items(), tablefmt="grid"))
            html = html.format(table=tabulate(data_dict.items(), tablefmt="html"))
            
            message = MIMEMultipart(
                "alternative", None, [MIMEText(text), MIMEText(html,'html')])

            
            message['Subject'] = subject
            message['From'] = 'your mail address' # Sender Mail
            message['To'] = recipient # Reciever Mail

            
            server.sendmail(
                message['From'],
                message['To'],
                message.as_string()
            )
            print('Email has been sent!')

    server.quit()

def initiate_covid():
    data_dict = get_data(Country)
    send_mail(data_dict) 
    return

#scheduled for every 4 hours
schedule.every(4).hours.do(initiate_covid)

while True:
    schedule.run_pending()
    time.sleep(1) 
