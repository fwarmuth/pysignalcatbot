import click
from loguru import logger
import glob
import os
import random
import base64
import requests

from pysignalcatbot.bot import Bot
from pysignalcatbot.commands import CatNowCommand

# Start command:
@click.command()
@click.option('--interval', default=60, help='Interval in seconds')
@click.option('--path', default='../images', help='Path to the directory')
@click.option('--number', default='-1', help='Phone number sending from', type=str)
@click.option('--recipients', type=str, help='Phone number or groups of recipients')
@click.option('--api-endpoint', default='http://localhost:18080/v2/send', help='API endpoint path, of the "signal-cli-rest-api"')
def start(**kwargs):
    logger.info(f'Starting SignalCatBot with {kwargs["path"]}')

    # Parse recipients as list of string
    kwargs['recipients'] = kwargs['recipients'].split(',')

    bot = Bot(kwargs)


# Send single image command:
@click.command()
@click.option('--path', default='../images', help='Path to the directory')
@click.option('--number', default='-1', help='Phone number sending from', type=str)
@click.option('--recipients', type=str, help='Phone number or groups of recipients')
@click.option('--api-endpoint', default='http://localhost:18080/v2/send', help='API endpoint path, of the "signal-cli-rest-api"')
def single(**kwargs):
    # Parse recipients as list of string
    kwargs['recipients'] = kwargs['recipients'].split(',')

    # Find all images in the directory
    images = []
    exts = ['jpg', 'jpeg', 'png']
    for ext in exts:
        images += glob.glob(os.path.join(kwargs['path'], f"*.{ext}"))
    
    logger.info(f"Found {len(images)} images")

    # Select random image
    image_path = random.choice(images)
    # Load image
    with open(image_path, 'rb') as f:
        image = base64.b64encode(f.read()).decode()
    
    # Create a request
    content_type = 'application/json'
    host = kwargs['api_endpoint']
    data = {
        # "message": "A cat a day keeps the doctor away",
        "base64_attachments": [image],
        "number": kwargs['number'],
        "recipients": kwargs['recipients'],
    }
    # Send request
    headers = {
        'Content-Type': content_type,
    }
    response = requests.post(host, headers=headers, json=data)
    logger.info(f"response: {response}")

