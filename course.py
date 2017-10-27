import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs4

currency_names = {
	"E_usd":"R01235",
	"E_eur":"R01239",
	"E_nok":"R01535"
}


today = datetime.today()
yesterday = today - timedelta(days = 1)

today =  today.strftime("%d/%m/%Y")
yesterday = yesterday.strftime("%d/%m/%Y")

def write_file(data, filename):
    with open(filename + ".txt", "w", encoding="utf-8") as file:
        file.write(str(data))


def get_currency (date):
	response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date)
	data = bs4(response.content, "lxml")
	valute = data.find("valute",id = currency_names[currency_name])
	value = str(valute.find("value").text)
	value = value.replace(',','.')


	return float(value[:-2])


if __name__ == '__main__':
	today = datetime.today()
	yesterday = today - timedelta(days = 1)

	today =  today.strftime("%d/%m/%Y")
	yesterday = yesterday.strftime("%d/%m/%Y")

	write_file(today, "E_date")

	for currency_name in currency_names:

		today_curre = (get_currency(today))
		yesterday_curre = (get_currency(yesterday))

		volatility = ("{0:.2f}".format(yesterday_curre - today_curre))

		write_file(today_curre, currency_name)
		write_file(volatility, currency_name + "_mod" )

		print (today_curre, yesterday_curre, volatility)
		