import os

import asyncio

from pydub import AudioSegment

from src.settings import ASSETS_DIR


class AudioSplitter:
    def _split_audio(self, input_file):
        """
        Load a stereo audio file, split it into monophonic channels
        """
        try:
            # Determine the file extension
            file_extension = os.path.splitext(input_file)[1]
            file_format = file_extension[1:]

            # Load the stereo audio file
            audio = AudioSegment.from_file(input_file, format=file_format)

            # Split it into monophonic channels
            left_channel = audio.split_to_mono()[0]
            right_channel = audio.split_to_mono()[1]

            return left_channel, right_channel
        except Exception as e:
            print(f"Error: {e}")

    async def split_audio(self, input_file):
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self._split_audio, input_file)
        return result


async def test():
    input_audio_file = ASSETS_DIR / 'sample-12s.mp3'

    audio_splitter = AudioSplitter()
    await audio_splitter.split_audio(input_audio_file)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test())

