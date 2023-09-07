import pandas
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
from keyboards.client_kb import kb_client, registration_kb, kb_cancel, trainings_kb, kb_ask, schedule_kb
from data_base import sqlite_db
from datetime import datetime
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMClient(StatesGroup):
    saba_id = State()


class FSMQuestion(StatesGroup):
    question = State()
    question_id = State()
    reply = State()


class FSMReset(StatesGroup):
    new_id = State()


class FSMTrainingRequest(StatesGroup):
    request = State()


excel_data_df = pandas.read_excel('lms_id.xlsx', sheet_name='sheet1')
id_saba = excel_data_df['ID'].tolist()

"""*********************************БЛОК РЕГИСТРАЦИИ ПОЛЬЗОВАТЕЛЕЙ***************************************"""


async def client_start(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        # changed_id = ''
        # if "_" in ret[1]:
        #     changed_id = ret[1].replace('_', "#")
        #     test_dict[ret[0]] = changed_id
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key in test_dict and str(values).upper() in id_saba:
            await bot.send_message(message.from_user.id, 'Проверка ID номеров пройдена успешно!')
            await bot.send_message(message.from_user.id,
                                   'Добро пожаловать в Академию👋! Я бот, который будет помогать вам получать '
                                   'интересующую вас информацию и всегда оставаться в курсе последних новостей '
                                   'Академии Тойота 📰. Я нахожусь на первоначальном этапе разработки и поддерживаюсь '
                                   'энтузиазмом сотрудников академии. Постепенно моя функциональность будет '
                                   'расти и я буду еще более полезен.',
                                   reply_markup=kb_client)
        elif message.from_user.id == key and str(values).upper() not in id_saba:
            await bot.send_message(message.from_user.id,
                                   'Вы есть в базе, но видимо указан не корректный ID в учебном портале, '
                                   'обратитесь к администратору',
                                   reply_markup=kb_ask)
            await bot.send_message(message.from_user.id, f'Указанный САБА ID - {values}')
    if message.from_user.id not in test_dict:
        await FSMClient.saba_id.set()
        await bot.send_message(message.from_user.id, 'Давайте начнем регистрацию!')
        await message.reply('Введите ваше ID используемый на портале САБА (learn@toyota)',
                            reply_markup=types.ReplyKeyboardRemove())


async def load_saba_id(message: types.Message, state: FSMContext):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    if str(message.text) not in test_dict.values():
        await message.reply(message.text)
        async with state.proxy() as data:
            data['user_id'] = message.from_user.id
            data['saba_id'] = str(message.text).upper()
            if '_' in data['saba_id']:
                data['saba_id'] = data['saba_id'].replace('_', '#')
            data['Creation_time'] = datetime.now().date()
        await sqlite_db.sql_add_user_command(state)
        await state.finish()
        await message.reply(
            'Вы зарегистрированы, теперь можете еще раз ввести "/start" для доступа к основным функциям')
    else:
        async with state.proxy() as data:
            data['user_id'] = message.from_user.id
            data['saba_id'] = None
            data['Creation_time'] = datetime.now().date()
        await sqlite_db.sql_add_user_command(state)
        await state.finish()
        await bot.send_message(message.from_user.id,
                               'указанный id уже есть в базе обратитесть в академию', reply_markup=kb_ask)


"""*********************************БЛОК ЗАДАВАНИЯ ВОПРОСОВ****************************************************"""


async def cm_question_start(message: types.Message):
    await FSMQuestion.question.set()
    await bot.send_message(message.from_user.id, 'Введите ваш вопрос', reply_markup=kb_cancel)


async def load_question(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await message.reply('Ввод отменен, выберите пункт меню', reply_markup=kb_client)
    else:
        async with state.proxy() as data:
            read = await sqlite_db.sql_read_users()
            for ret in read:
                if message.from_user.id == ret[0]:
                    data['user_id'] = ret[0]
                    data['first_name'] = ret[1]
                    data['last_name'] = ret[2]
                    data['job_title'] = ret[3]
                    data['dlr_for'] = ret[4]
                    data['question'] = message.text
                    data['question_status'] = "in process"
                    data['Creation_time'] = datetime.now().date()
        await sqlite_db.sql_add_questions(state)
        await state.finish()
        await message.reply('Спасибо вам за обращение, скоро мы вернемся с информацией!')


"""*********************************БЛОК ЗАПИСИ НА ТРЕНИНГ****************************************************"""


async def cm_training_request_start(message: types.Message):
    await FSMTrainingRequest.request.set()
    await bot.send_message(message.from_user.id,
                           'Введите информацию в свободной форме. Обязательно укажите ФИО участника, дилерский центр,'
                           'название тренанга/ов и дату начала',
                           reply_markup=kb_cancel)


async def load_request(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await message.reply('Ввод отменен, выберите пункт меню', reply_markup=kb_client)
    else:
        async with state.proxy() as data:
            read = await sqlite_db.sql_read_users()
            for ret in read:
                if message.from_user.id == ret[0]:
                    data['user_id'] = ret[0]
                    data['first_name'] = ret[1]
                    data['last_name'] = ret[2]
                    data['job_title'] = ret[3]
                    data['dlr_for'] = ret[4]
                    data['request'] = "Запись на тренинг -" + message.text
                    data['question_status'] = "in process"
                    data['Creation_time'] = datetime.now().date()
        await sqlite_db.sql_add_questions(state)
        await state.finish()
        await message.reply('Ваш запрос принят! Скоро мы вернемся к вам с информацией.')


"""*********************************БЛОК ЗАПРОСА НА КОРРЕКТИРОВКУ ID**********************************************"""


async def cm_id_correction(message: types.Message):
    await FSMReset.new_id.set()
    await bot.send_message(message.from_user.id, 'Введите корректный ID',
                           reply_markup=types.ReplyKeyboardRemove())  # TODO заменить клавиатуру


async def load_new_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        read = await sqlite_db.sql_read_users()
        for ret in read:
            if message.from_user.id == ret[0]:
                data['user_id'] = ret[0]
                data['first_name'] = ret[1]
                data['last_name'] = ret[2]
                data['job_title'] = ret[3]
                data['dlr_for'] = ret[4]
                data['question'] = "Новый ID - " + message.text
                data['question_status'] = "in process"
                data['Creation_time'] = datetime.now().date()
    await sqlite_db.sql_add_questions(state)
    await state.finish()
    await message.reply('Спасибо вам за обращение, скоро мы вернемся с информацией!')


"""***************************************************************************************************************"""


# Базовая команда старт
async def commands_start(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    # changed_id =''
    for ret in read:
        # if "_" in ret[1]:
        #     changed_id = ret[1].replace ('_',"#")
        # test_dict[ret[0]] = changed_id
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and str(values).upper() in id_saba:
            await bot.send_message(message.from_user.id, 'Проверка ID номеров пройдена успешно!')
            await bot.send_message(message.from_user.id,
                                   'Добро пожаловать в Академию👋! Я бот, который будет помогать вам получать '
                                   'интересующую вас информацию и всегда оставаться в курсе последних новостей '
                                   'Академии Тойота 📰. Я нахожусь на первоначальном этапе разработки и поддерживаюсь '
                                   'энтузиазмом сотрудников академии. Постепенно моя функциональность будет '
                                   'расти и я буду еще более полезен.',
                                   reply_markup=kb_client)
            break
        elif message.from_user.id == key and str(values).upper() not in id_saba:
            await bot.send_message(message.from_user.id,
                                   'Вы есть в базе, но видимо указан не корректный ID в учебном портале, '
                                   'обратитесь к администратору',
                                   reply_markup=kb_ask)
            await bot.send_message(message.from_user.id, f'Указанный вами САБА ID - {values}')
            break
    if message.from_user.id not in test_dict:
        await bot.send_message(message.from_user.id,
                               'Вам нужно пройти регистрацию, для этого нажмите соответсвующую кнопку',
                               reply_markup=registration_kb)
    # await bot.send_message(message.from_user.id, 'Вам нужно пройти регистрацию, для этого нажмите',
    # 'соответсвующую кнопку', reply_markup=registration_kb)        #Это заглушка для создания первого юзера в базе
    await message.delete()


# Отправка контактов
async def contacts(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and values in id_saba:
            await bot.send_message(message.from_user.id,
                                   '<b>Менеджер:</b>\n<i>Сергей Тишкарь</i>: 8-916-351-72-03\n\n<b>Не '
                                   'техническое обучение:</b>\n<i>Владимир Крамсин</i>: '
                                   '8-916-532-08-75\n\n<b>Техническое обучение:</b>\n<i>Сергей Латахин</i>: '
                                   '8-985-768-49-37\n\n<b>Обучение авто с пробегом:</b>\n<i>Александр '
                                   'Родионов</i>: 8-926-012-22-23', parse_mode='html')


# Отправка гайда
async def guide(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and values in id_saba:
            await message.answer_document(open('guide.pdf', 'rb'))


# Не позволяет вводить что угодно, только команды
async def empty(message: types.Message):
    await bot.send_message(message.from_user.id, 'Нет такой команды')
    await message.delete()


"""*********************************ОПИСАНИЕ ТРЕНИНГОВ****************************************************"""


async def menu_trainings(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and values in id_saba:
            await bot.send_message(message.from_user.id, 'Выберите направление:', reply_markup=trainings_kb)


async def tech_trainings(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and values in id_saba:
            await sqlite_db.sql_read_tech_trainings(message)
            await bot.send_message(message.from_user.id, 'Выберите направление:', reply_markup=trainings_kb)


async def non_tech_trainings(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and values in id_saba:
            await sqlite_db.sql_read_non_tech_trainings(message)
            await bot.send_message(message.from_user.id, 'Выберите направление:', reply_markup=trainings_kb)


async def ucar_trainings(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and values in id_saba:
            await sqlite_db.sql_read_ucar_trainings(message)
            await bot.send_message(message.from_user.id, 'Выберите направление:', reply_markup=trainings_kb)


async def training_description(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and values in id_saba:
            await message.answer_document(open('trainings_description.pdf', 'rb'))


async def back_to_main_menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=kb_client)


"""*********************************ОПИСАНИЕ ТРЕНИНГОВ****************************************************"""


async def training_plan(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and values in id_saba:
            await bot.send_message(message.from_user.id, 'Выберите направление:', reply_markup=schedule_kb)


async def tech_schedule(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and values in id_saba:
            await sqlite_db.sql_read_tech_schedule(message)
            await bot.send_message(message.from_user.id, 'Выберите направление:', reply_markup=schedule_kb)


async def non_tech_schedule(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and values in id_saba:
            await sqlite_db.sql_read_non_tech_schedule(message)
            await bot.send_message(message.from_user.id, 'Выберите направление:', reply_markup=schedule_kb)


async def ucar_schedule(message: types.Message):
    read = await sqlite_db.sql_read_users()
    test_dict = {}
    for ret in read:
        test_dict[ret[0]] = ret[1]
    for key, values in test_dict.items():
        if message.from_user.id == key and values in id_saba:
            await sqlite_db.sql_read_ucar_schedule(message)
            await bot.send_message(message.from_user.id, 'Выберите направление:', reply_markup=schedule_kb)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(client_start, commands=['Регистрация'], state=None)
    dp.register_message_handler(load_saba_id, state=FSMClient.saba_id)
    dp.register_message_handler(training_plan, lambda message: 'Расписание тренингов' in message.text)
    dp.register_message_handler(cm_question_start, lambda message: 'Задать вопрос Академии' in message.text)
    dp.register_message_handler(load_question, state=FSMQuestion.question)
    dp.register_message_handler(contacts, lambda message: 'Контакты' in message.text)
    dp.register_message_handler(menu_trainings, lambda message: 'Описание тренингов' in message.text)
    dp.register_message_handler(guide, lambda message: 'Памятка для участия в тренинге' in message.text)
    dp.register_message_handler(tech_trainings, lambda message: 'Технические тренинги' in message.text)
    dp.register_message_handler(non_tech_trainings, lambda message: 'Нетехнические тренинги' in message.text)
    dp.register_message_handler(ucar_trainings, lambda message: 'Тренинги авто с пробегом' in message.text)
    dp.register_message_handler(back_to_main_menu, lambda message: 'Назад' in message.text)
    dp.register_message_handler(training_description, lambda message: 'Скачать описание всех тренингов' in message.text)
    dp.register_message_handler(cm_training_request_start,
                                lambda message: 'Записаться на платный тренинг' in message.text)
    dp.register_message_handler(load_request, state=FSMTrainingRequest.request)
    dp.register_message_handler(cm_id_correction, lambda message: 'Отправить запрос в Академию' in message.text)
    dp.register_message_handler(load_new_id, state=FSMReset.new_id)
    dp.register_message_handler(tech_schedule, lambda message: 'Технические направление' in message.text)
    dp.register_message_handler(non_tech_schedule, lambda message: 'Нетехнические направление' in message.text)
    dp.register_message_handler(ucar_schedule, lambda message: 'Направление авто с пробегом' in message.text)
    dp.register_message_handler(empty)
