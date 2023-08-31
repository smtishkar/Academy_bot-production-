from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from data_base import sqlite_db
from create_bot import dp, bot
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers import client
from datetime import datetime

CHANEL_ID = '-1001870060633'  # Это канал

chat_admins = None
admin_list = []


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


class FSMTrainings(StatesGroup):
    photo = State()
    training_name = State()
    short_name = State()
    for_whom = State()
    description = State()
    format = State()
    price = State()


class FSMPost(StatesGroup):
    topic = State()
    content = State()


class FSMSend(StatesGroup):
    id_question = State()


class FSMScedule(StatesGroup):
    training_name = State()
    for_whom = State()
    start_date = State()
    end_date = State()
    format = State()
    price = State()


# Основная комада для доступа к функциям админа. Получаем ID текущего модератора
async def make_changes_command(message: types.Message):
    global chat_admins
    chat_admins = await bot.get_chat_administrators(CHANEL_ID)
    for admins in chat_admins:
        user_id = admins.user.id
        if user_id not in admin_list:
            admin_list.append(user_id)
    await bot.send_message(message.from_user.id, admin_list)
    if message.from_user.id in admin_list:
        await bot.send_message(message.from_user.id, 'Что хозяин надо???', reply_markup=admin_kb.button_case_admin)
        await message.delete()


"""*********************************БЛОК ЗАГРУЗКИ ОПИСАНИЯ ТРЕНИНГОВ***************************************"""


async def training_description_menu(message: types.Message):
    if message.from_user.id in admin_list:
        await bot.send_message(message.from_user.id, 'Выберите пункт меню:',
                               reply_markup=admin_kb.kb_training_description)


async def cm_training_start(message: types.Message):
    if message.from_user.id in admin_list:
        await FSMTrainings.photo.set()
        await bot.send_message(message.from_user.id, 'Давайте начнем регистрацию тренингов',
                               reply_markup=admin_kb.admin_cancel_kb)
        await message.reply('Загрузи фото')


async def load_training_photo(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':  # TODO придумать обработку отмены. Из-за фото у нас не получается отмена
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.kb_training_description)
        else:
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
            await FSMTrainings.next()
            await message.reply('Теперь введите название', reply_markup=admin_kb.admin_cancel_kb)


async def load_training_name(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.kb_training_description)
        else:
            async with state.proxy() as data:
                data['training_name'] = message.text
            await FSMTrainings.next()
            await message.reply('Введите краткое название тренинга', reply_markup=admin_kb.admin_cancel_kb)


async def load_training_short_name(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.kb_training_description)
        else:
            async with state.proxy() as data:
                data['short_name'] = message.text
            await FSMTrainings.next()
            await message.reply('Введите целевую аудиторию', reply_markup=admin_kb.admin_cancel_kb)


async def load_for_whom(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.kb_training_description)
        else:
            async with state.proxy() as data:
                data['for_whom'] = message.text
            await FSMTrainings.next()
            await message.reply('Введите содержание тренинга', reply_markup=admin_kb.admin_cancel_kb)


async def load_training_description(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.kb_training_description)
        else:
            async with state.proxy() as data:
                data['description'] = message.text
            await FSMTrainings.next()
            await message.reply('Введите формат тренинга (Очно/Вебинар)', reply_markup=admin_kb.admin_cancel_kb)


async def load_format(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.kb_training_description)
        else:
            async with state.proxy() as data:
                data['format'] = message.text
            await FSMTrainings.next()
            await message.reply('Введите цену', reply_markup=admin_kb.admin_cancel_kb)


async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.kb_training_description)
        else:
            async with state.proxy() as data:
                data['price'] = message.text
            await sqlite_db.sql_add_training(state)
            await bot.send_message(message.from_user.id, 'Тренинг добавлен в список',
                                   reply_markup=admin_kb.kb_training_description)
            await state.finish()


async def delete_training_description(message: types.Message):
    if message.from_user.id in admin_list:
        read = await sqlite_db.sql_read_trainings2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0],
                                 f'Название: {ret[1]}\nЦелевая аудитория: {ret[3]}\nСодержание:\n{ret[4]}\n\
                                 Формат: {ret[5]}\nЦена: {ret[-1]}')
            await bot.send_message(chat_id=message.from_user.id,
                                   text='^^^',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton("Удалить", callback_data=f'Remove {ret[2]}')))
        await bot.send_message(message.from_user.id, 'Что делать дальшей?', reply_markup=admin_kb.main_menu_button)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Remove '))
