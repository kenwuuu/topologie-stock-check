import json
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import time
import os


# Twilio account SID and auth token
account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']

# Twilio phone number and your own phone number
twilio_number = os.environ['twilio_number']
your_number = os.environ['your_number']

# URL of the page containing the HTML
url = "https://topologie.com/collections/the-bags/products/flat-sacoche?variant=39841883226172"


def get_page_content():
    # Send a GET request to the URL
    response = requests.get(url)
    return response.content


def parse_page_content(content):
    # Parse the HTML content
    soup = BeautifulSoup(content, "html.parser")
    return soup


def check_inventory(soup):
    # List of available colors
    colors = ["Dry Black", "Moss", "Slate", "Sand", "Mustard", "Black", "Bronze", "Future Blue", "Peach"]

    # Find the script with the product JSON
    script = soup.find("script", {"data-product-json": True})
    script_json = json.loads(script.string)

    # Get variants and check if Sand is available
    variants = script_json["variants"]
    for variant in variants:
        if variant["available"]:
            print(f"{variant['title']} available")

            # If Sand is available, send a text message
            if variant["title"] == "Sand":
                send_text_message("The Sand variant is available!")
        else:
            print(f"{variant['title']} not available")


def send_text_message(message):
    # Send a text message
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=your_number
    )
    print("Text message sent!")


def run_inventory_check():
    content = get_page_content()
    soup = parse_page_content(content)
    check_inventory(soup)


# run every hour
while True:
    run_inventory_check()
    time.sleep(60 * 60)
