from datetime import datetime
from pprint import pprint
import xml.etree.ElementTree as ET
import requests

def get_usd_price():
    """Получаем актуальный курс доллара от ЦБ
    Returns: float курс долл
    """
    valute = 0
    try:
        response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp?date_req=' + datetime.now().strftime(('%d/%m/%Y')))
        response = ET.fromstring(response.text)
        usd = response.find("Valute[@ID='R01235']")
        valute = float(usd[4].text.replace(',', '.'))
    except Exception as e:
        pprint('[INFO CB] Error while getting valute', e)
    finally:
        return valute