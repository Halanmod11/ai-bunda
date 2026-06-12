import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import io

# Konfigurasi Halaman
st.set_page_config(page_title="Ai Bunda", page_icon="💖")

# Ambil API Key dari Secrets (bukan dari dalam kode)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Waduh, kunci API belum diatur di Secrets. Tolong cek Settings > Secrets di Streamlit Cloud!")
    st.stop()

st.title("💖 Ai Bunda")
st.write("Halo anakku sayang, Bunda siap mendengarkanmu.")

# Sisa kode kamu taruh di sini (persona, fungsi chat, dll)
