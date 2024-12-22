from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
import speech_recognition as sr
import subprocess
import asyncio
import os


TOKEN = '8004157085:AAEp1hp4klubTIcvWwEcBB1jSqLb63qAzvo'

bot = Bot(TOKEN)
dp = Dispatcher()
r = sr.Recognizer()

#приветствие
@dp.message(CommandStart())

async def start_command(message: types.Message):
    await message.answer('Здравствуйте! Отправьте аудио для перевода в текст.')


@dp.message(F.audio)  #бот работает только с аудио
async def convert_audio_to_text(message: types.Message):
    split_tup = os.path.splitext(message.audio.file_name)     #сохранение имени и расширения полученного файла
    file_name = f'{split_tup[0]}_{message.from_user.full_name}{split_tup[1]}'  #сохранение имени файла в формате: исходноеназвание_имяпользователя_расширение
    await bot.download(message.audio.file_id, file_name)  #скачивание файла



    #преобразование аудио в текст

    with sr.AudioFile(file_name) as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language='ru')
    await message.answer(text)

    os.remove(file_name)




#удаление предыдущих действий
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
