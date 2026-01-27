import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

BOT_TOKEN = '7735138529:AAEsyKvRpHUIo_1PaXOGUpLGhw5eU0YTOOE'

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(text='Hello')


@dp.message()
async def receive_file_id(message: Message):
    type_id: str = message.content_type
    my_file_id = message.content_type.lower().file_id
    print(f'This - {type_id.lower()}')
    # if message.photo:
    #     logger.info((f'photo_id - {message.photo[0].file_id}'))
    #     await message.answer(text=message.photo[0].file_id)
    # elif message.audio:
    #     logger.info((f'audio_id - {message.audio.file_id}'))
    #     await message.answer(text=message.audio.file_id)
    # elif message.document:
    #     logger.info((f'document_id - {message.document.file_id}'))
    #     await message.answer(text=message.document.file_id)
    # elif message.video:
    #     logger.info((f'video_id - {message.video.file_id}'))
    #     await message.answer(text=message.video.file_id)
    # elif message.voice:
    #     logger.info((f'voice_id - {message.voice.file_id}'))
    #     await message.answer(text=message.voice.file_id)

if __name__ == '__main__':
    dp.run_polling(bot)