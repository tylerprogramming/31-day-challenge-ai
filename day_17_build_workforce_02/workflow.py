import agents
import functions

from moviepy.editor import *
from pydub import AudioSegment

agents.user_proxy.initiate_chat(
    agents.manager,
    message="""Create a prompt for image generation ai with luigi.  Be creative.  The style should be dreamy.
        You will perform the following in order:
        
        1. Create the prompt for the image_creation agent to then generate an image from it.
        2. ONLY WHEN you have called the function for the image creation agent, then move on to the image_describer.
        3. The image_describer agent will then take that image, and then describe it.
        4. Return the output form the image_describer
        5. Then the audio_creator will take the output from image_describer and then create audio from it.
            """
)

image = ImageClip("filename_test.png")

if not os.path.exists("sample.mp3"):
    flac_audio = AudioSegment.from_file("ai_audio.flac", "flac")
    flac_audio.export("sample.mp3", format="mp3")

audio = AudioFileClip("sample.mp3")

image = image.set_position(lambda t: functions.shake(t, (0, 1)))
video = CompositeVideoClip([image.set_duration(audio.duration)])
video = video.set_audio(audio)

video.write_videofile(
    "output.mp4",
    codec='libx264',
    audio_codec='aac',
    temp_audiofile='temp-audio.m4a',
    remove_temp=True,
    fps=30
)
