import asyncio

from io import BytesIO
from pydub import AudioSegment


async def split_audio(binary_audio_data: bytes) -> list[AudioSegment]:
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, _split_audio, binary_audio_data)
    return result


def _split_audio(binary_audio_data: bytes) -> list[AudioSegment]:
    """
    Split a stereo audio file represented as binary data into monophonic channels

    :param binary_audio_data: Binary audio data representing a stereo audio file
    :return: A list of AudioSegment objects representing the monophonic channels
    """
    try:
        # Load the stereo audio file
        audio = AudioSegment.from_file(BytesIO(binary_audio_data))

        # Split it into monophonic channels
        audio_channels = audio.split_to_mono()
        return audio_channels
    except Exception as e:
        print(f"Error: {e}")
