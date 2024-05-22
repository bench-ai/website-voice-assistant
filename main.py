import os
import time

from agent.conduit import LiveConduit
from agent.config.operation import OpenAISettings
from agent.config.session import Session
from record import record_audio
from transcribe import transcribe_audio
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPEN_AI")

sess = Session(live=True, session_lifetime=1_000_000, command_lifetime=20_000)
open_ai = OpenAISettings(api_key=key, model="gpt-4o-2024-05-13")

brow_opts = sess.new_browser_operation()
llm_opts = sess.new_llm_operation(3, 400, [open_ai])

with LiveConduit(sess):
    brow_opts.add_navigate_command("https://www.bench-ai.com/")
    time.sleep(5)
    sc = brow_opts.add_full_screenshot_command(10, "test.jpg", "s1")
    llm_opts.add_standard_command("system", "you are a assistant that helps individuals"
                                            " who are blind understand webpages by operating as their eyes")

    mm = llm_opts.add_multimodal_command("user")
    mm.add_content("image_url", sc.get_image().byte_string)

    run = 0

    while run < 3:
        print("Please ask a question")
        print()
        print()
        record_audio()
        print("here finished recording")
        #
        text = transcribe_audio()
        print(f"transcribed text: {text}")

        llm_opts.add_standard_command("user", text)
        print("good")
        com = llm_opts.execute()
        print(com.content)
        llm_opts.add_response(com)
        run+=1