async def del_callback_schedule(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_training_description(callback_query.data.replace('Remove ', ''))
    await callback_query.answer(text='Описание тренинга удалено', show_alert=True)


"""***********************************************БЛОК ДЕЛАЕМ ПОСТ ************************************************"""

async def cm_post_start(message: types.Message):
    if message.from_user.id in admin_list:
        await FSMPost.topic.set()
        await bot.send_message(message.from_user.id, 'Давайте начнем создавать пост')
        await message.reply('Введите название поста', reply_markup=admin_kb.admin_cancel_kb)


async def load_topic_name(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.button_case_admin)
        else:
            async with state.proxy() as data:
                data['topic'] = message.text
            await FSMPost.next()
            await message.reply('Введите содержание поста', reply_markup=admin_kb.admin_cancel_kb)


async def load_content(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.button_case_admin)
        else:
            async with state.proxy() as data:
                data['content'] = message.text
            await bot.send_message(CHANEL_ID,
                                   text=f"<b>Тема:</b> {data['topic']}\n<b>Содержание:</b> {data['content']}",
                                   parse_mode='html')
            read = await sqlite_db.sql_read_users()    #TODO Рассылка сообщений
            for ret in read:
                await bot.send_message(ret[0],
                                       text=f"<b>Тема:</b> {data['topic']}\n<b>Содержание:</b> {data['content']}",
                                       parse_mode='html')
            await bot.send_message(message.from_user.id, 'Пост опубликован', reply_markup=admin_kb.button_case_admin)
            await state.finish()


"""***********************************************БЛОК ОТВЕТОВ НА ВОПРОСЫ*******************************************"""


# Проверяем все вопросы где статус != Done
async def questions_check(message: types.Message):
    if message.from_user.id in admin_list:
        await sqlite_db.sql_read_questions(message)
        await bot.send_message(message.from_user.id, 'Что делаем дальше?', reply_markup=admin_kb.processing_buttons)


# Отвечаем на вопрос клиента
async def cm_reply_to_customer_start(message: types.Message):
    if message.from_user.id in admin_list:
        await client.FSMQuestion.question_id.set()
        await bot.send_message(message.from_user.id, 'Введите номер вопроса', reply_markup=admin_kb.admin_cancel_kb)


async def load_question_id(message: types.Message, state: FSMContext):  # TODO обработка если вопроса нет в списке
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.processing_buttons)
        else:
            async with state.proxy() as data:
                data['question_id'] = message.text
            await client.FSMQuestion.next()
            await message.reply('Введите ответ на вопрос дилера')


async def load_reply_to_customer_question(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.processing_buttons)
        else:
            async with state.proxy() as data:
                data['reply'] = message.text
            read = await sqlite_db.sql_read_questions2()
            for ret in read:
                if ret[0] == int(data['question_id']):
                    data['reply_time'] = datetime.now().date()
                    await sqlite_db.sql_questions_add_reply(state)
            await state.finish()
            await message.reply('Ответ добавлен', reply_markup=admin_kb.processing_buttons)


# Отправка письма клиенту
async def cm_send_reply(message: types.Message):
    if message.from_user.id in admin_list:
        await FSMSend.id_question.set()
        await bot.send_message(message.from_user.id, 'Введите номер вопроса', reply_markup=admin_kb.processing_buttons)


async def load_question_id_for_sending_reply(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.processing_buttons)
        else:
            async with state.proxy() as data:
                data['id_question'] = message.text
            read = await sqlite_db.sql_read_questions2()
            for ret in read:
                if ret[0] == int(data['id_question']):
                    await bot.send_message(ret[1],
                                           f"ID вашего вопроса: {ret[0]}\nТекст вопроса: {ret[6]}\nОтвет: {ret[8]}")
            await state.finish()


# Меняем статус вопроса дилера
async def questions_check_for_work(message: types.Message):
    if message.from_user.id in admin_list:
        read = await sqlite_db.sql_read_questions2()
        for ret in read:
            await bot.send_message(message.from_user.id,
                                   f'Question_id: {ret[0]}\nUser_ID: {ret[1]}\nФИО: {ret[2]} {ret[3]}\n\
                                   Должность: {ret[4]}\nДЦ: {ret[5]}\nВопрос: {ret[6]}\nСтатус: {ret[7]}\
                                   Ответ: {ret[8]}')
            await bot.send_message(chat_id=message.from_user.id,
                                   text='^^^',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton("Изменить_статус", callback_data=f'change {ret[0]}')))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('change '))
async def change_status(callback_query: types.CallbackQuery):
    await sqlite_db.sql_questions_change_status(callback_query.data.replace('change ', ''))
    await callback_query.answer(text=f'Статус изменен', show_alert=True)


async def back_to_main_admin(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=admin_kb.button_case_admin)


"""***************************************БЛОК ЗАПИСИ НА ТРЕНИНГ**************************************"""


# Проверяем все вопросы где статус != Done
async def training_requests_check(message: types.Message):
    if message.from_user.id in admin_list:
        await sqlite_db.sql_read_questions(message)
        await bot.send_message(message.from_user.id, 'Что делаем дальше?', reply_markup=admin_kb.processing_buttons)


