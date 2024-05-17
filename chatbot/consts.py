from telegram.ext import ConversationHandler

UPLOAD_PDF, UPLOAD_TXT, SEND_TXT = map(int, range(6, 9))

START_OVER, DONE, SELECTING_ACTION, DOWNLOAD_FILE, GENERATE_QUESTS, CHECKING_ANSWER = map(int, range(6))

END = ConversationHandler.END


SAMPLE_QS = {
    1: {
        "question": "What is the capital of France?",
        "answer": "Paris",
        "choices": {
            1: "Berlin",
            2: "Madrid",
            3: "Paris",
            4: "Rome"
        }
    },
    2: {
        "question": "What is 2 + 2?",
        "answer": "4",
        "choices": {
            1: "3",
            2: "4",
            3: "5",
            4: "6"
        }
    }
}
