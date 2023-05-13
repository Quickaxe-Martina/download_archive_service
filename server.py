import asyncio
import datetime
import logging

import aiofiles
from aiohttp import web

from api.archive import archive
from settings import LOG_LEVEL


async def handle_index_page(request):
    async with aiofiles.open("index.html", mode="r") as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type="text/html")


async def uptime_handler(request):
    response = web.StreamResponse()

    response.headers["Content-Type"] = "text/html"

    await response.prepare(request)

    while True:
        formatted_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"{formatted_date}<br>"

        logging.debug(f"write: {message.encode('utf-8')}")
        try:
            await response.write(message.encode("utf-8"))
        except ConnectionResetError:
            break

        await asyncio.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL)
    app = web.Application()
    app.add_routes(
        [
            web.get("/", handle_index_page),
            web.get("/archive/{archive_hash}/", archive),
            web.get("/server_time/", uptime_handler),
        ]
    )
    web.run_app(app)
