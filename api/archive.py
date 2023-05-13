import asyncio
import logging
import os
from asyncio import StreamReader
from asyncio.subprocess import Process

from aiohttp import web

from settings import BASE_FILE_FOLDER, BUFF_SIZE, DELAY_TIME


async def write_output(output, stdout: StreamReader):
    while line := await stdout.read(BUFF_SIZE):
        logging.debug(f"[write_output]: {line}")
        await output.write(line)
        if DELAY_TIME:
            await asyncio.sleep(DELAY_TIME)


async def archive(request):
    archive_hash = request.match_info.get("archive_hash")

    if not os.path.exists(f"{BASE_FILE_FOLDER}/{archive_hash}"):
        raise web.HTTPNotFound(text="Архив не существует или был удален")

    response = web.StreamResponse()
    response.headers["Content-Disposition"] = "attachment; filename=archive.zip"
    await response.prepare(request)

    program: list[str] = ["zip", "-r", "-", "."]
    process: Process = await asyncio.create_subprocess_exec(
        *program,
        cwd=f"{BASE_FILE_FOLDER}/{archive_hash}",
        stdout=asyncio.subprocess.PIPE,
    )
    stdout_task = asyncio.create_task(
        write_output(
            output=response,
            stdout=process.stdout,
        ),
    )

    try:
        return_code, _ = await asyncio.gather(process.wait(), stdout_task)
        logging.debug(f"[{' '.join(program)!r} exited with {process.returncode}]")
    except SystemExit as e:
        logging.exception(e)
    except ConnectionResetError:
        logging.info("Download was interrupted")
    finally:
        if process.returncode is None:
            process.kill()
            await process.communicate()
        return response
