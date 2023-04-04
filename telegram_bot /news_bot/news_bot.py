import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from get_news import *


def main():
    lst_news = get_news()
    
    
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f'''Xin chào, {update.effective_user.first_name}
    Vui lòng chọn các lệnh sau:
        1. /help
        2. /news
        3. /update (10s/post)
                                        ''')

    async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
        news_top = ''
        for new in lst_news:
            news_top += new +'\n'
        await update.message.reply_text(f'''
10 tin mới nhất:
{news_top}
                                        ''')
    repeat = True
    async def update(update: Update, context: ContextTypes.DEFAULT_TYPE):

        while repeat:
            lst_news = get_news()
            await update.message.reply_text(f'''
Tin mới nhất:
{lst_news[0]}
/stop_update
                                        ''')
            time.sleep(10)
    async def stop_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
        global repeat
        repeat = False
        await update.message.reply_text(f'''
stoping
                                        ''')

    app = ApplicationBuilder().token("6088851168:AAHfFLpcKgMCYj0Ds7HKZ-5o9-tScHkBRvM").build()

    app.add_handler(CommandHandler(["start","help"], help))

    app.add_handler(CommandHandler("news", news))
    
    app.add_handler(CommandHandler("update", update))
    
    app.add_handler(CommandHandler("stop_update", stop_update))
    
    app.run_polling()
    
    
if __name__ == "__main__":
    main()

