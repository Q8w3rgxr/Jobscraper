import requests
import smtplib
from bs4 import BeautifulSoup
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



def createJobDict(job_kind, job_location):
    URL = "https://www.monster.de/jobs/suche/?q=" + job_kind + "&where=" + job_location
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='ResultsContainer')
    job_elems = results.find_all('section', class_='card-content')
    Companylist = []


    for job_elem in job_elems:
        title_elem = job_elem.find('h2', class_='title')
        company_elem = job_elem.find('div', class_='company')
        location_elem = job_elem.find('div', class_='location')
        if None in (title_elem, company_elem, location_elem):
            continue
        Companylist.append(company_elem.text.strip())

        # print(title_elem.text.strip())
        # print(company_elem.text.strip())
        # print(location_elem.text.strip())

    return Companylist


def scrapeCompanyEmail(company):
    driver = webdriver.Chrome(executable_path="/Applications/chromedriver") # path to chromedriver
    URL = "https://www.startpage.com/do/dsearch?query=" + company
    driver.get(URL) 
    html = driver.page_source
    soup = BeautifulSoup(html,"lxml")
    driver.quit()

    result = soup.find('div', class_='w-gl__result-url-container')
    for a in result.find_all('a', href=True):
        print("Found the URL:", a['href'])
        compurl = a['href']

    compurl = compurl[compurl.find('.'):]
    compurl = compurl[1:]
    compurl = compurl.split("/")[0]
    return "jobs@" + compurl            # add most plausible prefix



def writeMail(toaddr,fromaddr, message, subject,passwd, attachement):
    """
    instance of MIMEMultipart
    storing the senders email address
    storing the receivers email address
    storing the subject
    storing the subject
    string to store the body of the mail
    attach the body with the msg instance
    open the file to be sent
    instance of MIMEBase and named as p
    To change the payload into encoded form
    encode into base64
    attach the instance 'p' to instance 'msg'
    creates SMTP session
    start TLS for security
    Authentication
    Converts the Multipart msg into a string
    sending the mail
    terminating the session
    """
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))
    filename = "cv.pdf"
    attachment = open(attachement, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, passwd)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    print("Email has been sent to " + toaddr)
