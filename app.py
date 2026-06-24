import streamlit as st
from rembg import remove
from PIL import Image, ImageOps
import io
import numpy as np
import cv2

# 🎨 App Structure (No external image loading constraints to prevent crash)
st.set_page_config(
    page_title="Aegis AI - Sticker Studio", 
    page_icon="⚡", 
    layout="centered"
)

def add_sticker_border(pil_img, border_thickness=12):
    """Adds a thick white die-cut contour border around the isolated object"""
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

# Main UI Header
st.title("⚡ Aegis AI: Sticker Studio")
st.write("Isolate objects and instantly apply die-cut white contour borders.")
st.write("---")

# File Upload Panel
uploaded_file = st.file_uploader("Choose an image (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Load image safely
        input_image = Image.open(uploaded_file).convert("RGBA")
        st.image(input_image, caption="Original Image")
        
        # Start AI Processing Layer
        with st.spinner("AI running object isolation & contouring... Please wait..."):
            
            # Step 1: Remove background
            raw_transparent = remove(input_image)
            
            # Step 2: Add solid white border
            final_sticker = add_sticker_border(raw_transparent, border_thickness=12)
            
            # Render Output
            st.write("---")
            st.subheader("✨ High-Fi Sticker Output")
            st.image(final_sticker, caption="Generated Sticker Model")
            
            # Prepare download buffer
            buf = io.BytesIO()
            final_sticker.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="📥 Download WhatsApp Sticker (PNG)",
                data=byte_im,
                file_name=f"aegis_{uploaded_file.name.split('.')[0]}.png",
                mime="image/png"
            )
    except Exception as e:
        st.error(f"Processing Error: {e}")
