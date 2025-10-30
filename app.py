import os
import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO

# ---------------- Hugging Face API Setup ----------------
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    st.error("Hugging Face API token not found. Set HF_TOKEN in environment variables.")
    st.stop()

client = InferenceClient(api_key=HF_TOKEN)

# ---------------- Streamlit App ----------------
st.set_page_config(page_title="LinkedIn Profile Builder", layout="wide")
st.title("AI LinkedIn Profile Builder")

tab1, tab2 = st.tabs(["Beautify Headshot", "Create LinkedIn Banner"])

# ---------------- Tab 1: Beautify Headshot ----------------
with tab1:
    st.header("Upload your headshot to beautify")
    uploaded_file = st.file_uploader("Upload a photo", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        try:
            img = Image.open(uploaded_file)
            st.image(img, caption="Original Headshot",  width=250)
        except:
            st.error("Cannot open image. Please upload a valid image file.")
            uploaded_file = None

        if uploaded_file and st.button("Beautify Headshot"):
            with st.spinner("Beautifying your photo..."):
                try:
                    uploaded_file.seek(0)
                    img_bytes = uploaded_file.read()

                    # Using public image-to-image model
                    output_image = client.image_to_image(
                        image=img_bytes,
                        prompt="Professional LinkedIn headshot, realistic, well-lit, friendly",
                        model="stabilityai/stable-diffusion-2-inpainting"
                    )

                    if output_image is None:
                        st.error("Model did not return an image. Try again or check the model.")
                    else:
                        st.image(output_image, caption="Beautified Headshot", use_column_width=True)

                        # Download button
                        buf = BytesIO()
                        output_image.save(buf, format="PNG")
                        st.download_button(
                            label="Download Beautified Headshot",
                            data=buf.getvalue(),
                            file_name="beautified_headshot.png",
                            mime="image/png"
                        )

                except Exception as e:
                    st.error(f"Error: {e}")

# ---------------- Tab 2: Create LinkedIn Banner ----------------
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
                        width=1200,
                        height=300
                    )

                    if output_image is None:
                        st.error("Model did not return an image. Try again.")
                    else:
                        st.image(output_image, caption="Generated LinkedIn Banner", use_column_width=True)

                        # Download button
                        buf = BytesIO()
                        output_image.save(buf, format="PNG")
                        st.download_button(
                            label="Download LinkedIn Banner",
                            data=buf.getvalue(),
                            file_name="linkedin_banner.png",
                            mime="image/png"
                        )

                except Exception as e:
                    st.error(f"Error: {e}")
