import streamlit as st
from diffusers import DiffusionPipeline
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="LinkedIn Visual Builder", layout="wide")
st.title("AI LinkedIn Profile Builder")

tab1, tab2 = st.tabs(["Beautify Headshot", "Create LinkedIn Banner"])

# ---------------- Tab 1: Beautify Headshot ----------------
with tab1:
    st.header("Upload your headshot to beautify")
    uploaded_file = st.file_uploader("Upload a photo", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        try:
            img = Image.open(uploaded_file)
            st.image(img, caption="Original Headshot", width=250)  # smaller preview
        except:
            st.error("Cannot open image. Please upload a valid image file.")
            uploaded_file = None

        if uploaded_file and st.button("Beautify Headshot"):
            with st.spinner("Beautifying your photo..."):
                try:
                    # Load the Qwen Image Edit model (public)
                    pipe = DiffusionPipeline.from_pretrained("valiantcat/Qwen-Image-Edit-MeiTu")

                    # Prompt for headshot enhancement
                    prompt = "Professional LinkedIn headshot, realistic, well-lit, friendly"

                    output_image = pipe(image=img, prompt=prompt).images[0]

                    st.image(output_image, caption="Beautified Headshot", width=250)

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
                    # Load the text-to-image model (public)
                    pipe_banner = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1")

                    output_image = pipe_banner(prompt=prompt.strip(), width=1200, height=300).images[0]

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
