#6918204649:AAGP-uIfNoziXXN-ueYXHD7kMJ3NJ566BUk - api key

import spacy
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from unittest.mock import Mock

TOKEN: Final = '6918204649:AAGP-uIfNoziXXN-ueYXHD7kMJ3NJ566BUk'
BOT_USERNAME: Final = '@docquest_bot'




#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to DocQuest! Your personal reviewer assistant. Send me a document and I will help you with it.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Please type something so I can help you.')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('this is a custom command')



#Responses

def handle_response(text: str) -> str:
    text_input: str = text.lower()

    if 'hello' in text_input:
        return 'Hello! How can I help you today?'
    #add nlp so that it can understand the text and give a response
    elif text_input:
        text_to_summarize = text_input

        summary = text_summarization(text_to_summarize, 0.3)
        return f'Summarization of the text:\n{summary}'
    

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    text: str = update.message.text
    response: str = handle_response(text)
    print("Bot:", response)
    await update.message.reply_text(response)

#summarization of the text
def text_summarization(text, percentage):

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text) 

    tokens=[token.text for token in doc]
    # print("unused tokens:", tokens)
    frequency = dict()

    #cleaning text
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in frequency.keys():
                    frequency[word.text] = 1
                else:
                    frequency[word.text] += 1

    #print("Freq:", frequency)
    #setting max frequency of word
    max_frequency = max(frequency.values())

    #normalization
    for word in frequency.keys():
        frequency[word] = frequency[word]/max_frequency

    #sentence is weighed based on how often it contains the token
    sent_tokens = [sent for sent in doc.sents]
    #print("SentTokens:", sent_tokens)

    sentscore = dict()
    for sent in sent_tokens:
        for word in sent:
            if word.text.lower() in frequency.keys():
                if sent not in sentscore.keys():
                    sentscore[sent] = frequency[word.text.lower()]
                else:
                    sentscore[sent] += frequency[word.text.lower()]

    len_tokens = int(len(sent_tokens)*percentage)

    #Summary for the sentences with maximum score. 
    #Here, each sentence in the list is of spacy.span type
    summary = nlargest(n = len_tokens, iterable = sentscore, key = sentscore.get)

    #preparation for final summary
    final_summary = [word.text for word in summary] 
    
    #string convert
    summary = ' '.join(final_summary)

    return summary




async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')



if __name__ == '__main__':

    print('Bot starting..')
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #error
    app.add_error_handler(error)

    print('polling....')
    app.run_polling(poll_interval=3)



    #all that is left is to add the nlp and the pdf reader
    #publish the bot and test it