import json
import os

import requests


def transcribe_audio(api_key: str):
    files = {
        'file': ('output.wav', open('output.wav', 'rb')),
        # if you need to specify the content type
        # 'file_field_name': ('filename.txt', open('path/to/your/file.txt', 'rb'), 'text/plain')
    }

    req = requests.post("https://api.openai.com/v1/audio/transcriptions",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                        },
                        files=files,
                        data={"model": "whisper-1"}
                        )

    return json.loads(req.content)["text"]


if __name__ == '__main__':
    key = os.getenv("OPEN_AI")
    print(transcribe_audio(key))
