# Main File :

# Imports :
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
import re
from USER_DATA import USER_STATE
import DATA
# Telegram Token and URL for webinar :
API_TOKEN: str = "YOUR_API_TOKEN"
URL: str = "YOUR_WEBINAR_URL"

# bot and dispatcher :
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Functions :

# Start command :
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    if USER_STATE['is_authorized'] is None:
        # First message
        await message.answer("Привет\nЯ бот, если ты хочешь записаться на вебинар по красоте, напиши мне ФИО")
    if USER_STATE['is_authorized']:
        # If user is troll :)
        await message.answer(f"Вы уже записаны на вебинар, ссылка на него - {URL}.")
    if not USER_STATE['is_authorized']:
        # If user is used cancel command
        await message.answer("Вы хотите записаться на вебинар.\nТогда напишите ФИО")

# Help command :
@dp.message(Command(commands=["help"]))
async def help_command(message: Message):
    await message.answer("Команды: \n\n/cancel - вы будете удалены из списка участвующих на вебинаре")


# Function which work after username and user surname and write for user "You booked the webinar.” :
@dp.message(lambda message: re.match(r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+$', message.text))
async def setFIO(message: Message):
    # name
    name = message.text
    await message.answer(f'Поздравляю, {name}! Вы записались на вебинар, вот ваша ссылка, {URL}, заходите на нее в четверг в 18:00, также я напишу вам за 15 минут до вебинара')

    # Message for <name> about user which booked on webinar
    await bot.send_message(chat_id=DATA.USERNAME_FOR_MESSAGE_ABOUT_AUTHORIZATION_ON_WEBINAR, text=f"{name} - присоединился к списку людей на вебинаре)")

    # User authorized state
    USER_STATE['is_authorized'] = True

# Cancel command :
@dp.message(Command(commands=["cancel"]))
async def cancel(message: Message):
    await message.answer("Жаль :(.\nТеперь вы убраны из списка людей на вебинаре")
    await bot.send_message(chat_id = DATA.USERNAME_FOR_MESSAGE_ABOUT_AUTHORIZATION_ON_WEBINAR, text=f"{message.from_user.full_name} убран из списка людей на вебинаре(.")
    USER_STATE['is_authorized'] = False

# Bot start function :
if __name__ == '__main__':
    dp.run_polling(bot)



