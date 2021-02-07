import telebot
from check import check_one_person
import schedule
import threading
import time
from send_mail import send_mail
from hide import TELEGRAM_BOT_API, CHAT_MESSAGE_ID, users

bot = telebot.TeleBot(
    TELEGRAM_BOT_API, parse_mode="MARKDOWN")

chat_message_id = CHAT_MESSAGE_ID


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['id'])
def send_id(message):
    bot.reply_to(message, "Hey my friend, your id is: **"+str(message.from_user.id)+"**")
    # print(message)

@bot.message_handler(commands=['info'])
def send_id(message):
    bot.reply_to(message, u"ℹ Information:\nchat id: {}\nyour id: {}".format(message.chat.id, message.from_user.id))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def send_to_the_group():
    bot.send_message(chat_message_id, "My test")


def daily_check():
    for student in users:
        print("[+] Start check {}".format(student['name']))
        result, message = check_one_person(student)
        bot.send_message(chat_message_id, student['name']+"\n"+message)

def send_time():
    bot.send_message(chat_message_id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def my_schedule():
    schedule.every().day.at("08:30").do(daily_check)
    print("[+] Add daily check schedule")
    schedule.every(4).hours.do(send_time)   # 每四个小时判断服务器状态
    print("[+] Add time send schedule")
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    print("Thread start")
    task = threading.Thread(target=my_schedule)
    task.setDaemon(True)
    task.start()
    print("Task started!")
    bot.polling()

if __name__ == "__main__":
    main()
