from selenium.common import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import time
import random
import asyncio
import multiprocessing
from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from chromedriver.scraper_gumtree import Ad, cycle_one, print_ads, proxy_setup





# telegram part


storage = MemoryStorage()
bot = Bot(token='6237128583:AAFtVuZobkQNwyHIRgzshAfoihpWRyJ-4VI')
dp = Dispatcher(bot, storage=storage)
vip = [371348044, 5613237024, 770310010]
active_chat_ids = []
chats_ids_dict = {key: 0 for key in vip}


async def set_commands():
    commands = [
        types.BotCommand(command="/help", description="Все доступные команды"),
        types.BotCommand(command="/start", description="Запускает бота"),
        types.BotCommand(command="/start_time", description="Запускает бота на определенное время"),
        types.BotCommand(command="/payment", description="Оплата и контакты"),
        types.BotCommand(command="/exit", description="Выключить бота")
    ]
    await bot.set_my_commands(commands)


async def send_telegram_message(chat_id, text):
    await bot.send_message(chat_id, text)


HELP_COMMAND = """
/help - список команд
/start - запустить бота (автоматом стоит на час)
/start_time - запустить бота на время
/payment - оплатить подписку за бота 
/exit - выключить бота 
"""

payment_reminder = "К сожалению вы не оплатили бота. Если вы хотите его оплатить, или уже оплатили но видите это сообщение напишите @sky7walker"


class TimerSetupStates(StatesGroup):
    WAITING_FOR_TIMER = State()

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)
    print("HELP")


@dp.message_handler(commands=['payment'])
async def payment_command(message: types.Message):
    await message.reply(text="🤑 По вопросам оплаты пишите @sky7walker. 🤕 По проблемам с ботом пишите @grerik")


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in vip:
        await message.reply(payment_reminder)
    else:
        chats_ids_dict[message.chat.id] = 1 * 60 * 60 + time.time()
        print(chats_ids_dict[message.chat.id], message.chat.id)
        await message.reply(text="Вы запустили бота на час. Удачной работы 😤")

@dp.message_handler(commands=['start_time'])
async def start_timer_command(message: types.Message, state: FSMContext):
    # Set the state to WAITING_FOR_TIMER
    await TimerSetupStates.WAITING_FOR_TIMER.set()
    chat_id = message.chat.id
    if chat_id not in vip:
        await message.reply(payment_reminder)
        await state.finish()
    else:
        await message.reply(text="Введите значение таймера (в часах):")

@dp.message_handler(state=TimerSetupStates.WAITING_FOR_TIMER)
async def process_timer_value(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if chat_id not in vip:
        await message.reply(payment_reminder)
        await state.finish()
    else:
        try:
            timer_value = int(message.text)
            chats_ids_dict[message.chat.id] = timer_value * 60 * 60 + time.time()
            await message.reply(text=f"Бот установлен на {timer_value} часов.Удачной работы")
        except ValueError:
            await message.reply(text="Некорректное значение таймера. Введите число (в часах).")

        await state.finish()

@dp.message_handler(lambda message: not message.is_command() and not message.text.isdigit())
async def process_other_messages(message: types.Message):
    # Handle other messages that are not commands and not a number (when the user is not setting up the timer)
    await message.reply(text="Я не понимаю вас 😢.")


async def check_for_new_users(chats_ids_dict):
    for key, val in chats_ids_dict.items():
        if val > time.time():
            if key not in active_chat_ids:
                active_chat_ids.append(key)
        else:
            if key in active_chat_ids:
                active_chat_ids.pop(key)
    if len(active_chat_ids) == 0:
        return False
    else:
        return True

async def start_bot():
    await set_commands()
    await dp.skip_updates()
    await dp.start_polling()

async def main_work(queue):
    chrome_options = Options()
    url = "https://www.gumtree.com.au/s-r500"
    driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=proxy_setup(1))
    ads_finished = {}
    print(10)
    used_ads = []
    while True:
        if await check_for_new_users(chats_ids_dict):
            print("Passed")
            driver.get(url)
            ad_collection_section = driver.find_element(By.CLASS_NAME, "search-results-page__user-ad-collection")
            ad_elements = ad_collection_section.find_elements(By.CLASS_NAME, "user-ad-row-new-design")
            ads = []
            cycle_one(ads, driver, ad_elements)
            driver.refresh()
            used_chats = active_chat_ids[:]
            for ad in ads:
                if ad.id not in ads_finished.keys():
                    if ad.id not in used_ads:
                        ads_finished[ad.id] = ad
                        message = "Title: {}\nPrice: {}\nLocation: {}\nP_time: {}\nLink: {}\nId: {}\nRegistred_date: {}".format(
                            ad.item_name, ad.price, ad.location, ad.publication_time, ad.ad_link, ad.id, ad.date_registered)
                        if len(used_chats) > 0:
                            random_index = random.randint(0, len(used_chats) - 1)
                            selected_chat_id = used_chats.pop(random_index)
                        else:
                            used_chats = active_chat_ids[:]
                            random_index = random.randint(0, len(used_chats) - 1)
                            selected_chat_id = used_chats.pop(random_index)
                        await send_telegram_message(selected_chat_id, message)
                        ads_finished[ad.id].print_info()
                        used_ads.append(ad.id)



def start_bot_sync(queue):
    asyncio.run(start_bot(queue))

def main_work_sync(queue):
    asyncio.run(main_work(queue))

if __name__ == '__main__':
    queue = multiprocessing.Queue()

    start_bot_process = multiprocessing.Process(target=start_bot_sync, args=(queue,))
    main_work_process = multiprocessing.Process(target=main_work_sync, args=(queue,))

    start_bot_process.start()
    main_work_process.start()

    start_bot_process.join()
    main_work_process.join()


