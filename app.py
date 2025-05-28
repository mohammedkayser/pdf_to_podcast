import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from utils.pdf_processor import PDFProcessor
from utils.summarizer import PodcastScriptGenerator
from utils.audio_generator import AudioGenerator

# Load environment variables
load_dotenv()

# App Config
st.set_page_config(page_title="PDF to Podcast", layout="centered")
st.title("🎧 PDF to Podcast Converter")
st.markdown("Upload a research paper PDF and get a podcast-style MP3 narration.")

# Set up directories
DATA_DIR = Path("data")
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
for folder in [INPUT_DIR, OUTPUT_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# File uploader
uploaded_file = st.file_uploader("📄 Upload your PDF file", type="pdf")

if uploaded_file:
    # Save the uploaded PDF
    pdf_path = INPUT_DIR / uploaded_file.name
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # Process button
    if st.button("🎙️ Generate Podcast"):
        with st.spinner("Extracting text from PDF..."):
            pdf_processor = PDFProcessor(max_pages=50)
            extracted_text = pdf_processor.extract_text(str(pdf_path))

        with st.spinner("Generating podcast script using Gemini..."):
            script_generator = PodcastScriptGenerator(model_name="gemini-1.5-flash")
            script = script_generator.generate_script(extracted_text)
            script_path = OUTPUT_DIR / f"{pdf_path.stem}_script.txt"
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script)

        st.text_area("📝 Generated Podcast Script", script, height=300)

        with st.spinner("Converting script to audio using ElevenLabs..."):
            audio_generator = AudioGenerator()
            audio_path = OUTPUT_DIR / f"{pdf_path.stem}.mp3"
            audio_success = audio_generator.generate_audio(script, str(audio_path))

        if audio_success:
            st.success("🎉 Podcast generation complete!")
            st.audio(str(audio_path), format='audio/mp3')
            with open(audio_path, "rb") as f:
                st.download_button("⬇️ Download MP3", f, file_name=audio_path.name)
        else:
            st.error("❌ Failed to generate audio. Please try again.")
