import asyncio
import logging
import os
from asyncio.subprocess import Process

from aiohttp import web
from aiohttp.web_request import Request


async def archive(request: Request):
    archive_hash = request.match_info["archive_hash"]

    if not os.path.exists(f"{request.app['BASE_FILE_FOLDER']}/{archive_hash}"):
        raise web.HTTPNotFound(text="Архив не существует или был удален")

    response = web.StreamResponse()
    response.enable_chunked_encoding()
    response.headers["Content-Disposition"] = "attachment; filename=archive.zip"
    await response.prepare(request)

    program = ["zip", "-r", "-", "."]
    process: Process = await asyncio.create_subprocess_exec(
        *program,
        cwd=f"{request.app['BASE_FILE_FOLDER']}/{archive_hash}",
        stdout=asyncio.subprocess.PIPE,
    )
    try:
        while line := await process.stdout.read(request.app["BUFF_SIZE"]):
            logging.debug(f"{line=}")
            await response.write(line)
            if request.app["DELAY_TIME"]:
                await asyncio.sleep(request.app["DELAY_TIME"])
    except SystemExit as e:
        logging.exception(e)
        raise web.HTTPInternalServerError(text="Произошла внутренняя ошибка сервера")
    except ConnectionResetError:
        logging.info("Download was interrupted")
    finally:
        if process.returncode is None:
            process.kill()
            await process.communicate()
        return response
