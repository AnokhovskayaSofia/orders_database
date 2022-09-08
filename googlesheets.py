from oauth2client.service_account import ServiceAccountCredentials
from config import *
import httplib2
from googleapiclient import discovery 
from pprint import pprint
import datetime as dt


class GoogleSheet():
    def __init__(self):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
                sheet_file,
                [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
            )
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service_d = discovery.build('drive', 'v3', http = self.httpAuth)
        self.service_s = discovery.build('sheets', 'v4', http = self.httpAuth)
        self.saved_start_page_token = self.service_d.changes().getStartPageToken().execute().get("startPageToken")

    def get_data_sheetfile(self):
        """Получаем данные из файла (гугл таблицы)
        """
        values = self.service_s.spreadsheets().values().get(
            spreadsheetId=google_file_ID,
            range='Sheet1',
            majorDimension='ROWS'
        ).execute()
        return values.get('values')

    def prepare_data_sheetfile(self, table: list, usd: float):
        """Подготовка данных для записи в БД
        Input : данные для изменения
        Input : актуальный курс доллара

        Return : модифицированные данные
        """
        if table:
            for item in table[1:]:
                if len(item) == 4:
                    item[3] = str(item[3].replace('.','-'))
                    item.append(int(item[2])*usd)
            return table
        else:
            print('[INFO Sheet] Error while changing table. Table is empty.')


    def changes_in_file(self, saved_start_page_token: int):
        """Узнаем есть ли изменения в файле
        Input : сохраненный токен с прошлого изменения
        """
        were_changes_in_a_file = False
        page_token = self.saved_start_page_token
        while page_token is not None:
            try:
                changes = self.service_d.changes().list(pageToken=page_token).execute()
                for change in changes.get('changes'):
                    file_id =  change.get("fileId")
                    if file_id == google_file_ID:
                        were_changes_in_a_file = True
                if 'newStartPageToken' in changes:
                    self.saved_start_page_token = changes.get('newStartPageToken')
                page_token = changes.get('nextPageToken')

                if not page_token:
                    break
            except Exception as ex:
                self.saved_start_page_token = None
                print('[INFO Sheet] Error while finding changes in file', ex)
            break
        return were_changes_in_a_file

    def overdue_orders(self, table):
        """Поиск просроченных заказов
        Input : данные заказов

        Return : номера просроченных заказах
        """
        result =[]
        if table:
            for item in table[1:]:
                if dt.datetime.strptime(item[3], '%d-%m-%Y') < dt.datetime.now():
                    result.append(item[1])
        return result