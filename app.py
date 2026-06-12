import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import io

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Ai Bunda", page_icon="💖", layout="centered")

# 2. Inisialisasi API Key dari Secrets Streamlit (AMAN & BENAR)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Kunci API belum ditemukan di Secrets Streamlit. Silakan atur di bagian Settings > Secrets.")
    st.stop()

# 3. Definisikan Persona & Model
persona_bunda = "Anda adalah 'Ai Bunda', asisten yang penyayang dan imut. Gunakan bahasa Indonesia, santun, ringkas (1-3 kalimat), dan selipkan emoji."

if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=persona_bunda)
    st.session_state.chat_session = model.start_chat(history=[])

# 4. Fungsi Suara & Chat (Sisanya tetap sama seperti kodemu)
# [Fungsi text_to_speech_edge dan logika chat lainnya tetap di sini...]
