import sqlite3 as sq
from create_bot import dp,bot


"""******************************************БЛОК СОЗДАНИЯ ТАБЛИЦ************************************************"""
def sql_users():
    global base, cur
    base = sq.connect('academy.db')
    cur = base.cursor()
    if base:
        print('Academy database connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS users(user_id PRIMARY KEY, saba_id TEXT, first_name TEXT, last_name TEXT, job_title TEXT, dlr TEXT, creation_time TEXT)')
    base.execute(
        'CREATE TABLE IF NOT EXISTS trainings(img TEXT, training_name TEXT, short_name TEXT, for_whom TEXT, description TEXT, format TEXT, price TEXT)')
    base.execute(
        'CREATE TABLE IF NOT EXISTS schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, training_name TEXT, for_whom TEXT, start_date TEXT, end_date TEXT, format TEXT, price TEXT)')
    base.execute(
        'CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, first_name TEXT, last_name TEXT, job_title TEXT, dlr TEXT, question TEXT, status TEXT, reply TEXT, creation_time TEXT)')
    base.commit()
"""******************************************БЛОК ЗАПИСИ В ТАБЛИЦУ************************************************"""

async def sql_add_user_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO users (user_id, saba_id, creation_time) VALUES (?,?, ?)', tuple(data.values()))
        base.commit()

async def sql_add_training(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO trainings VALUES (?,?,?,?,?,?,?)', tuple(data.values()))
        base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))
        base.commit()

async def sql_add_questions(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO questions (user_id, first_name, last_name, job_title, dlr, question, status, creation_time) VALUES (?,?,?,?,?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_add_training_requests(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO questions (user_id, first_name, last_name, job_title, dlr, request, status) VALUES (?,?,?,?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_add_training_schedule(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO schedule (training_name, for_whom, start_date, end_date, format, price) VALUES (?,?,?,?,?,?)', tuple(data.values()))
        base.commit()



"""******************************************БЛОК ЧТЕНИЯ ТАБЛИЦ************************************************"""

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')


async def sql_read_users():
    return cur.execute('SELECT * FROM users').fetchall()

async def sql_read_schedule(message):
    for ret in cur.execute('SELECT * FROM schedule').fetchall():
        await bot.send_message(message.from_user.id,f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[2]}\n<b><u>Начало тренинга:</u></b> {ret[3]}\n<b><u>Окончание тренинга:</u></b> {ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}', parse_mode='HTML')

async def sql_read_trainings(message):
    for ret in cur.execute('SELECT * FROM trainings').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[3]}\n<b><u>Содержание:</u></b>\n{ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}', parse_mode='HTML')

async def sql_read_training_requests(message):
    for ret in cur.execute('SELECT * FROM trainings').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[3]}\n<b><u>Содержание:</u></b>\n{ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}', parse_mode='HTML')


async def sql_read_tech_trainings(message):
    for ret in cur.execute('SELECT * FROM trainings WHERE short_name LIKE "DT%"').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[3]}\n<b><u>Содержание:</u></b>\n{ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}', parse_mode='HTML')


async def sql_read_non_tech_trainings(message):
    for ret in cur.execute('SELECT * FROM trainings WHERE short_name LIKE "SA%"').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[3]}\n<b><u>Содержание:</u></b>\n{ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}', parse_mode='HTML')

async def sql_read_ucar_trainings(message):
    for ret in cur.execute('SELECT * FROM trainings WHERE short_name LIKE "UC%"').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[3]}\n<b><u>Содержание:</u></b>\n{ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}', parse_mode='HTML')

async def sql_read_tech_schedule(message):
    for ret in cur.execute('SELECT * FROM schedule WHERE for_whom LIKE "Механики-диагносты"').fetchall():
        # await bot.send_photo(message.from_user.id, ret[0], f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[3]}\n<b><u>Содержание:</u></b>\n{ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}', parse_mode='HTML')
        await bot.send_message(message.from_user.id,f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[2]}\n<b><u>Начало тренинга:</u></b> {ret[3]}\n<b><u>Окончание тренинга:</u></b> {ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}', parse_mode='HTML')

async def sql_read_non_tech_schedule(message):
    for ret in cur.execute('SELECT * FROM schedule WHERE for_whom LIKE "Сервисные консультанты"').fetchall():
        # await bot.send_photo(message.from_user.id, ret[0], f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[3]}\n<b><u>Содержание:</u></b>\n{ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}', parse_mode='HTML')
        await bot.send_message(message.from_user.id,
                               f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[2]}\n<b><u>Начало тренинга:</u></b> {ret[3]}\n<b><u>Окончание тренинга:</u></b> {ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}',
                               parse_mode='HTML')
async def sql_read_ucar_schedule(message):
    for ret in cur.execute('SELECT * FROM schedule WHERE for_whom LIKE "Закупщики автомобилей"').fetchall():
        # await bot.send_photo(message.from_user.id, ret[0], f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[3]}\n<b><u>Содержание:</u></b>\n{ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}', parse_mode='HTML')
        await bot.send_message(message.from_user.id,
                               f'<b><u>Название:</u></b> {ret[1]}\n<b><u>Целевая аудитория:</u></b> {ret[2]}\n<b><u>Начало тренинга:</u></b> {ret[3]}\n<b><u>Окончание тренинга:</u></b> {ret[4]}\n<b><u>Формат:</u></b> {ret[5]}\n<b><u>Цена:</u></b> {ret[-1]}',
                               parse_mode='HTML')

async def sql_read_trainings2():
    return cur.execute('SELECT * FROM trainings').fetchall()
async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()

async def sql_read_questions(message):
    for ret in cur.execute('SELECT * FROM questions WHERE status != "Done"').fetchall():
        await bot.send_message(message.from_user.id,f'Question_id: {ret[0]}\nUser_ID: {ret[1]}\nФИО: {ret[2]} {ret[3]}\nДолжность: {ret[4]}\nДЦ: {ret[5]}\nВопрос: {ret[6]}\nСтатус: {ret[7]}\nОтвет: {ret[8]}')

async def sql_read_questions2():
    return cur.execute('SELECT * FROM questions WHERE status != "Done"').fetchall()

async def sql_read_schedule2():
    return cur.execute('SELECT * FROM schedule').fetchall()

async def sql_questions_change_status(data):
    cur.execute('UPDATE questions SET status = "Done" WHERE id == ?', (data,))
    base.commit()

async def sql_questions_add_reply(state):
    async with state.proxy() as data:
        cur.execute('UPDATE questions SET reply = ?  WHERE id == ?', (data['reply'], data['question_id']))
        base.commit()

async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()

async def sql_delete_schedule(data):
    cur.execute('DELETE FROM schedule WHERE id == ?', (data,))
    base.commit()

async def sql_delete_training_description(data):
    cur.execute('DELETE FROM trainings WHERE short_name == ?', (data,))
    base.commit()

