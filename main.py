#6918204649:AAGP-uIfNoziXXN-ueYXHD7kMJ3NJ566BUk - api key

from typing import Final
from chatbot.chatbot import ChatBot

TOKEN: Final = '6918204649:AAGP-uIfNoziXXN-ueYXHD7kMJ3NJ566BUk'
BOT_USERNAME: Final = '@docquest_bot'



if __name__ == '__main__':

    docquest = ChatBot(TOKEN)

    print('polling....')
    docquest.app.run_polling(poll_interval=3)



    #all that is left is to add the nlp and the pdf reader
    #publish the bot and test it