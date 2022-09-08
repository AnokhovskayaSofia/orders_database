import telebot
from config import *
import datetime as dt

class Bot():
    def __init__(self):
        self.bot = telebot.TeleBot(telegram_token)

    def prepare_text(self, order_ids: list, table: list):
        """Подготовка текста для сообщения в Телеграмм из таблицы
        Input : номера просреченных заказах 
        Input : данные о всех заказах

        Return : список с сообщениями на отправку 
        """
        description_dict = {
            1: 'Номер заказа: ',
            2: 'Стоимость usd: ',
            3: 'СРОКИ ПОСТАВКИ: ',
            4: 'Стоимость в rub: ',
        }
        num=0
        result = []
        count_m = 0
        if order_ids:
            r = '-------------------------------------------------\n'
            r += '-------------------------------------------------\n'
            r = 'ПРОСРОЧЕННЫЕ ЗАКАЗЫ С ' + str(dt.datetime.now().date()) + '\n'
            r += '-------------------------------------------------\n'
            r += '-------------------------------------------------\n'
            result.append(r)
            count_m +=1
            r=''
            for row in table:
                if num <= len(order_ids)-1 and int(order_ids[num]) == int(row[1]):
                    for ind in range(1, len(row)):
                        r += description_dict[ind] + str(row[ind]) + ' | '
                    r += '\n'
                    r += '-------------------------------------------------\n'
                    # деление сообщений по 10 записей
                    if (num+1) % 10 == 0:
                        result.append(r)
                        count_m += 1
                        r=''
                    num+=1
                    
                    
            if r:
                result.append(r)
                    
        return result


    def send_message_overdue_orders(self, order_ids: list, orders: list):
        """Отправляем сообщение в Телеграмм про просроченные заказы.
        Input : номера просреченных заказах 
        Input : данные о всех заказах 
        """
        if order_ids:
            text = self.prepare_text(order_ids, orders)
            for mess in text:
                self.bot.send_message(channel_name, mess)