import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Ai Bunda", page_icon="💖", layout="centered")

# Mengambil kunci dari brankas rahasia
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("🔑 API Key belum ditemukan. Silakan atur di Settings > Secrets.")
    st.stop()

# Persona Ai Bunda
st.title("💖 Ai Bunda")
st.caption("Tempat bersandar, bercerita, dan mencari kedamaian hati seorang Ibu.")
st.divider()

# Inisialisasi model
model = genai.GenerativeModel("gemini-1.5-flash")

# Menyimpan riwayat pesan
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan pesan yang sudah ada
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari pengguna
if prompt := st.chat_input("Apa yang ingin kamu ceritakan ke Bunda hari ini, Nak?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bunda memproses jawaban
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Pesan persona Bunda
        pesan_bunda = f"Sebagai sosok Ibu yang penyayang, berikan jawaban hangat dan menenangkan untuk: {prompt}"
        
        response = model.generate_content(pesan_bunda)
        full_response = response.text
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
