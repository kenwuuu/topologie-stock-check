import json
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import time
import os
import logging

# URL of the page containing the HTML
url = "https://topologie.com/collections/the-bags/products/flat-sacoche?variant=39841883226172"

# Configure the logger
logging.basicConfig(level=logging.INFO)  # Set the desired log level


def get_page_content():
    # Send a GET request to the URL
    response = requests.get(url)
    return response.content


def parse_page_content(content):
    # Parse the HTML content
    soup = BeautifulSoup(content, "html.parser")
    return soup


def check_inventory(soup, desired_item_name):
    # Find the script with the product JSON
    script = soup.find("script", {"data-product-json": True})
    script_json = json.loads(script.string)

    # Get variants and check if Sand is available
    variants = script_json["variants"]
    for variant in variants:
        if variant["available"]:
            logging.info(f"{variant['title']} available")

            # If Sand is available, send a text message
            if desired_item_name in variant["title"]:
                return desired_item_name
        else:
            logging.info(f"{variant['title']} not available")

    return False

def send_text_message(message, item_name):
    # Send a text message
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(body=message, from_=twilio_number, to=your_number)
    logging.info(f"Text message for {item_name} sent!")


def run_inventory_check():
    content = get_page_content()
    soup = parse_page_content(content)
    item_name = check_inventory(soup, "Moss")
    if item_name:
        send_text_message(f"{item_name} available now", item_name)


# Run every hour
while True:
    # Print UTC time
    logging.info(
        "Checking inventory. Time: " + time.strftime("%H:%M:%S", time.gmtime())
    )
    run_inventory_check()
    time.sleep(60 * 5) # seconds * minutes
