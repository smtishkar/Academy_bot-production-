from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db


async def on_startup(_):
    print('Бот запущен')                #Выводит в консоль служебную информацию, дальше поключим сюда еще и СУБД
    sqlite_db.sql_users()


from handlers import client,admin,other

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)