#\==================================================================/#
#/========================/ installed libs \========================\#

from typing        import List
from telebot       import TeleBot
from telebot.types import Message

#--------------------------\ project files /-------------------------#

from path    import GROUPS_FILE
from utility import delFile, getData, makeKey, saveText, showFile

#\==================================================================/#
LINK_BASE = 'https://t.me/'
#\==================================================================/#

#\==================================================================/#
def show_group_key(bot : TeleBot, _id : int | str) -> None:
    keyboard = makeKey(['Добавить', 'Удалить', 'Показать', 'Назад'])

    txt = 'Здесь можно редактировать группы.'

    bot.send_message(_id, txt, reply_markup=keyboard)
#\==================================================================/#

#\==================================================================/#
def add_group(bot : TeleBot, _id) -> None:

    def __add_group(msg : Message, 
                    bot : TeleBot, 
                    _id : int | str) -> None:
        name : str = msg.text
        
        if LINK_BASE in name:
            saveText(f'{name}\n', GROUPS_FILE)
            bot.send_message(_id, f'Добавил: {name}')
        else:
            bot.send_message(_id, 
                f'Ошибка. Ссылка должна быть вида: {LINK_BASE}')
    
    msg = bot.send_message(_id, 'Отправьте ссылку на группу.')
    bot.register_next_step_handler(msg, __add_group, bot, _id)
#\==================================================================/#

#\==================================================================/#
def show_groups(bot : TeleBot, _id : int | str) -> None:
    showFile(bot, _id, GROUPS_FILE, 'Группы', 'Нет добавленных групп.')
#\==================================================================/#

#\==================================================================/#
def del_groups(bot : TeleBot, _id : int | str) -> None:
    delFile(bot, _id, GROUPS_FILE, 'Данные удалены.', 'Ошибка удаления.')
#\==================================================================/#

#\==================================================================/#
def get_groups() -> List[str | None]:
    return getData(GROUPS_FILE, '\n')
#\==================================================================/#
