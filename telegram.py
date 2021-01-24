import telebot

from constants import TELEGRAM_TOKEN
from models import ProductRequest
from parse import RequestService
from products import ProductService

bot = telebot.TeleBot(TELEGRAM_TOKEN)
print("Бот запущен")

product_request_dict = {}
request_service = RequestService()
product_service = ProductService()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=True)
    user_markup.row("/start", "/stop", "/help")
    user_markup.row("Добавить запись", "Найти")
    bot.send_message(message.chat.id, 'Добрый день ' + message.from_user.first_name + '.Я бот. Приятно познакомиться', reply_markup=user_markup)
    msg = bot.reply_to(message, "Что вы хотите?")

@bot.message_handler(commands=['stop'])
def send_welcome(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "...", reply_markup=hide_markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'добавить запись':
        msg = bot.send_message(message.chat.id, "Введите название продукта")
        bot.register_next_step_handler(msg, process_create_record)
    elif message.text.lower() == 'найти':
        msg = bot.send_message(message.chat.id, "Введите название продукта")
        bot.register_next_step_handler(msg, process_find_record)
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')
        bot.clear_step_handler_by_chat_id(message.chat.id)

def process_create_record(message):
    product_request = ProductRequest()
    product_request.product_name = message.text
    product_request_dict[message.chat.id] = product_request
    msg = bot.send_message(message.chat.id, "Введите ссылку на irecommend")
    bot.register_next_step_handler(msg, process_create_record_2)

def process_create_record_2(message):
    try:
        product_request = product_request_dict[message.chat.id]
        product_request.url = message.text
        print(product_request)
        product = request_service.get_product_info(product_request)
        product_service.save(product)
        bot.send_message(message.chat.id, "Спасибо за добавленный продукт")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Что-то пошло не так")
        bot.clear_step_handler_by_chat_id(message.chat.id)

def process_find_record(message):
    try:
        product_name = message.text
        product = product_service.find_by_name(product_name)
        bot.send_photo(message.chat.id, product.image_url)
        product_info = "Наименование: " + product.name + " Ссылка: " + product.link_url + " Рейтинг: " + str(
            product.rating)
        bot.send_message(message.chat.id, product_info)

        for review in product.reviews:
            review_info = "Отзыв от: " + review.reviewer_name + " Время: " + review.post_time + " Рейтинг: " + str(review.rating) +\
                          " Загаловок: " + review.title + " Ссылка на отзыв: " + review.read_link
            bot.send_message(message.chat.id, review_info)

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Не удалось найти продукт")


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(none_stop=True, interval=0)
