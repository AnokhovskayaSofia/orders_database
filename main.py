import asyncio
from db import DB
from cb import get_usd_price
from telegram import Bot
from googlesheets import GoogleSheet
from pprint import pprint

from apscheduler.schedulers.asyncio import AsyncIOScheduler



if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    gsheet = GoogleSheet()
    db = DB()
    bot = Bot()
    print('[INFO  __main__] committing table')
    table = gsheet.get_data_sheetfile()
    if table:
        dbtable = gsheet.prepare_data_sheetfile(table, get_usd_price())
        db.update_db(dbtable)
        bot.send_message_overdue_orders(gsheet.overdue_orders(table), db.getdate_db())

        print('[INFO  __main__] done!')
    else:
        print('[INFO __main__] Error while changing table. Table is empty.')

    
    async def usd_change_job():
        db.update_rub_cost(get_usd_price())
        print('[INFO currency_rate_check_job] the USD-RUB currency rate :', get_usd_price())

    async def sheet_change_job():
        print('[INFO sheet_change_job] checking the spreadsheet')
        if not gsheet.changes_in_file(gsheet.saved_start_page_token):
            print('[INFO sheet_change_job] no changes')
            return

        print('[INFO  sheet_change_job] committing changes')
        table = gsheet.get_data_sheetfile()
        if table:
            dbtable = gsheet.prepare_data_sheetfile(table, get_usd_price())
            db.update_db(dbtable)
            bot.send_message_overdue_orders(gsheet.overdue_orders(table), db.getdate_db())
            
            print('[INFO  sheet_change_job] done!')
        else:
            print('[INFO sheet_change_job] Error while changing table. Table is empty.')
        print('[INFO  sheet_change_job] done!')
        

    scheduler.add_job(usd_change_job, "interval", hours=1)
    scheduler.add_job(sheet_change_job, "interval", seconds=15)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        asyncio.get_event_loop().stop()