# Отвечаем на вопрос клиента
async def cm_reply_to_customer_start(message: types.Message):
    if message.from_user.id in admin_list:
        await client.FSMQuestion.question_id.set()
        await bot.send_message(message.from_user.id, 'Введите номер вопроса', reply_markup=admin_kb.admin_cancel_kb)


async def load_question_id(message: types.Message, state: FSMContext):  # TODO обработка если вопроса нет в списке
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.processing_buttons)
        else:
            async with state.proxy() as data:
                data['question_id'] = message.text
            await client.FSMQuestion.next()
            await message.reply('Введите ответ на вопрос дилера')


async def load_reply_to_customer_question(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.processing_buttons)
        else:
            async with state.proxy() as data:
                data['reply'] = message.text
            read = await sqlite_db.sql_read_questions2()
            for ret in read:
                if ret[0] == int(data['question_id']):
                    await sqlite_db.sql_questions_add_reply(state)
            await state.finish()
            await message.reply('Ответ добавлен', reply_markup=admin_kb.processing_buttons)


# Отправка письма клиенту
async def cm_send_reply(message: types.Message):
    if message.from_user.id in admin_list:
        await FSMSend.id_question.set()
        await bot.send_message(message.from_user.id, 'Введите номер вопроса', reply_markup=admin_kb.processing_buttons)


async def load_question_id_for_sending_reply(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.processing_buttons)
        else:
            async with state.proxy() as data:
                data['id_question'] = message.text
            read = await sqlite_db.sql_read_questions2()
            for ret in read:
                if ret[0] == int(data['id_question']):
                    await bot.send_message(ret[1],
                                           f"ID вашего вопроса: {ret[0]}\nТекст вопроса: {ret[6]}\nОтвет: {ret[8]}")
            await state.finish()


# Меняем статус вопроса дилера
async def questions_check_for_work(message: types.Message):
    if message.from_user.id in admin_list:
        read = await sqlite_db.sql_read_questions2()
        for ret in read:
            await bot.send_message(message.from_user.id,
                                   f'Question_id: {ret[0]}\nUser_ID: {ret[1]}\nФИО: {ret[2]} {ret[3]}\n\
                                   Должность: {ret[4]}\nДЦ: {ret[5]}\nВопрос: {ret[6]}\nСтатус: {ret[7]}\n\
                                   Ответ: {ret[8]}')
            await bot.send_message(chat_id=message.from_user.id,
                                   text='^^^',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton("Изменить_статус", callback_data=f'change {ret[0]}')))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('change '))
async def change_status(callback_query: types.CallbackQuery):
    await sqlite_db.sql_questions_change_status(callback_query.data.replace('change ', ''))
    await callback_query.answer(text=f'Статус изменен', show_alert=True)


async def back_to_main_admin(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=admin_kb.button_case_admin)


"""***************************************БЛОК ВНЕСЕНИЯ ТРЕНИНГОВ В РАСПИСАНИЕ**************************************"""


async def cm_schedule_start(message: types.Message):
    if message.from_user.id in admin_list:
        await FSMScedule.training_name.set()
        await bot.send_message(message.from_user.id, 'Давайте внесем тренинг в расписание')
        await message.reply('Введите название тренинга', reply_markup=admin_kb.admin_cancel_kb)


async def load_training_name_for_schedule(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.button_case_admin)
        else:
            async with state.proxy() as data:
                data['training_name'] = message.text
            await FSMScedule.next()
            await message.reply('Введите целевую аудиторию', reply_markup=admin_kb.admin_cancel_kb)


async def load_for_whom_for_schedule(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.button_case_admin)
        else:
            async with state.proxy() as data:
                data['for_whom'] = message.text
            await FSMScedule.next()
            await message.reply('Введите дату начала тренинга (формат: 20.02.2022)',
                                reply_markup=admin_kb.admin_cancel_kb)


async def load_start_date(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.button_case_admin)
        else:
            async with state.proxy() as data:
                data['start_date'] = message.text
            await FSMScedule.next()
            await message.reply('Введите дату окончания тренинга (формат: 20.02.2022)',
                                reply_markup=admin_kb.admin_cancel_kb)


async def load_end_date(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.button_case_admin)
        else:
            async with state.proxy() as data:
                data['end_date'] = message.text
            await FSMScedule.next()
            await message.reply('Введите формат тренинга', reply_markup=admin_kb.admin_cancel_kb)


async def load_training_format_for_schedule(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.button_case_admin)
        else:
            async with state.proxy() as data:
                data['format'] = message.text
            await FSMScedule.next()
            await message.reply('Введите стоимость', reply_markup=admin_kb.admin_cancel_kb)


