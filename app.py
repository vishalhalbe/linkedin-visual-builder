import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Load your Hugging Face API token from Streamlit secrets
API_TOKEN = st.secrets["huggingface"]["api_token"]

HEADSHOT_MODEL = "valiantcat/Qwen-Image-Edit-MeiTu"  # Image-to-image beautify
BANNER_MODEL = "stabilityai/stable-diffusion-2"      # Text-to-image banner generation

HEADSHOT_API_URL = f"https://api-inference.huggingface.co/models/{HEADSHOT_MODEL}"
BANNER_API_URL = f"https://api-inference.huggingface.co/models/{BANNER_MODEL}"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query_image_edit(image_bytes):
    payload = {
        "inputs": image_bytes,
        "options": {"wait_for_model": True}
    }
    response = requests.post(HEADSHOT_API_URL, headers=headers, data=image_bytes)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        st.error(f"Headshot beautify failed: {response.status_code} - {response.text}")
        return None

def query_text_to_image(prompt):
    payload = {"inputs": prompt, "options": {"wait_for_model": True}}
    response = requests.post(BANNER_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        st.error(f"Banner generation failed: {response.status_code} - {response.text}")
        return None

st.title("AI LinkedIn Profile Enhancer")

tab1, tab2 = st.tabs(["Beautify Headshot", "Create LinkedIn Banner"])

with tab1:
    st.header("Upload your headshot to beautify")
    uploaded_file = st.file_uploader("Upload a photo", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original Headshot", use_column_width=True)

        if st.button("Beautify Headshot"):
            with st.spinner("Beautifying your photo..."):
                img_bytes = uploaded_file.read()
                result_img = query_image_edit(img_bytes)
                if result_img:
                    st.image(result_img, caption="Beautified Headshot", use_column_width=True)

with tab2:
    st.header("Generate a LinkedIn Banner from Text")
    prompt = st.text_area("Describe your ideal LinkedIn banner:", height=100,
                          placeholder="E.g., professional corporate banner with blue tones and modern design")
    if st.button("Generate Banner"):
        if not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating your LinkedIn banner..."):
                banner_img = query_text_to_image(prompt.strip())
                if banner_img:
                    st.image(banner_img, caption="Generated LinkedIn Banner", use_column_width=True)
