import logging
import json

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

BOT_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dict_id = {}


@dp.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(text='Hello')


@dp.message(F.photo)
async def receive_file_id_photo(message: Message):
    file_id = message.photo[0].file_id
    if 'photo_id1' in dict_id:
        dict_id['photo_id2'] = file_id
    else:
        dict_id['photo_id1'] = file_id
    print(dict_id)


@dp.message()
async def receive_file_id(message: Message):
    type_id: str = message.content_type
    dict_mes = json.loads(message.model_dump_json(indent=4, exclude_none=True))
    file_id = dict_mes.get(type_id).get("file_id")
    if f'{type_id.lower()}_id1' in dict_id:
        dict_id[f'{type_id.lower()}_id2'] = file_id
    else:
        dict_id[f'{type_id.lower()}_id1'] = file_id
    print(dict_id)


if __name__ == '__main__':
    dp.run_polling(bot)