async def load_training_price_for_schedule(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_list:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.reply('Ввод отменен, выберите пункт меню', reply_markup=admin_kb.button_case_admin)
        else:
            async with state.proxy() as data:
                data['price'] = message.text
            await sqlite_db.sql_add_training_schedule(state)
            await message.reply('На этому все. Тренинг добавлен в расписание!', reply_markup=admin_kb.button_case_admin)
            await state.finish()


async def delete_schedule(message: types.Message):
    if message.from_user.id in admin_list:
        read = await sqlite_db.sql_read_schedule2()
        for ret in read:
            await bot.send_message(message.from_user.id,
                                   f'Название: {ret[1]}\nНачало тренинга: {ret[2]}\nОкончание тренинга: {ret[3]}\n\
                                   Формат: {ret[4]}\nЦена: {ret[-1]}')
            await bot.send_message(chat_id=message.from_user.id,
                                   text='^^^',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton("Удалить", callback_data=f'del {ret[0]}')))
        await bot.send_message(message.from_user.id, 'Что делать дальшей?', reply_markup=admin_kb.main_menu_button)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_schedule(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_schedule(callback_query.data.replace('del ', ''))
    await callback_query.answer(text='Тренинг удален из расписания', show_alert=True)


"""***********************************************************************************************************"""

#Обновляем базу САБА
# async def db_update(message: types.Message):
#     if message.from_user.id in admin_list:
#         excel_data_df = read_excel('lms_id.xlsx', sheet_name='sheet1')
#         id_saba = excel_data_df['ID'].tolist()              #TODO база ни куда не передается
#         return id_saba
async def menu_schedule(message: types.Message):
    if message.from_user.id in admin_list:
        await bot.send_message(message.from_user.id, 'Что будем делать дальше?:', reply_markup=admin_kb.schedule_kb)


async def main_menu(message: types.Message):
    if message.from_user.id in admin_list:
        await bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=admin_kb.button_case_admin)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id in admin_list:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                                   add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


# Регистрация Хендлеров
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(questions_check, lambda message: 'Проверить вопросы дилеров' in message.text)
    dp.register_message_handler(questions_check_for_work, lambda message: 'Изменить статус' in message.text)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'])
    dp.register_message_handler(cm_training_start, lambda message: 'Добавить описание тренинга' in message.text,
                                state=None)
    dp.register_message_handler(load_training_photo, content_types=['photo'], state=FSMTrainings.photo)
    dp.register_message_handler(load_training_name, state=FSMTrainings.training_name)
    dp.register_message_handler(load_training_short_name, state=FSMTrainings.short_name)
    dp.register_message_handler(load_for_whom, state=FSMTrainings.for_whom)
    dp.register_message_handler(load_training_description, state=FSMTrainings.description)
    dp.register_message_handler(load_format, state=FSMTrainings.format)
    dp.register_message_handler(load_price, state=FSMTrainings.price)
    dp.register_message_handler(cm_post_start, lambda message: 'Сделать пост' in message.text, state=None)
    dp.register_message_handler(load_topic_name, state=FSMPost.topic)
    dp.register_message_handler(load_content, state=FSMPost.content)
    dp.register_message_handler(cm_reply_to_customer_start, lambda message: 'Ответить' in message.text, state=None)
    dp.register_message_handler(load_question_id, state=client.FSMQuestion.question_id)
    dp.register_message_handler(load_reply_to_customer_question, state=client.FSMQuestion.reply)
    dp.register_message_handler(cm_send_reply, lambda message: 'Отправить ответ' in message.text, state=None)
    dp.register_message_handler(load_question_id_for_sending_reply, state=FSMSend.id_question)
    dp.register_message_handler(back_to_main_admin, lambda message: 'В главное меню' in message.text)
    dp.register_message_handler(cm_schedule_start, lambda message: 'Добавить тренинг в расписание' in message.text,
                                state=None)
    dp.register_message_handler(load_training_name_for_schedule, state=FSMScedule.training_name)
    dp.register_message_handler(load_for_whom_for_schedule, state=FSMScedule.for_whom)
    dp.register_message_handler(load_start_date, state=FSMScedule.start_date)
    dp.register_message_handler(load_end_date, state=FSMScedule.end_date)
    dp.register_message_handler(load_training_format_for_schedule, state=FSMScedule.format)
    dp.register_message_handler(load_training_price_for_schedule, state=FSMScedule.price)
    dp.register_message_handler(menu_schedule, lambda message: 'Тренинг расписание' in message.text)
    dp.register_message_handler(delete_schedule, lambda message: 'Удалить тренинг из расписания' in message.text)
    dp.register_message_handler(main_menu, lambda message: 'Главное меню' in message.text)
    dp.register_message_handler(training_description_menu, lambda message: 'Список тренингов' in message.text)
    dp.register_message_handler(delete_training_description,
                                lambda message: 'Удалить опсиание тренинга' in message.text)
