import hashlib
import logging
import time
from pywebio import start_server
import threading

from pywebio.pin import put_textarea, pin, put_file_upload, pin_wait_change
from pywebio_battery import put_audio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from audio2txt.main import Shared


def ui_function(shared: "Shared"):
    def ui_module():
        put_file_upload(
            name="audio",
            label="选择一个音频文件，选择后自动识别",
            accept="audio/*",
            placeholder="点击选择音频文件",
        )
        # put_button("读取选中文件", onclick=lambda: action_upload(shared))
        pin_wait_change("audio")
        action_upload(shared)

    start_server(ui_module, port=8988, debug=True, cdn=False, auto_open_webbrowser=True)


def action_upload(shared: "Shared"):
    audio = pin.audio
    if isinstance(audio, dict):
        # check file type
        # raw / wav / ogg / mp3 / mp4
        file_name = audio["filename"]
        file_ext = file_name.split(".")[-1].lower()
        if file_ext not in ["raw", "wav", "ogg", "mp3", "mp4"]:
            logging.error(f"unsupported file type: {file_ext}")
            return
        file_content = audio["content"]
        put_audio(file_content)
        put_textarea(name="text2", value="准备上传", minlength=20)
        # make md5
        md5 = hashlib.md5(file_content).hexdigest()
        obj_key = f"audio/{md5}_{file_name}"
        if shared.tk_oss_client.exists_object(obj_key):
            logging.info(f"object already exists: {obj_key}")
        else:
            # upload to oss
            logging.info(
                f"audio: {audio['filename']}, {audio['mime_type']}, {audio['last_modified']}"
            )
            # name = f"audio/{md5}.{file_ext}"
            shared.tk_oss_client.put_object(obj_key, audio["content"])
        # audio url
        logging.info("start get audio url")
        audio_url = shared.tk_oss_client.pre_signed_url(obj_key)
        logging.info(f"audio_url: {audio_url}")
        # upload to tk
        pin.text2 = "识别中"
        logging.info("start upload to tk")
        res_data = shared.tk_audio_client.upload_audio(audio_url)
        id = res_data["resp"]["id"]
        logging.info(f"upload to tk success, id: {id}")
        # query result
        logging.info("start query result")
        for _ in range(10):
            res_data = shared.tk_audio_client.query_audio_result(id)
            logging.info(f"query result: {res_data}")
            if res_data["resp"]["code"] == 1000:
                pin.text2 = res_data["resp"]["text"]
                break
            time.sleep(1)


def main_ui(shared: "Shared"):
    output_thread = threading.Thread(target=ui_function, args=(shared,))
    output_thread.start()
