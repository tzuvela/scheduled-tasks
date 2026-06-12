##################### Normal Starting Project ######################
import pandas
import random
from datetime import datetime
import smtplib
from io import StringIO

import os
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

today_tuple = datetime.now().month, datetime.now().day
# print(today)

csv_data = os.environ.get("BIRTHDAYS_CSV")
data = pandas.read_csv(StringIO(csv_data))
# print(data)

birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
# print(birthdays_dict)

if (today_tuple) in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]

    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]",birthday_person["name"])
        # print(contents)

    with smtplib.SMTP("smtp.gmail.com",587) as conn:
        conn.ehlo()
        conn.starttls()
        conn.ehlo()
        conn.login(MY_EMAIL, MY_PASSWORD)
        conn.sendmail(from_addr=MY_EMAIL,
                      to_addrs=birthday_person["email"],
                      msg=f"Subject:Happy Birthday!\n\n{contents}"
        )






