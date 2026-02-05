from aiogram import Bot, Dispatcher, F
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, InputMediaAudio,
                           InputMediaDocument, InputMediaPhoto,
                           InputMediaVideo, Message)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


LEXICON: dict[str, str] = {
    'audio': '🎶 Аудио',
    'text': '📃 Текст',
    'photo': '🖼 Фото',
    'video': '🎬 Видео',
    'document': '📑 Документ',
    'voice': '📢 Голосовое сообщение',
    'text_1': 'Это обыкновенное текстовое сообщение, его можно легко отредактировать другим текстовым сообщением, но нельзя отредактировать сообщением с медиа.',
    'text_2': 'Это тоже обыкновенное текстовое сообщение, которое можно заменить на другое текстовое сообщение через редактирование.',
    'photo_id1': 'AgACAgIAAxkBAAIC32l7A9vusc5DtP-ZfV9vcgeIe82MAAKRE2sbys_IS871vaNBRf9YAQADAgADcwADOAQ',
    'photo_id2': 'AgACAgIAAxkBAAIC2Wl7AzLAW28Qbopkk6W0XPWZ23HIAAJjE2sbys_IS-ErHehzU9zTAQADAgADcwADOAQ',
    'voice_id1': 'AwACAgIAAxkBAAIDEml-ZMwSPu1AOEoLHEUcDVxumUzGAAIOlgACIajwSxNLroJo-8KEOAQ',
    'voice_id2': 'AwACAgIAAxkBAAIDE2l-ZNVaZHikvrLVQioHdcKjZ0F2AAIPlgACIajwS8QreEJWviRcOAQ',
    'audio_id1': 'CQACAgIAAxkBAAIDD2l-ZHvk8zy6s1G79lyfM2_oJQ2uAAINlgACIajwS39T-FPdmzS1OAQ',
    'audio_id2': 'CQACAgIAAxkBAAIDFWl-ZRV-BCwWoG_q0qsoFy0H-FC5AAIQlgACIajwSzYlJfYSqFBZOAQ',
    'document_id1': 'BQACAgIAAxkBAAIDFml-ZTXUxVRiGb9Q48F7NMfep3lVAAIRlgACIajwS_79IetT0mG1OAQ',
    'document_id2': 'BQACAgIAAxkBAAIDF2l-ZVd2muqn00njaFH_Do8o9RiRAAISlgACIajwSz6EkqHFa4d-OAQ',
    'video_id1': 'BAACAgIAAxkBAAIDGGl-ZWqfJxlyjAuKlR4Tm_b8ULYhAAITlgACIajwS-TXWRBwkEVHOAQ',
    'video_id2': 'BAACAgIAAxkBAAIDA2l-XVI8qLs1RcSYKQV2qei-B7PYAAKtlQACIajwSwzj1dM3m8bsOAQ'
}


# Функция для генерации клавиатур с инлайн-кнопками
def get_markup(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    markup = get_markup(2, 'photo')
    await message.answer_document(
        document=LEXICON['video_id1'],
        caption='Это видео 1',
        reply_markup=markup
    )


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
@dp.callback_query(F.data.in_(
    ['text', 'audio', 'video', 'document', 'photo', 'voice']
))
async def process_button_press(callback: CallbackQuery, bot: Bot):
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=LEXICON['photo_id2'],
                caption='Это фото 2'
            ),
            reply_markup=get_markup(2, 'video')
        )
    except TelegramBadRequest:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaVideo(
                media=LEXICON['video_id1'],
                caption='Это видео 1'
            ),
            reply_markup=get_markup(2, 'photo')
        )


# Этот хэндлер будет срабатывать на все остальные сообщения
@dp.message()
async def send_echo(message: Message):
    await message.answer(text='Не понимаю')


if __name__ == '__main__':
    dp.run_polling(bot)