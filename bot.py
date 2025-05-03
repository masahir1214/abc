import streamlit as st
from diffusers import AutoPipelineForText2Image
import torch
from PIL import Image
import soundfile as sf
#from IPython.display import Audio  # Remove or comment out this line to avoid streamlit issue
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

# Load pipelines outside the functions for efficiency
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16)
if torch.cuda.is_available():
    pipe.to("cuda")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(device)
tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

def generate_image(prompt):
    image = pipe(prompt, guidance_scale=7.5).images[0]
    return image

def text_to_speech(speech_prompt, description):
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(speech_prompt, return_tensors="pt").input_ids.to(device)
    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()
    sf.write("parler_tts_out.wav", audio_arr, model.config.sampling_rate)
    # return Audio("parler_tts_out.wav") # Modify to return the audio path instead of Audio object
    return "parler_tts_out.wav" 

st.title("Mimo - AI Assistant")

input_name = st.text_input("Hi, My name is mimo. What's your name?")
if input_name:
    st.write(f"Nice to meet you {input_name}")
    task_choice = st.selectbox("Do you want to check the tasks I can perform?", ["Yes", "No"])

    if task_choice == "Yes":
        task_type = st.selectbox("Choose a task:", ["Text-to-Speech", "Text-to-Image"])

        if task_type == "Text-to-Speech":
            speech_prompt = st.text_input("Enter your prompt to generate speech:")
            if speech_prompt:
                with st.spinner("Generating speech..."):
                    description = "A male speaker delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."
                    audio_file = text_to_speech(speech_prompt, description)
                    st.audio(audio_file) 

        elif task_type == "Text-to-Image":
            image_prompt = st.text_input("Enter your prompt to generate image:")
            if image_prompt:
                with st.spinner("Generating image..."):
                    image = generate_image(image_prompt)
                    st.image(image)

    elif task_choice == "No":
        st.write(f"Nice to meet you {input_name}, see you soon!")