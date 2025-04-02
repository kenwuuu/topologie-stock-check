import time
import logging

from topologie import Topologie

# Configure the logger
logging.basicConfig(level=logging.INFO)  # Set the desired log level


def send_text_message(message):
    # Send a text message
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(body=message, from_=twilio_number, to=your_number)
    logging.info("Text message sent!")


def log_start_of_run():
    logging.info("-----")
    logging.info(
        "Checking inventory. Time: " + time.strftime("%H:%M:%S", time.gmtime())
    )


def check_topologie():
    top = Topologie()
    is_available = top.run_inventory_check()
    if is_available:
        send_text_message("lorem ipsum")


while True:
    log_start_of_run()

    check_topologie()

    time.sleep(60 * 60)  # seconds * minutes
