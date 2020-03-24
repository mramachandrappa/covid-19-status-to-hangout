import urllib.request
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from httplib2 import Http
from json import dumps
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import datetime
import re


class CovidIndia():

    def hangout(self, active, ind_national, foreign_national, cured, deaths, total):

        url = '<INCOMING-WEBHOOK-URL>'
        currentDT = datetime.datetime.now()

        date = currentDT.strftime("%a, %b %d, %Y") + ' | ' + currentDT.strftime("%I:%M:%S %p")

        message = "*Good Morning Everyone!*\n\n" \
                  "*Current Status of COVID-19 in India as on _" + date + "_*\n\n" \
                  "```Total Number of Active Covid-19 Cases so far across India : " + str(active) + "\n\n" \
                  "Total Number of Cases(Indian National)    : " + str(ind_national) + "\n" \
                  "Total Number of Cases(Foreign National)   : " + str(foreign_national) + "\n" \
                  "Total Number of Cured/Migrated Cases      : " + str(cured) + "\n" \
                  "Total Number of Deaths due to Covid-19    : " + str(deaths) + "\n\n" \
                  "Total Count of Confirmed Covid-19 Cases so far across India : " + str(total) + "```\n" \
                  "*For State Wise Report Visit -> <https://www.mohfw.gov.in/|Ministry of Health & Family Welfare>*\n\n" \
                  "*Follow Hygiene! Stay Home! And Stay Safe!*"

        bot_message = {
                    "text": message
        }

        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

        http_obj = Http()

        response = http_obj.request(
                uri=url,
                method='POST',
                headers=message_headers,
                body=dumps(bot_message),
        )

        print(response)

    def covid_report(self):
            url = 'https://www.mohfw.gov.in/'
            response = urllib.request.urlopen(url)

            soup = BeautifulSoup(response, 'lxml')
            soup_table = soup.find('table')
            table_rows = soup_table.findAllNext('tr')

            table_data = []
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]
                table_data.append(row)

            report = ['Consolidated Report'] + table_data[len(table_data) - 1]

            print(report)
            cons_report = []
            for element in report:
                cons_report.append(re.sub('[^0-9,.]', '', element))

            print(cons_report)

            active_cases = int(cons_report[2]) + int(cons_report[3]) - int(cons_report[4]) - int(cons_report[5])
            total_cases = int(cons_report[2]) + int(cons_report[3]) + int(cons_report[4]) + int(cons_report[5])

            print("Total number of Active COVID 2019 cases across India :", active_cases)
            print("Total number of Cured/Discharged COVID 2019 cases across India :", cons_report[4])
            print("Total number of Deaths due to COVID 2019 across India :", cons_report[5])
            print("Total count of cases :", total_cases)

            #data = table_data[6:-1]

            #table = PrettyTable()
            #table.title = 'Covid-19 report of India'
            #table.field_names = ['SL.No', 'State', 'Confirmed Cases[Indian National]',
             #                    'Confirmed Cases[Foreign National]', 'Cured/Discharged/Migrated', 'Death']

            #for row in data:
              #  table.add_row(row)

            #table.add_row(['--------------', '--------------', '--------------', '--------------', '--------------',
             #              '--------------'])
            #table.add_row(cons_report)

            #print(data)

            #df = pd.DataFrame(data, columns=['SL.No', 'State', 'Indian National', 'Foreign National', 'Cured', 'Death'])
            #print(df)
            #print(table)

            #f = open("data.txt", "w")
            #f.write(str(df))
            #f.close()

            self.hangout(active_cases, cons_report[2], cons_report[3], cons_report[4], cons_report[5], total_cases)

s = CovidIndia()
print(s.covid_report())
#s.hangout()