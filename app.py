import google.generativeai as genai
from dotenv import load_dotenv

import streamlit as st
import os
from PIL import Image




load_dotenv() ## load all environment variables from .env
## Configure Genai Key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def get_gemini_response(image,input):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not  None:
        bytes_data=uploaded_file.getvalue()
        image_parts= [
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts[0]
    else:
        raise FileNotFoundError("no file uploaded")

st.set_page_config(page_title="Text Extractor")

st.header("Gemini Application")
# input= st.text_input("Input Prompt: ",key="input")
uploaded_file=st.file_uploader("Choose an image...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image= Image.open(uploaded_file)
    st.image(image,caption='Uploaded Image:',use_column_width=True)
submit=st.button("Process")
input_propmt="""
You are an expert in reading handwritings.\nYou will get an image containing a handwritten text.\n
You have to generate a textual response of what you read.
"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_propmt,image_data)
    st.subheader("Text-")
    st.write(response)

