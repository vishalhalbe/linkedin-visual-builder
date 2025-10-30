import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import os

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="LinkedIn Visual Builder", layout="wide")
st.title("🌟 LinkedIn Visual Builder (Free AI Edition)")
st.markdown(
    "Easily create **professional LinkedIn headshots and banners** following 2025 design best practices — all with free AI tools."
)
st.markdown("---")

# -------------------------------
# SIDEBAR SETTINGS
# -------------------------------
st.sidebar.header("🎨 Customize Your Style")

profession = st.sidebar.selectbox(
    "Select Profession / Style:",
    [
        "Corporate / Consultant",
        "Tech / Developer",
        "Creative / Designer",
        "Coach / Speaker",
        "Academic / Researcher",
    ],
)

color_tone = st.sidebar.color_picker("Choose Brand / Accent Color:", "#0A66C2")

uploaded_file = st.sidebar.file_uploader(
    "Upload Your Headshot (optional)", type=["jpg", "jpeg", "png"]
)

# Retrieve Hugging Face API token
hf_token = st.sidebar.text_input(
    "🔑 Hugging Face API Token",
    placeholder="Get one free from https://huggingface.co/settings/tokens",
    type="password",
)
if not hf_token:
    # Fallback to Streamlit secret if deployed on Streamlit Cloud
    hf_token = os.environ.get("HF_TOKEN")

st.sidebar.markdown(
    "📘 **Tip:** Free Hugging Face accounts allow limited image generations daily."
)

# -------------------------------
# PROMPTS (headshot + banner)
# -------------------------------
prompts = {
    "Corporate / Consultant": {
        "headshot": (
            "professional business headshot, confident smile, soft natural lighting, "
            "neutral gray background, corporate attire, realistic DSLR portrait, LinkedIn profile photo"
        ),
        "banner": f"minimal elegant LinkedIn banner, soft city skyline blur, geometric overlay, clean design, {color_tone} accent, 1584x396 aspect ratio",
    },
    "Tech / Developer": {
        "headshot": (
            "tech professional headshot, bright background, soft natural light, "
            "tech-casual clothing, realistic DSLR portrait, LinkedIn photo"
        ),
        "banner": f"futuristic digital LinkedIn banner, glowing circuit lines, blue-gray gradient with {color_tone} tone, sleek modern look, 1584x396",
    },
    "Creative / Designer": {
        "headshot": (
            "creative portrait, colorful studio lighting, confident and approachable expression, "
            "artistic blurred background, DSLR realism"
        ),
        "banner": f"vibrant creative LinkedIn banner, geometric shapes, gradient with {color_tone}, minimal yet bold design, 1584x396",
    },
    "Coach / Speaker": {
        "headshot": (
            "motivational coach headshot, warm tones, confident friendly smile, "
            "studio light, professional DSLR photo, LinkedIn-ready"
        ),
        "banner": f"inspirational LinkedIn banner with soft gradient, stage lights, and {color_tone} accent, uplifting tone, 1584x396",
    },
    "Academic / Researcher": {
        "headshot": (
            "academic portrait, thoughtful look, soft light, calm neutral background, "
            "professional attire, realistic DSLR photograph"
        ),
        "banner": f"clean academic LinkedIn banner, abstract network or science motif, minimal professional layout, subtle {color_tone} accent, 1584x396",
    },
}

# -------------------------------
# FUNCTION: Generate image via Hugging Face API
# -------------------------------
def generate_image(prompt, hf_token):
    """Call Hugging Face Stable Diffusion API to generate an image."""
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}
    response = requests.post(url, headers=headers, json=payload, timeout=180)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        st.error(f"⚠️ Generation failed (status {response.status_code}). Try again later.")
        st.text(response.text)
        return None


# -------------------------------
# LAYOUT
# -------------------------------
col1, col2 = st.columns(2)

# ===== HEADSHOT =====
with col1:
    st.subheader("👤 Profile Photo")

    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Uploaded Headshot", use_column_width=True)
    else:
        if st.button("✨ Generate AI Headshot"):
            if not hf_token:
                st.warning("⚠️ Please enter or set your Hugging Face token.")
            else:
                st.info("Generating your professional headshot... please wait ⏳")
                head_img = generate_image(prompts[profession]["headshot"], hf_token)
                if head_img:
                    st.image(head_img, caption="AI-Generated Headshot", use_column_width=True)
                    buf = BytesIO()
                    head_img.save(buf, format="PNG")
                    st.download_button(
                        "⬇️ Download Headshot",
                        data=buf.getvalue(),
                        file_name="linkedin_headshot.png",
                        mime="image/png",
                    )

# ===== BANNER =====
with col2:
    st.subheader("🌆 Banner Image")
    if st.button("🎨 Generate AI Banner"):
        if not hf_token:
            st.warning("⚠️ Please enter or set your Hugging Face token.")
        else:
            st.info("Generating your LinkedIn banner... this can take 20–40 seconds ⏳")
            banner_img = generate_image(prompts[profession]["banner"], hf_token)
            if banner_img:
                st.image(banner_img, caption="AI-Generated Banner", use_column_width=True)
                buf = BytesIO()
                banner_img.save(buf, format="PNG")
                st.download_button(
                    "⬇️ Download Banner",
                    data=buf.getvalue(),
                    file_name="linkedin_banner.png",
                    mime="image/png",
                )

# -------------------------------
# BOTH IMAGES TOGETHER
# -------------------------------
st.markdown("---")
st.subheader("🧩 Optional: Generate Both at Once")
if st.button("🚀 Generate Headshot + Banner"):
    if not hf_token:
        st.warning("⚠️ Please enter your Hugging Face token.")
    else:
        st.info("Creating both images... please wait ⏳")
        head_img = generate_image(prompts[profession]["headshot"], hf_token)
        banner_img = generate_image(prompts[profession]["banner"], hf_token)
        if head_img and banner_img:
            c1, c2 = st.columns(2)
            with c1:
                st.image(head_img, caption="AI Headshot", use_column_width=True)
            with c2:
                st.image(banner_img, caption="AI Banner", use_column_width=True)
            st.success("✅ Both images generated successfully!")

# -------------------------------
# PROMPT DETAILS
# -------------------------------
st.markdown("---")
st.subheader("🧠 AI Prompt Details (for transparency or custom editing)")
st.text_area("Headshot Prompt", prompts[profession]["headshot"], height=80)
st.text_area("Banner Prompt", prompts[profession]["banner"], height=80)

st.markdown("---")
st.caption("⚙️ Built with Streamlit + Hugging Face Stable Diffusion 2 • Created with GPT-5 • 2025 LinkedIn Visual Best Practices")
