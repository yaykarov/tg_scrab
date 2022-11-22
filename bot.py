#/==================================================================\#
#                                                                    #
#\==================================================================/#

#\==================================================================/#
#/========================/ installed libs \========================\#

from typing        import Dict
from telebot       import TeleBot
from telebot.types import Message
from traceback     import format_exc

#--------------------------\ project files /-------------------------#

from utility import makeKey
from debug   import saveLogs
from path    import PEOPLE_FILE

#\==================================================================/#

#\==================================================================/#
TOKEN = '5361529726:AAHkDG9SoOJUA_1F9rWnIjTXkxW_kpq4vQg'

spamer = {
    '_nm'     : '',
    '_id_api' : 13568188,
    '_hsh'    : '3845a0ff5cf2bd00bf6f1006f5c2666e',
    '_fl'     : PEOPLE_FILE
}
"""
Reg at https://my.telegram.org/apps
"""
#\==================================================================/#

#\==================================================================/#
bot = TeleBot(TOKEN)
#\==================================================================/#

#\==================================================================/#
@bot.message_handler(commands=['start', 'help'])
def start(msg : Message) -> None:
    keyboard = makeKey(['Группы', 'Контакты', 'Рассылка'])

    txt = 'Выберите канал для парсинга'
    bot.send_message(msg.chat.id, txt, reply_markup=keyboard)
#\==================================================================/#

#\==================================================================/#
#--------------------------\ project files /-------------------------#

from groups  import show_group_key , \
                    add_group      , \
                    show_groups    , \
                    del_groups     , \
                    get_groups
from people  import del_people     , \
                    show_people_key, \
                    show_people    , \
                    add_people
from mailing import mail_msg

#\==================================================================/#

#\==================================================================/#
@bot.message_handler(content_types=['text'])
def parsing(msg : Message) -> None:
    txt : str = msg.text
    _id : int = msg.chat.id

    ACTIONS : Dict[str, function] = {
        'Группы'   : show_group_key,
        'Показать' :    show_groups,
        'Удалить'  :     del_groups,
        'Добавить' :      add_group,

        'Контакты' : show_people_key,
        'Список'   :     show_people,
        'Очистить' :      del_people
    }

    try:
        if txt in ACTIONS:
            ACTIONS[txt](bot, _id)

        elif txt == 'Сканировать':
            add_people(bot, _id, get_groups(), **spamer)
            show_people_key(bot, _id)

        elif txt == 'Назад':
            start(msg)

        elif txt == 'Рассылка':
            mail_msg(bot, _id, spamer)

    except:
        saveLogs(f'[parsing]---->{format_exc()}')
#\==================================================================/#

#\==================================================================/#
if __name__ == "__main__":
    try: 
        bot.polling(none_stop=True)
    except:
        saveLogs(f"Program error!\n\n{format_exc()}")
#\==================================================================/#
