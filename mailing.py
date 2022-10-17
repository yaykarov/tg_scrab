#\==================================================================/#
#/========================/ installed libs \========================\#

from time          import sleep
from asyncio       import run as async_run
from traceback     import format_exc
from typing        import Dict, List
from telebot       import TeleBot
from telebot.types import Message
from telethon      import TelegramClient

#--------------------------\ project files /-------------------------#

from debug  import saveLogs
from people import get_people

#\==================================================================/#

#\==================================================================/#
DELAY_S = 1
#\==================================================================/#


#\==================================================================/#
def mail_msg(bot : TeleBot, _id : int | str, spm : Dict) -> None:

    def __mail_msg(msg  : Message, spm  : Dict) -> None:

        async def __mail(user    : str, 
                         txt     : str, 
                         _nm     : str, 
                         _id_api : int,
                         _hsh    : str,
                         _fl     : str) -> None:
            try:
                _client = TelegramClient(_nm, _id_api, _hsh)
                
                await _client.start ()
                await _client.get_me()

                await _client.send_message(user, txt)


                saveLogs(f'[SEND][TRUE]-->{user}')
            except:
                saveLogs(f'[SEND][FALSE]-->{format_exc()}')
            
            await _client.disconnect()
            
            sleep(DELAY_S)
                

        txt : str = msg.text

        accs : List[str | None] = get_people()

        if not len(accs):
            bot.send_message(_id, 'Добавьте аккаунты для рассылки.')
            return

        for acc in accs:
            acc = list(acc.split(' '))
            if acc[0]:
                if acc[1] != 'None':
                    async_run(__mail(acc[1], txt, **spm))
                elif acc[2] != 'None':
                    async_run(__mail(acc[2], txt, **spm))
            
                

    txt = 'Введите сообщение для рассылки.'
    msg = bot.send_message(_id, txt)
    bot.register_next_step_handler(msg, __mail_msg, spm)
#\==================================================================/#
