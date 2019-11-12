#myapp/telegrambot.py
import telegram
from telegram.utils.request import Request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job, JobQueue, CallbackQueryHandler
from telegram.ext import messagequeue as mq
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
import logging
from cv import Id_Admins, Caption_Template
import cv
from logoadder import watermark_vid, watermark_pic

logging.basicConfig(filename = 'bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def handleAll(bot, update):
	try:
		userId = update.message.chat_id
		caption = Caption_Template%(update.message.caption or ' ')#if update.message.caption!=None else ' '
		if userId in Id_Admins:
			if update.message.photo:
				bot.send_chat_action(userId, telegram.ChatAction.UPLOAD_PHOTO)
				file_id = update.message.photo[-1]
				newImage = bot.get_file(file_id)
				newImage.download('files/to_watermark_pic.png')
				watermark_pic()
				bot.send_photo(chat_id=userId, photo=open('files/watermarked_pic.png', 'rb'), caption=caption, parse_mode=telegram.ParseMode.HTML)
			elif update.message.video:
				bot.send_chat_action(userId, telegram.ChatAction.UPLOAD_VIDEO)
				file_id = update.message.video
				newVideo = bot.get_file(file_id)
				bot.send_message(update.message.chat_id, text='Watermarking')
				newVideo.download('files/to_watermark_vid.mp4')
				duration, width, height = watermark_vid()
				bot.send_video(chat_id=userId, video=open('files/watermarked_vid.mp4', 'rb'), 
								duration=duration, width=width, height=height, caption=caption, parse_mode=telegram.ParseMode.HTML)
			elif update.message.animation:
				bot.send_chat_action(userId, telegram.ChatAction.UPLOAD_VIDEO)
				file_id = update.message.animation
				newVideo = bot.get_file(file_id)
				bot.send_message(update.message.chat_id, text='Watermarking')
				newVideo.download('files/to_watermark_vid.mp4')
				watermark_vid()
				bot.send_animation(chat_id=userId, animation=open('files/watermarked_vid.mp4', 'rb'), caption=caption, parse_mode=telegram.ParseMode.HTML)

	except Exception as e:
		bot.send_message(update.message.chat_id, text='Error :|')
		logger.exception('in text message')


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
	logger.info("Loading handlers for telegram bot")

	updater = telegram.ext.updater.Updater(token="TOKEN")
	dp = updater.dispatcher

	dp.add_handler(MessageHandler(Filters.all, handleAll))
	dp.add_error_handler(error)

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()