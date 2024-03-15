from transformers import AutoProcessor
from transformers import MusicgenForConditionalGeneration
import torch
import scipy

model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-large")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model.to(device)

processor = AutoProcessor.from_pretrained("facebook/musicgen-large")

inputs = processor(
    text=["I want a Metallica band sound"],
    padding=True,
    return_tensors="pt",
)

audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=1024)

sampling_rate = model.config.audio_encoder.sampling_rate

scipy.io.wavfile.write(
    "musicgen_out_metallica.wav",
    rate=sampling_rate,
    data=audio_values[0, 0].cpu().numpy())
