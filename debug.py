from datetime import datetime
from utility  import saveText
from path     import LOG_FILE

def saveLogs(text, file = LOG_FILE) -> int:
    return saveText(f'\nDate: {datetime.now()}\n\n{text}', file)

