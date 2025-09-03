import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# --- Your Parking Details ---
APARTMENT = "S102"
MAKE = "Toyota"
MODEL = "Prius"
PLATE = "DARR32"
EMAIL = "sanjar29@colostate.edu"

def register_car():
    options = Options()
    options.add_argument("--headless")           # run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    driver.get("https://www.register2park.com/")

    # Click "Register Vehicle"
    driver.find_element(By.XPATH, "//button[contains(text(),'Register Vehicle')]").click()
    time.sleep(2)

    # Search for property
    search_box = driver.find_element(By.TAG_NAME, "input")
    search_box.send_keys("Bighorn Landing Apartments")
    time.sleep(2)

    # Select property
    driver.find_element(By.XPATH, "//button[contains(text(),'Select')]").click()
    time.sleep(2)

    # Choose Visitor Parking
    driver.find_element(By.XPATH, "//button[contains(text(),'Visitor Parking')]").click()
    time.sleep(2)

    # Fill form
    driver.find_element(By.NAME, "ApartmentNumber").send_keys(APARTMENT)
    driver.find_element(By.NAME, "Make").send_keys(MAKE)
    driver.find_element(By.NAME, "Model").send_keys(MODEL)
    driver.find_element(By.NAME, "LicensePlate").send_keys(PLATE)
    driver.find_element(By.NAME, "ConfirmLicensePlate").send_keys(PLATE)
    driver.find_element(By.XPATH, "//button[contains(text(),'Next')]").click()
    time.sleep(3)

    # Email confirmation
    email_input = driver.find_element(By.NAME, "Email")
    email_input.send_keys(EMAIL)
    driver.find_element(By.XPATH, "//button[contains(text(),'Confirm')]").click()

    time.sleep(3)
    driver.quit()

def start(update: Update, context: CallbackContext):
    keyboard = [[KeyboardButton("Do it")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("👋 Tap the button below to register your car:", reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Do it":
        update.message.reply_text("🚗 Registering your car...")
        register_car()
        update.message.reply_text("✅ Done! Car registered for 24 hours.")

# --- TELEGRAM BOT SETUP ---
BOT_TOKEN = os.getenv("BOT_TOKEN")  # read token from environment
updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
updater.idle()
