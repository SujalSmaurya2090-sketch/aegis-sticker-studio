import streamlit as st
from rembg import remove
from PIL import Image, ImageOps
import io
import numpy as np
import cv2

# 🎨 1. App Structure & Layout Configuration
st.set_page_config(
    page_title="Aegis AI - Sticker Studio", 
    page_icon="⚡", 
    layout="centered"
)

# Premium Cyber Dark Theme Implementation
st.markdown("""
    <style>
    .main { background-color: #0b0f17; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe, #4facfe);
        color: white; border: none; padding: 12px 30px;
        border-radius: 12px; font-weight: bold; width: 100%;
        font-size: 16px; box-shadow: 0px 4px 20px rgba(79, 172, 254, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0px 6px 25px rgba(79, 172, 254, 0.6); }
    </style>
""", unsafe_allow_html=True)

def add_sticker_border(pil_img, border_thickness=12):
    """Advanced Computer Vision Layer: Draws a thick white die-cut outline around the object"""
    padded_img = ImageOps.expand(pil_img, border=border_thickness * 2, fill=(0, 0, 0, 0))
    img_np = np.array(padded_img)
    alpha = img_np[:, :, 3]
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (border_thickness, border_thickness))
    dilated_alpha = cv2.dilate(alpha, kernel, iterations=1)
    
    sticker_np = img_np.copy()
    sticker_np[dilated_alpha > 0] = [255, 255, 255, 255]
    
    mask_indices = alpha > 0
    sticker_np[mask_indices] = img_np[mask_indices]
    
    return Image.fromarray(sticker_np)

# 🖥️ 2. Main Workstation Interface Header
st.title("⚡ Aegis AI: Sticker Studio Machine")
st.markdown("##### Isolate objects and instantly apply professional die-cut white contour borders.")
st.write("---")

# 📂 3. Operations Panel & Pipeline
uploaded_file = st.file_uploader("Upload Image Asset (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Load asset with safe alpha channel configuration
        input_image = Image.open(uploaded_file).convert("RGBA")
        st.image(input_image, caption="Original Asset Layer")
        
        # Triggering AI Computer Vision Processing
        with st.spinner("AI running segmentation matrix & drawing border contours... Please wait..."):
            
            # Phase 1: Object Isolation (Background Removal)
            raw_transparent = remove(input_image)
            
            # Phase 2: Contour Generation
            final_sticker = add_sticker_border(raw_transparent, border_thickness=12)
            
            # Rendering Result
            st.write("---")
            st.subheader("✨ High-Fi Alpha Sticker Output")
            st.image(final_sticker, caption="Generated Sticker Production Model")
            
            # Package asset into direct byte array stream for secure downloading
            buf = io.BytesIO()
            final_sticker.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="📥 Download WhatsApp-Ready Sticker (PNG)",
                data=byte_im,
                file_name=f"aegis_{uploaded_file.name.split('.')[0]}.png",
                mime="image/png"
            )
    except Exception as e:
        st.error(f"System Execution Exception: {e}")
