import urllib.request
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from httplib2 import Http
from json import dumps
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import datetime


class CovidIndia():

    def hangout(self, active, cured, deaths, total):

        url = '<WEBHOOK URL>'
        currentDT = datetime.datetime.now()

        date = currentDT.strftime("%a, %b %d, %Y") + ' | ' + currentDT.strftime("%I:%M:%S %p")

        bot_message = {
                      "text": "*Gud Morning Everyone!* \n\n"
                              "*Current Status of COVID 2019 as of _" + date + "_*\n\n"
                              "```Total number of Confirmed Cases across India : " + str(total) + "\n"
                              "Total number of Active cases across India    : " + str(active) + "\n"
                              "Total number of Cured Cases across India     : " + str(cured) + "\n"
                              "Total number of Deaths across India          : " + str(deaths) + "```"
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
            cons_report = []
            for element in report:
                cons_report.append(element.strip())

            print(cons_report)

            active_cases = int(cons_report[2]) + int(cons_report[3]) - int(cons_report[4]) - int(cons_report[5])
            total_cases = int(cons_report[2]) + int(cons_report[3]) + int(cons_report[4]) + int(cons_report[5])

            print("Total number of Active COVID 2019 cases across India :", active_cases)
            print("Total number of Cured/Discharged COVID 2019 cases across India :", cons_report[4])
            print("Total number of Deaths due to COVID 2019 across India :", cons_report[5])

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

            self.hangout(active_cases, cons_report[4], cons_report[5], total_cases)

s = CovidIndia()
print(s.covid_report())
#s.hangout()