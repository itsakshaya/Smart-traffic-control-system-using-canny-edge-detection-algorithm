import streamlit as st
import numpy as np
from PIL import Image
import os
import cv2

# PAGE
st.set_page_config(page_title="Smart Traffic Control", layout="wide")

st.title("🚦 Smart Traffic Control System")
st.markdown("Using Canny Edge Detection")
st.markdown("---")

# SIDEBAR
st.sidebar.title("Settings")

low = st.sidebar.slider("Low Threshold", 10, 100, 50)
high = st.sidebar.slider("High Threshold", 100, 300, 150)

st.sidebar.markdown("""
### Density Rules
<12% → Low  
12–30% → Medium  
>30% → High
""")

# ─────────────────────────────
# FUNCTIONS
# ─────────────────────────────
def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    return gray, blur

def detect_edges(image, low, high):
    return cv2.Canny(image, low, high)

def calculate_density(edge_img):
    kernel = np.ones((3,3), np.uint8)
    clean = cv2.morphologyEx(edge_img, cv2.MORPH_CLOSE, kernel)

    edge_pixels = np.sum(clean == 255)
    total_pixels = clean.size

    density = (edge_pixels / total_pixels) * 100

    density = density * 2.2
    density = min(density, 100)

    return round(density, 2)

def signal_logic(density):
    if density < 12:
        return "Low", 20, "Low traffic"
    elif density < 30:
        return "Medium", 40, "Moderate traffic"
    else:
        return "High", 60, "Heavy traffic"

# ─────────────────────────────
# INPUT
# ─────────────────────────────
st.subheader("📷 Step 1: Upload or Select Image")

option = st.radio("Choose Input Type", ["Upload Image", "Use Dataset"])

image = None

if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload image", type=["jpg","png","jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

else:
    dataset_path = os.path.join(os.getcwd(), "Vehicle_Detection_Image_Dataset", "train", "images")

    if os.path.exists(dataset_path):

        images = [f for f in os.listdir(dataset_path)
                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if images:
            selected = st.selectbox("Select Dataset Image", images)

            if selected:
                image = Image.open(os.path.join(dataset_path, selected)).convert("RGB")
        else:
            st.warning("No image files found in dataset")

    else:
        st.warning("⚠️ Dataset not available in cloud. Please upload an image.")

# ─────────────────────────────
# PROCESS
# ─────────────────────────────
if image:

    img = np.array(image)

    st.markdown("---")

    # STEP 2
    st.subheader("🔲 Step 2: Preprocessing")

    gray, blur = preprocess(img)

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Original Image", use_container_width=True)
    with col2:
        st.image(gray, caption="Grayscale Image")

    st.markdown("---")

    # STEP 3
    st.subheader("✏️ Step 3: Edge Detection")

    edges = detect_edges(blur, low, high)

    col3, col4 = st.columns(2)
    with col3:
        st.image(blur, caption="Blurred Image")
    with col4:
        st.image(edges, caption="Edge Image")

    st.markdown("---")

    # STEP 4
    st.subheader("📊 Step 4: Traffic Density")

    density = calculate_density(edges)

    col5, col6 = st.columns([1,2])
    with col5:
        st.metric("Density", f"{density}%")
    with col6:
        st.progress(min(density/100,1.0))
        st.caption("Edge pixel percentage")

    if density < 5:
        st.error("❌ Not a traffic image")
        st.stop()

    st.markdown("---")

    # STEP 5
    st.subheader("🚦 Step 5: Signal Decision")

    level, time, msg = signal_logic(density)

    if level == "Low":
        color = "#d4edda"
        text = "#155724"
        emoji = "🟢"
    elif level == "Medium":
        color = "#fff3cd"
        text = "#856404"
        emoji = "🟡"
    else:
        color = "#f8d7da"
        text = "#721c24"
        emoji = "🔴"

    st.markdown(f"""
    <div style="background:{color}; padding:20px; border-radius:10px;">
        <h2 style="color:{text};">{emoji} {level} Traffic</h2>
        <h3 style="color:{text};">Green Signal: {time} sec</h3>
        <p style="color:{text};">{msg}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # SUMMARY
    st.subheader("📋 Summary")

    summary = {
        "Step": ["Input", "Grayscale", "Blur", "Edges", "Density", "Signal"],
        "Result": ["Done", "Done", "Done", "Done", f"{density}%", f"{level} → {time}s"]
    }

    st.table(summary)

# FOOTER
st.markdown("---")
st.caption("MCA Project | Smart Traffic Control | Python + OpenCV + Streamlit")
