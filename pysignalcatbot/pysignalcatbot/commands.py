from loguru import logger
import glob
import os
import random
import base64
from signalbot import Command, Context

class CatNowCommand(Command):
    images = []
    def __init__(self, path):
        # Get all images in the directory
        exts = ['jpg', 'jpeg', 'png']
        for ext in exts:
            self.images += glob.glob(os.path.join(path, f"*.{ext}"))
        
        logger.info(f"Found {len(self.images)} images")

    def describe(self) -> str:
        return "Next Command: Sends the next image"

    async def handle(self, c: Context):
        command = c.message.text.lower()
        if command.startswith("/"):
            logger.debug(f"Received command {command}")
        else: 
            return

        if command == "/cat" or command == "/now":
            logger.info(f"Received command {command}")
            # Select random image
            image_path = random.choice(self.images)
            logger.debug(f"Selected image {image_path}")

            # Load file
            with open(image_path, 'rb') as f:
                image = base64.b64encode(f.read()).decode()

            await c.send("On its way")
            await c.send("",
                         base64_attachments=[image])
            logger.info(f"Sent {image_path}")
        else:
            c.send("Unknown command")
            logger.error(f"Unknown command {command}")
        
        logger.debug(f"Finished handling command {command}")
        return