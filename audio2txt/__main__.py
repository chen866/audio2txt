import logging

from dotenv import load_dotenv

from audio2txt.main import Shared
from audio2txt.ui import main_ui

# logging
logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s [%(filename)s:%(lineno)d] %(levelname)s - %(message)s"
    )
)
logging.getLogger("root").addHandler(handler)

load_dotenv()
shared = Shared()
main_ui(shared)

# test_id = "7e385009-6eda-475a-af52-3a263376acc1"
# res_data = shared.tk_audio_client.query_audio_result(test_id)
# raise
