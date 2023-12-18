import os
import g4f
import telebot

from dotenv import load_dotenv

load_dotenv('.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT = telebot.TeleBot(BOT_TOKEN)

HISTORY = []

MODELS = [
    "gpt-4",
    "gpt-3.5-turbo",
]

def generate_answer(query: str, model: str) -> str:
    '''
    Generates an answer for the given query.
    '''
    print(f'Getting Response for `{query}` using {model}')
    
    prepared_history = HISTORY.copy()
    prepared_history.append({
        'role': 'user',
        'content': query
    })

    # Execute with a specific provider
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4 if model.lower() == 'gpt-4' else 'gpt-3.5-turbo',
        provider=g4f.Provider.Bing,
        messages=prepared_history,
    )

    HISTORY.append({
        'role': 'user',
        'content': query
    })

    HISTORY.append({
        'role': 'bot',
        'content': response
    })

    # Return the answer
    return response

def main():
    '''
    Main function.
    '''
    @BOT.message_handler(commands=['start'])
    def start(message):
        BOT.reply_to(message, '# Welcome!\nI\'m MedusaAI, and I operate here on Telegram to give you the best experience possible. You can start by entering the `/help` command, or asking me a question, just type /query <your question> <model you want to use: `gpt-4`, `gpt-3.5-turbo`>.', parse_mode="Markdown")

    @BOT.message_handler(commands=['help'])
    def help(message):
        BOT.reply_to(message, '# Help\n## Commands\n- `/start`: Shows the start message.\n- `/help`: Shows this help message.\n- `/query <query> <model>`: Queries the bot with the given query and model. Available models: `gpt-4`, `gpt-3.5-turbo`.\n- `/history`: Shows the history of the conversation.\n- `/clear`: Clears the history of the conversation.', parse_mode="Markdown")

    @BOT.message_handler(commands=['query'])
    def query(message):
        # Get the query and model
        parts = message.text.split(' ')
        model = parts[-1]
        query = ' '.join(parts[1:-1])

        if not model.lower() in MODELS:
            BOT.reply_to(message, 'Please, provide a valid model! Available models: `gpt-4`, `gpt-3.5-turbo`', parse_mode="Markdown")
            return

        if not query:
            BOT.reply_to(message, 'Please, provide a query!')
            return
        
        if not model:
            BOT.send_message(message, 'Using default model: `gpt-3.5-turbo`', parse_mode="Markdown")
            model = 'gpt-3.5-turbo'
            return

        answer = generate_answer(query, model)

        # Send the answer
        BOT.reply_to(message, answer, parse_mode="Markdown")

    @BOT.message_handler(commands=['history'])
    def history(message):
        txt_history = ''
        for message in HISTORY:
            txt_history += f'{message["role"]}: {message["content"]}\n'

        # Send the answer
        BOT.reply_to(message, txt_history, parse_mode="Markdown")

    @BOT.message_handler(commands=['clear'])
    def clear(message):
        HISTORY.clear()

        # Send the answer
        BOT.reply_to(message, '# Success\nYour history has been cleared!', parse_mode="Markdown")


if __name__ == '__main__':
    main()

    BOT.infinity_polling()
