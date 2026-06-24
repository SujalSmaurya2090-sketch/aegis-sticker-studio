import streamlit as st
from rembg import remove
from PIL import Image, ImageOps
import io
import base64
import numpy as np
import cv2

# 🎨 App Configurations
st.set_page_config(
    page_title="Aegis AI - Sticker Studio", 
    page_icon="⚡", 
    layout="wide"
)

# Custom Cyber Dark Theme Styling
st.markdown("""
    <style>
    .main { background-color: #0b0f17; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe, #4facfe);
        color: white; border: none; padding: 12px 30px;
        border-radius: 12px; font-weight: bold; width: 100%;
        box-shadow: 0px 4px 20px rgba(79, 172, 254, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

def add_sticker_border(pil_img, border_thickness=12):
    """Adds a clean white contour border around the asset"""
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

# Main UI Setup
st.title("⚡ Aegis AI: Professional Sticker Studio Machine")
st.markdown("##### Isolate objects and instantly apply die-cut white contour borders.")

st.write("---")

main_col1, main_col2 = st.columns([1, 1])

with main_col1:
    st.subheader("📂 Drop Source Asset")
    uploaded_file = st.file_uploader("Upload Image Asset (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        input_image = Image.open(uploaded_file).convert("RGBA")
        
        with main_col1:
            st.write("**Original Photo:**")
            st.image(input_image, use_container_width=True)
            
        with main_col2:
            st.subheader("✨ High-Fi Alpha Sticker Output")
            with st.spinner("AI running segmentation matrix..."):
                # Background removal
                raw_transparent = remove(input_image)
                # Adding contour border
                final_sticker = add_sticker_border(raw_transparent, border_thickness=12)
                
                st.image(final_sticker, use_container_width=True, caption="Generated Sticker Asset Model")
                
                buf = io.BytesIO()
                final_sticker.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 Download WhatsApp-Ready Sticker (PNG)",
                    data=byte_im,
                    file_name=f"aegis_sticker_{uploaded_file.name.split('.')[0]}.png",
                    mime="image/png"
                )
    except Exception as e:
        st.error(f"Execution Error: {e}")
