import os

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
BUFF_SIZE: int = int(os.getenv("BUFF_SIZE", "1024"))
BASE_FILE_FOLDER: str = os.getenv("BASE_FILE_FOLDER", "test_photos")
DELAY_TIME = int(os.getenv("DELAY_TIME", "0"))
