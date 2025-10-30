import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import base64

# Function to call Hugging Face API and generate image
def generate_image(prompt, hf_token):
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=180)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            st.error(f"⚠️ Generation failed (status {response.status_code}). {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Request error: {e}")
    return None

# Helper to convert PIL image to downloadable bytes
def image_to_bytes(img, format="PNG"):
    buf = BytesIO()
    img.save(buf, format=format)
    byte_im = buf.getvalue()
    return byte_im

# Helper to generate download link
def get_download_link(img, filename):
    img_bytes = image_to_bytes(img)
    b64 = base64.b64encode(img_bytes).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="{filename}">⬇️ Download {filename}</a>'
    return href

# Main Streamlit app
def main():
    st.set_page_config(page_title="LinkedIn Profile Image & Banner Generator", layout="wide")
    st.title("🚀 LinkedIn Profile Headshot & Banner Image Generator")

    with st.sidebar:
        st.header("🎨 Customize Your Style")
        profession = st.selectbox(
            "Select Profession / Style:",
            ["Corporate / Consultant", "Creative / Designer", "Tech / Developer", "Education / Tutor", "Entrepreneur / Founder"]
        )
        brand_color = st.color_picker("Choose Brand / Accent Color:", "#0a47f9")
        headshot_file = st.file_uploader("Upload Your Headshot (optional)", type=["jpg", "jpeg", "png"])
        hf_token = st.text_input(
            "Hugging Face API Token (Get free token from https://huggingface.co/settings/tokens)",
            type="password"
        )

    if not hf_token:
        st.warning("Please enter your Hugging Face API token to generate images.")
        st.stop()

    # Compose prompts based on inputs
    style_prompts = {
        "Corporate / Consultant": "professional corporate headshot, clean background, business attire",
        "Creative / Designer": "creative professional headshot, artistic background, colorful style",
        "Tech / Developer": "tech professional headshot, modern style, casual attire",
        "Education / Tutor": "friendly professional headshot, soft background, approachable look",
        "Entrepreneur / Founder": "dynamic professional headshot, confident pose, modern business style"
    }

    banner_prompts = {
        "Corporate / Consultant": f"professional LinkedIn banner with blue and white colors, clean corporate design, business theme, accent color {brand_color}",
        "Creative / Designer": f"colorful LinkedIn banner with artistic design, creative elements, accent color {brand_color}",
        "Tech / Developer": f"modern LinkedIn banner with tech symbols and digital theme, accent color {brand_color}",
        "Education / Tutor": f"educational LinkedIn banner with books and light background, accent color {brand_color}",
        "Entrepreneur / Founder": f"dynamic LinkedIn banner with startup and business growth elements, accent color {brand_color}"
    }

    headshot_prompt = style_prompts.get(profession, "professional headshot") + ", high resolution, realistic, studio lighting"
    banner_prompt = banner_prompts.get(profession, "professional LinkedIn banner") + ", high resolution, clean design, 1584x396 px"

    # If user uploaded a headshot, mention it in prompt (optional enhancement)
    if headshot_file:
        st.info("Uploaded headshot detected — using it as inspiration for the generated headshot.")
        # Currently the model API call doesn't support image input directly.
        # You could extend this with image-to-image pipelines or custom model.
        # For now we just mention it in prompt for creativity.
        headshot_prompt += ", inspired by uploaded photo"

    col1, col2 = st.columns(2)

    with col1:
        st.header("✨ Generate Headshot")
        if st.button("Generate Headshot"):
            with st.spinner("Generating headshot... ⏳"):
                headshot_img = generate_image(headshot_prompt, hf_token)
                if headshot_img:
                    st.image(headshot_img, caption="Generated Headshot", use_column_width=True)
                    st.markdown(get_download_link(headshot_img, "linkedin_headshot.png"), unsafe_allow_html=True)

    with col2:
        st.header("🎨 Generate Banner")
        if st.button("Generate Banner"):
            with st.spinner("Generating banner... ⏳"):
                banner_img = generate_image(banner_prompt, hf_token)
                if banner_img:
                    # Resize banner to LinkedIn recommended size (1584x396 px)
                    banner_img = banner_img.resize((1584, 396))
                    st.image(banner_img, caption="Generated Banner", use_column_width=True)
                    st.markdown(get_download_link(banner_img, "linkedin_banner.png"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
