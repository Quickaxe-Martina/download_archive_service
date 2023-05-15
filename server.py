from logging import config as logging_config

import aiofiles
from aiohttp import web
from aiohttp.web_request import Request

from api.archive import archive
from logging_config import LOGGING
from settings import set_settings

logging_config.dictConfig(LOGGING)


async def handle_index_page(request: Request):
    async with aiofiles.open("index.html", mode="r") as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type="text/html")


if __name__ == "__main__":
    app = web.Application()
    app.on_startup.append(set_settings)
    app.add_routes(
        [
            web.get("/", handle_index_page),
            web.get("/archive/{archive_hash}/", archive),
        ]
    )
    web.run_app(app)
