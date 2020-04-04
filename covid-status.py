import urllib.request
from bs4 import BeautifulSoup
from httplib2 import Http
from json import dumps
import datetime
import re
import sys


class Covid19_Report_IN():

    def smartshift_Bot(self, message, webhook_url):

        url = webhook_url

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

            KA_Report = None
            IN_Report_1 = None
            for table in table_data:
                for data in table:
                    if data == "Karnataka":
                        KA_Report = table
                    if data == "Total number of confirmed cases in India":
                        IN_Report_1 = table

            print(KA_Report)
            print(IN_Report_1)

            fail_report = "*Report generation is failed!*"
            sap_automation = "https://chat.googleapis.com/v1/spaces/AAAAimyyXHo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=u-1wNxlL_j45X0AK9iLHlBMok4ZLF779YpGv59mLXc8%3D"
            SS_India_Group = "https://chat.googleapis.com/v1/spaces/AAAAimyyXHo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=u-1wNxlL_j45X0AK9iLHlBMok4ZLF779YpGv59mLXc8%3D"

            if IN_Report_1 is None:
                self.smartshift_Bot(fail_report, sap_automation)
                sys.exit()

            IN_Report = []
            for element in IN_Report_1:
                IN_Report.append(re.sub('[^0-9,.]', '', element))

            print(IN_Report)

            active_cases = int(IN_Report[1]) - int(IN_Report[2]) - int(IN_Report[3])
            total_cases = int(IN_Report[1])
            active_KA = int(KA_Report[2])

            currentDT = datetime.datetime.now()

            date = currentDT.strftime("%a, %b %d, %Y") + ' at ' + currentDT.strftime("%I:%M:%S %p")

            report = "*Good Morning Everyone!*\n\n" \
                     "*Current Status of COVID-19 in India as on _" + date + "_*\n\n" \
                     "```Total Number of Active Covid-19 Cases so far across India : " + str(active_cases) + "\n\n" \
                     "Total Number of Cured/Migrated Cases      : " + str(IN_Report[2]) + "\n" \
                     "Total Number of Deaths due to Covid-19    : " + str(IN_Report[3]) + "\n" \
                     "Total Number of Active cases in Karnataka : " + str(active_KA) + "\n\n" \
                     "Total Confirmed Covid-19 Cases registered so far across India : " + str(total_cases) + "```\n" \
                     "*For State Wise Report Visit -> <https://www.mohfw.gov.in/|Ministry of Health & Family Welfare>*\n\n" \
                     "*Follow Hygiene! Stay Home! And Stay Safe!*"

            self.smartshift_Bot(report, sap_automation)


s = Covid19_Report_IN()
print(s.covid_report())
