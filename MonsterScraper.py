from Utils import  *
import json
from datetime import datetime

# Variables depending on the job your looking for and the location
job_kind = "python"         # "python developer" for example
job_location = "your_city"    # "berlin" for example

# Ggooglemail credentials
fromadr = "your_account@gmail.com"
passwd = "your_password"

# Email content
subject = "Application as a Python Developer"
attachement = "cv.pdf"
message = """\
------------------------
Insert your message here
------------------------
"""

# Date
now = datetime.now()
today = now.strftime("%Y%m%d")


def findJobMails():
    job_dict = createJobDict(job_kind, job_location)
    print(job_dict)
    job_emails = []
    for jobs in job_dict:
        mail = scrapeCompanyEmail(jobs + "+" + job_location)
        print(mail)
        job_emails.append(mail)
    job_string = today + "Jobs.txt"
    with open(job_string, "w") as fp:
        json.dump(job_emails, fp)


findJobMails()

# Send a testmail
writeMail("yourtestmail@provider.com",fromadr, message ,subject, passwd, attachement)


"""
The following code sends out the mail to the scraped emaillist.

"""
# with open(job_string, "r") as fp:
#    emaillist = json.load(fp)
#
# print(emaillist)
#
# for i in emaillist:
#     writeMail(i,fromadr, message ,subject, passwd, attachement)
