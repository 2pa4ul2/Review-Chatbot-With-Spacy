
import os, logging
import telegram
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    ConversationHandler,
    CallbackQueryHandler, 
    CallbackContext,  
    ContextTypes,
    filters
)


from workers import PDFtoQuestions
from .messages import *
from .consts import *



class ChatBot:
    def __init__(self, TOKEN: str) -> None:
        print('Bot starting..')
        self.app = Application.builder().token(TOKEN).build()

        message_handlers = [
            MessageHandler(filters.TEXT, self.handle_message),
            MessageHandler(filters.Document.PDF, callback=self.handle_file),
            MessageHandler(~filters.Document.MimeType('application/pdf'), self.handle_other_file)
        ]

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start_command)],
            states={
                SELECTING_ACTION: message_handlers,
                DOWNLOAD_FILE: [CallbackQueryHandler(self.download_file)],
                GENERATE_QUESTS: [CallbackQueryHandler(self.generate_questions)],
                CHECKING_ANSWER: [CallbackQueryHandler(self.handle_answer)],
                DONE: [CallbackQueryHandler(self.quests_done)],
            },
            fallbacks=[CommandHandler('custom', self.custom_command)]
        )

        self.app.add_handler(conv_handler)
        self.app.add_handler(CommandHandler('help', self.help_command))

        self.app.add_error_handler(self.error_handler)


    async def error_handler(self, update: Update, context: CallbackContext):
        """Log the error and send a message to the user or developer."""
        # Configure logging
        logging.basicConfig(
            format='%(name)s | %(levelname)s | %(message)s',
            level=logging.INFO
        )

        logger = logging.getLogger(__name__)
        logger.error(msg="Exception while handling an update:", exc_info=context.error)
        
        # Notify the user that an error occurred
        if update.message:
            await update.message.reply_text("Error occurred in update: ", update)
        elif update.callback_query:
            await update.callback_query.message.reply_text("Error occurred in callback query: ", context.error)


    def handle_response(self, text: str) -> str:
        text_input: str = text.lower()

        if 'hello' in text_input:
            return 'Hello! How can I help you today?'
        #add nlp so that it can understand the text and give a response
        elif 'pdf' in text_input:
            return INSTRUCTION_TEXT
        elif text_input:
            text_to_summarize = text_input

            summary = "SUMMARY FUNC" #self.text_summarization(text_to_summarize, 0.3)
            return f'Summarization of the text:\n{summary}'
    
        return "I'm not sure how to respond to that."
        
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: 
        text: str = update.message.text
        response: str = self.handle_response(text)
        print("Bot:", response)
        await update.message.reply_text(response)

        if text == 'pdf':
            return SELECTING_ACTION
        
        return 16 # GENERATE_QUESTS

    
    async def handle_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: 
        print("handle PDF file")
        buttons = [[InlineKeyboardButton(text="Generate Questions 📋", callback_data="generate")], [
                     InlineKeyboardButton(text="Get Images 📷", callback_data="idk")]]
        keyboard = InlineKeyboardMarkup(buttons)
        await update.message.reply_document(document=update.message.document, caption="Click On 👇 to Generate Questions", reply_markup=keyboard)

        return DOWNLOAD_FILE
    

    async def handle_other_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            print("other file")
            filename = update.message.document.file_name.split(".")
            extension = filename[len(filename)-1]
            await update.message.reply_text(text=WRONG_FILE.format(extension), parse_mode=constants.ParseMode.HTML)
        except AttributeError as e:
            await update.message.reply_text("Sorry Bot can't Read this file\n\nTry Sending the file with ```.pdf``` Extension",parse_mode=constants.ParseMode.MARKDOWN_V2)

        print("TRY AGAIN OTHER FILE")
        return END

    async def custom_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text('this is a custom command (fallbacks)')
        return END

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text(INSTRUCTION_TEXT, parse_mode=constants.ParseMode.HTML)
        return END


    async def start_command(self, update: Update, context: CallbackContext) -> int:
        print("start")
        await context.bot.set_my_commands([BotCommand("start", "Restart the bot"), BotCommand("help", "Help description")])

        if context.user_data.get(START_OVER):
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(text=INSTRUCTION_TEXT)
        else:
            await update.message.reply_text(text=START_TEXT)
            await update.message.reply_text(text=INSTRUCTION_TEXT, parse_mode=constants.ParseMode.HTML)

        context.user_data[START_OVER] = False
        context.user_data['curr_index'] = 1
        return SELECTING_ACTION
    

    async def download_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        print("download file")
        filename = r"chatbot\uploads\file"+str(update.effective_chat.id)+".pdf"
        file_id = update.callback_query.message.document.file_id
        docs = await context.bot.get_file(file_id=file_id)
        await docs.download_to_drive(custom_path=filename)
        await context.bot.answer_callback_query(update.callback_query.id, text="Downloading....")

        # self.question_data = SAMPLE_QS
        # print("self.question_data: ", self.question_data)

        buttons = [[InlineKeyboardButton(text="Start Quest!", callback_data="generate")],
                   [InlineKeyboardButton(text="Cancel Quest", callback_data="idk")]]
        keyboard = InlineKeyboardMarkup(buttons)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=QUEST_START, reply_markup=keyboard)
        
        return GENERATE_QUESTS
    
    async def generate_questions(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:         
        print("update.callback_query.data:", update.callback_query.data)
        if update.callback_query.data == "generate":

            # pdf = PDFtoQuestions(filename)
            # quests = pdf.extract_questions()

            # for index, question_data in quests.items():
            #     keyboard = []
            #     reply_markup = None
            #     qa_text = f"QUESTION #{index}\n{question_data['question']}\nAnswer: {question_data['answer']}\n"
                
            #     if 'choices' in question_data:
            #         for choice_number, choice_text in question_data['choices'].items():
            #             keyboard.append([InlineKeyboardButton(text=choice_text, callback_data=choice_number)])
            #         reply_markup = InlineKeyboardMarkup(keyboard)

            #     await context.bot.send_message(chat_id=update.effective_chat.id, text=QUESTION_TEXT.format(qa_text), parse_mode=constants.ParseMode.HTML, reply_markup=reply_markup)
            
            if context.user_data['curr_index'] <= len(SAMPLE_QS):
                i = context.user_data['curr_index']
                buttons = []
                question_data = SAMPLE_QS[i]

                print("question_data: ", question_data['question'])
                print("ans: ", question_data['answer'])
                print("ch: ", question_data['choices'])
                print("q_idx: ", i)

                qa_text = f"QUESTION #{i}\n{question_data['question']}\nAnswer: {question_data['answer']}\n"
                context.user_data['curr_answer'] = question_data['answer']

                buttons = [
                    [
                        InlineKeyboardButton(text=choice_text, callback_data=str(choice_text))
                        for choice_text in list(question_data['choices'].values())[i:i + 2]
                    ]
                    for i in range(0, len(question_data['choices']), 2)
                ]
                keyboard = InlineKeyboardMarkup(buttons)

                await context.bot.send_message(chat_id=update.effective_chat.id, text=QUESTION_TEXT.format(qa_text), parse_mode=constants.ParseMode.HTML, reply_markup=keyboard)

                return CHECKING_ANSWER
            return DONE
        elif update.callback_query.data == "idk":
            await context.bot.send_message(chat_id=update.effective_chat.id, text="IDK WHY")
            
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="NONENONENONE")

        return END



    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        selected_choice = query.data
        correct_answer = context.user_data['curr_answer']
        print("selected_choice:", selected_choice)
        print("['curr_answer']:", correct_answer)

        buttons = [[InlineKeyboardButton(text="Next Question?", callback_data="generate"),
                    InlineKeyboardButton(text="Cancel Quest", callback_data="idk")]]
        keyboard = InlineKeyboardMarkup(buttons)

        if str(selected_choice) == str(correct_answer):
            await context.bot.send_message(chat_id=update.effective_chat.id, text=ANS_CORRECT_TEXT.format(correct_answer), parse_mode=constants.ParseMode.HTML, reply_markup=keyboard)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=ANS_WRONG_TEXT.format(correct_answer), parse_mode=constants.ParseMode.HTML, reply_markup=keyboard)

        context.user_data['curr_index'] += 1
        print("['curr_index']:", context.user_data['curr_index'])
        return GENERATE_QUESTS
    

    async def quests_done(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        buttons = [[InlineKeyboardButton(text="Start Again", callback_data="start")],
                   [InlineKeyboardButton(text="Cancel Quest", callback_data="idk")]]
        keyboard = InlineKeyboardMarkup(buttons)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=QUEST_END, reply_markup=keyboard)

        return

        
                