from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
storage = MemoryStorage()

bot = Bot(os.getenv('TOKEN_API'))
dp = Dispatcher(bot, storage=storage)