#\==================================================================/#
#/========================/ installed libs \========================\#

from typing        import List
from asyncio       import run as async_run
from traceback     import format_exc
from telebot       import TeleBot
from telebot.types import ReplyKeyboardRemove as rmvKey

#--------------------------\ project files /-------------------------#

from utility import delFile, getData, makeKey, saveText, showFile
from debug   import saveLogs
from groups  import LINK_BASE
from path    import PEOPLE_FILE

#\==================================================================/#


#\==================================================================/#
def show_people_key(bot : TeleBot, _id : int | str) -> None:

    keyboard = makeKey(['Сканировать', 'Список', 'Очистить', 'Назад'])

    txt = 'Здесь можно редактировать списки аккаунтов.'

    bot.send_message(_id, txt, reply_markup=keyboard)
#\==================================================================/#

#\==================================================================/#
def show_people(bot : TeleBot, _id : int | str) -> None:
    showFile(bot, _id, PEOPLE_FILE, 'Аккаунты', 'Нет добавленных аккаунтов.')
#\==================================================================/#

#\==================================================================/#
def del_people(bot : TeleBot, _id : int | str) -> None:
    delFile(bot, _id, PEOPLE_FILE, 'Данные удалены.', 'Ошибка удаления.')
#\==================================================================/#

#\==================================================================/#
#/========================/ installed libs \========================\#

from telethon                       import TelegramClient
from telethon.tl.types              import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetParticipantsRequest

#\==================================================================/#
def add_people(bot     : TeleBot, 
               _id     : int | str,
               _lks    : str,
               _nm     : str,
               _id_api : int,
               _hsh    : str,
               _fl     : str) -> None:

    async def get_users(_lk     : str, 
                        _nm     : str, 
                        _id_api : int, 
                        _hsh    : str,
                        _fl     : str) -> None:
        try:
            _client = TelegramClient(_nm, _id_api, _hsh)

            await _client.start ()
            await _client.get_me()

            _ch = await _client.get_entity(_lk)

            items = []
            _offs = 0
            n = 0

            while n < 10:
                _srch = ChannelParticipantsSearch('')

                req = GetParticipantsRequest(_ch, _srch, _offs, 100, hash=0)
                
                _its = await _client(req)
                
                if not _its.users:
                    break
                
                items.extend(_its.users)

                _offs += len(_its.users)
                n += 1

            for it in items:
                saveText(f'{it.id} {it.username} {it.phone}\n', _fl)

            await _client.disconnect()
        
        except:
            saveLogs(f'[get_users]---->{format_exc()}')

    if not len(_lks):
        bot.send_message(_id, 'Добавьте группы для сбора аккаунтов.')
        return

    for _lk in _lks:
        if LINK_BASE in _lk:
            _txt = f'Начинаю сканировать: {_lk}'
            bot.send_message(_id, _txt, reply_markup=rmvKey())
            async_run(get_users(_lk, _nm, _id_api, _hsh, _fl))
    
    showFile(bot, _id, _fl, 'Аккаунты', 'Ошибка.')
#\==================================================================/#

#\==================================================================/#
def get_people() -> List[str | None]:
    return getData(PEOPLE_FILE, '\n')
#\==================================================================/#
