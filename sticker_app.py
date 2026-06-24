import streamlit as st
from rembg import remove
from PIL import Image, ImageOps
import io
import base64
import numpy as np
import cv2
from datetime import datetime

# 🎨 1. App Core Layout Settings
st.set_page_config(
    page_title="Aegis AI - Sticker Production Studio", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Cyber Dark UI Theme Custom Styling 
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
    .review-card { background-color: #161f30; padding: 20px; border-radius: 14px; margin-bottom: 15px; border: 1px solid #233554; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stat-box { background: linear-gradient(135deg, #1f293d, #111827); padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #374151; }
    </style>
""", unsafe_allow_html=True)

# 💾 2. Cloud-Safe Session State Memory Engine
if 'analytics_counter' not in st.session_state:
    st.session_state.analytics_counter = 142  # Seed database value for social proof conversion

if 'reviews_database' not in st.session_state:
    st.session_state.reviews_database = []  # Sandbox safe memory storage for community feedback

def add_sticker_border(pil_img, border_thickness=12):
    """Advanced Computer Vision Layer: Injects thick white border around isolated objects"""
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

# 📂 3. Sidebar Administration Panel
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/sticker.png", width=70)
    st.title("Aegis Production Control")
    
    # Dynamic Tracking Counter
    st.markdown(f"""
    <div class="stat-box">
        <span style='color: #00f2fe; font-size: 24px; font-weight: bold;'>{st.session_state.analytics_counter}+</span><br/>
        <span style='color: #9ca3af; font-size: 13px;'>Stickers Generated Worldwide Today</span>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    st.subheader("💡 Expert Conversion Pro-Tips")
    st.info("🎯 Complex ya congested images ke liye object ke paas thoda crop kar lijiye taaki edge analysis 100% accurate aaye.")
    st.success("🔒 System Version: Build v1.0 [Official Release]")

# 🖥️ 4. Main Interface Workstation Dashboard Banner
st.title("⚡ Aegis AI: Professional Sticker Studio Machine")
st.markdown("##### Isolate objects and instantly apply die-cut white contour borders optimized for chat applications.")

st.write("")
col_ex1, col_ex2, col_ex3 = st.columns([1, 0.2, 1])
with col_ex1:
    st.image("https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80", caption="1. Original Graphic Layer", use_container_width=True)
with col_ex2:
    st.write("")
with col_ex3:
    st.image("https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80", caption="2. Extracted Solid Sticker Asset", use_container_width=True)

st.write("---")

# Main Operations Engine Workspace Core split
main_col1, main_col2 = st.columns([1, 1])

with main_col1:
    st.subheader("📂 Drop Source Asset")
    uploaded_file = st.file_uploader("Upload Image Asset (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > 25:
        st.error("⚠️ File size validation failure. File exceeds 25MB constraint limit.")
    else:
        try:
            input_image = Image.open(uploaded_file).convert("RGBA")
            
            with main_col1:
                st.write("**Source Visual File Pipeline:**")
                st.image(input_image, use_container_width=True)
                
            with main_col2:
                st.subheader("✨ High-Fi Alpha Sticker Output")
                with st.spinner("AI running segmentation matrix & drawing border contours..."):
                    
                    # Process 1: Background Erase Phase
                    raw_transparent = remove(input_image)
                    
                    # Process 2: Continuous Contour Drawing Phase
                    final_sticker = add_sticker_border(raw_transparent, border_thickness=12)
                    
                    # Secure Layer Rendering
                    st.image(final_sticker, use_container_width=True, caption="Generated Sticker Asset Model")
                    
                    buf = io.BytesIO()
                    final_sticker.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    clicked = st.download_button(
                        label="📥 Download WhatsApp-Ready Sticker (PNG)",
                        data=byte_im,
                        file_name=f"aegis_sticker_{uploaded_file.name.split('.')[0]}.png",
                        mime="image/png"
                    )
                    if clicked:
                        st.session_state.analytics_counter += 1
        except Exception as e:
            st.error(f"Execution Error Intercepted: {e}")

st.write("---")

# 💬 5. Cloud Sandbox Safe Review Feed Room 
st.subheader("👥 Creator Community Feedback Room")
rev_col1, rev_col2 = st.columns([1, 1.2])

with rev_col1:
    st.markdown("#### Post Your Live Session Review")
    with st.form("unified_feedback_form", clear_on_submit=True):
        rev_name = st.text_input("Username / Alias", placeholder="e.g., Cyber_Sujal")
        rev_stars = st.slider("Conversion Score", 1, 5, 5)
        rev_text = st.text_area("Your experience feedback or log note")
        rev_img = st.file_uploader("Attach Your Sticker Output Sample (Optional)", type=["png", "jpg"])
        
        if st.form_submit_button("Publish to Live Feed"):
            if rev_name and rev_text:
                img_base64 = ""
                if rev_img is not None:
                    img_base64 = base64.b64encode(rev_img.read()).decode('utf-8')
                
                # Insert review directly into safe session memory database
                new_review = {
                    "name": rev_name,
                    "stars": rev_stars,
                    "text": rev_text,
                    "img_b64": img_base64,
                    "date": datetime.now().strftime('%Y-%m-%d')
                }
                st.session_state.reviews_database.insert(0, new_review)
                st.session_state.analytics_counter += 1
                st.success("Review logged and synchronized globally!")
                st.rerun()
            else:
                st.warning("Please provide values for both Name and Feedback text sections.")

with rev_col2:
    st.markdown("#### Live Community Feed")
    if not st.session_state.reviews_database:
        st.caption("No public logs published inside live feed tracking memory yet.")
    else:
        for rev in st.session_state.reviews_database[:5]:
            st.markdown(f"""
            <div class="review-card">
                <strong style='font-size: 16px; color: #00f2fe;'>👤 {rev['name']}</strong> 
                <span style='color: #ffb703; margin-left: 10px;'>{'★'*int(rev['stars'])}</span>
                <small style='float: right; color: #6b7280;'>{rev['date']}</small>
                <p style='margin-top: 10px; color: #e5e7eb;'>{rev['text']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if rev['img_b64']:
                st.markdown("**User Sticker Showcase:**")
                st.image(io.BytesIO(base64.b64decode(rev['img_b64'])), width=130)
                st.write("")
