#\==================================================================/#
#/========================/ installed libs \========================\#


from io            import open                as file_open
from os            import remove              as rmv
from os.path       import exists              as isExist
from telebot.types import ReplyKeyboardMarkup as crMrkup
from telebot.types import KeyboardButton      as crBtn
from telebot       import TeleBot
from typing        import List

#\==================================================================/#

#\==================================================================/#
def saveText(txt : str, _fl : str, _m = 'a', _c = 'utf-8') -> int:
    return open(_fl, _m, encoding = _c).write(txt)
#\==================================================================/#


#\==================================================================/#
def makeKey(btns : List):
    keyboard = crMrkup(resize_keyboard=True)
    
    keyboard.add(*[crBtn(btn) for btn in btns])
    
    return keyboard
#\==================================================================/#

#\==================================================================/#
def rmvFile(pth : str) -> bool:
    if isExist(pth):
        rmv(pth)
        return True
    return False
#\==================================================================/#

#\==================================================================/#
#\==================================================================/#
def showFile(bot : TeleBot, 
             _id : int | str, 
             _fl : str, 
             cap : str, 
             txt : str) -> None:
    if isExist(_fl):
        bot.send_document(_id, open(_fl, 'rb'), caption=cap)
    else:
        bot.send_message(_id, txt)
#\==================================================================/#

#\==================================================================/#
def delFile(bot   : TeleBot, 
            _id   : int | str,
            _fl   : str, 
            txt_t : str,
            txt_f : str) -> None:
    if rmvFile(_fl):
        bot.send_message(_id, txt_t)
    else:
        bot.send_message(_id, txt_f)
#\==================================================================/#
    
#\==================================================================/#
def openfileforRead(file = None, text = '') -> str:
    return text.join([i for i in file_open(file, encoding='utf-8')])
#\==================================================================/#

#\==================================================================/#
def getData(_fl : str, splt : str) -> List[str | None]:
    if isExist(_fl):
        return list(openfileforRead(_fl).split(splt))
    else:
        return []
#\=======================s===========================================/#
