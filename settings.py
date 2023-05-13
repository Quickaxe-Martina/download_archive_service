import os

from aiohttp.web_app import Application


async def set_settings(app: Application):
    app["LOG_LEVEL"] = os.getenv("LOG_LEVEL", "INFO")
    app["BUFF_SIZE"] = int(os.getenv("BUFF_SIZE", 1024))
    app["BASE_FILE_FOLDER"] = os.getenv("BASE_FILE_FOLDER", "test_photos")
    app["DELAY_TIME"] = int(os.getenv("DELAY_TIME", 0))
