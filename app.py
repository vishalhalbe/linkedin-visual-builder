import os
import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO

# Ensure HF_TOKEN is set in environment variables
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    st.error("Hugging Face API token not found. Set HF_TOKEN in environment variables.")
    st.stop()

client = InferenceClient(api_key=HF_TOKEN)

st.title("AI LinkedIn Profile Enhancer")

tab1, tab2 = st.tabs(["Beautify Headshot", "Create LinkedIn Banner"])

# -------------------- Tab 1: Beautify Headshot --------------------
with tab1:
    st.header("Upload your headshot to beautify")
    uploaded_file = st.file_uploader("Upload a photo", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original Headshot", use_column_width=True)

        if st.button("Beautify Headshot"):
            with st.spinner("Beautifying your photo..."):
                input_bytes = uploaded_file.read()
                try:
                    # Replace with a public image-to-image model
                    output_image = client.image_to_image(
                        input_image=input_bytes,
                        prompt="Professional LinkedIn headshot, well-lit, realistic",
                        model="runwayml/stable-diffusion-v1-5",
                    )
                    st.image(output_image, caption="Beautified Headshot", use_column_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# -------------------- Tab 2: Create LinkedIn Banner --------------------
with tab2:
    st.header("Generate a LinkedIn Banner from Text")
    prompt = st.text_area(
        "Describe your ideal LinkedIn banner:",
        height=100,
        placeholder="E.g., professional corporate banner with blue tones and modern design"
    )

    if st.button("Generate Banner"):
        if not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating your LinkedIn banner..."):
                try:
                    output_image = client.text_to_image(
                        prompt=prompt.strip(),
                        model="stabilityai/stable-diffusion-2-1",
                        width=1200,   # Banner width
                        height=300    # Banner height
                    )
                    st.image(output_image, caption="Generated LinkedIn Banner", use_column_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")
