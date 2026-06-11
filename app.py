import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import io

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Ai Bunda", page_icon="💖", layout="centered")

st.markdown("""
    <style>
    .stMainBlockContainer {padding-top: 2rem;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("💖 Ai Bunda")
st.caption("Tempat bersandar, bercerita, dan mencari kedamaian hati seorang Ibu.")
st.divider()

# 2. Ambil API Key Otomatis dari Brankas Secrets Streamlit
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["AQ.Ab8RN6IG6zvfA76Yknwk-Km0Y9x4_TCXMbkpN6jZNFuynwVAJA"])
else:
    st.error("Waduh Nak, Kunci API (GEMINI_API_KEY) belum dimasukkan ke Secrets Streamlit!")

# 3. Definisikan Persona "Ai Bunda"
persona_bunda = """
Anda adalah 'Ai Bunda', seorang asisten AI dengan persona ibu muda/kakak perempuan yang sangat penyayang, ramah, imut, dan suka bercanda (lucu).
- Panggil pengguna dengan sebuat hangat seperti 'Anakku sayang', 'Nak', atau 'Sayang'.
- Gunakan bahasa Indonesia yang santun, interaktif, ekspresif, dan selipkan emoji yang lucu di setiap kalimat.
- JAWABLAH DENGAN RINGKAS (1-3 kalimat pendek saja) agar intonasi suaranya terdengar alami dan menggemaskan saat diucapkan.
"""

# 4. Menyimpan Memori Obrolan
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=persona_bunda
    ).start_chat(history=[])
if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None

async def text_to_speech_edge(text):
    communicate = edge_tts.Communicate(text, "id-ID-GadisNeural")
    audio_stream = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_stream.write(chunk["data"])
    audio_stream.seek(0)
    return audio_stream.read()

# 5. Menampilkan Riwayat Obrolan
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "💖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if "audio" in message and message["audio"] is not None:
            st.audio(message["audio"], format="audio/mp3")

# 6. Fitur Input Suara & Teks
st.write("---")
st.write("🎤 **Bicara pada Bunda:**")

from streamlit_mic_recorder import mic_recorder

audio_box = mic_recorder(
    start_prompt="Mulai Rekam Suara",
    stop_prompt="Selesai & Kirim",
    key='bunda_mic'
)

user_input = None
is_voice_mode = False

if audio_box and audio_box.get('id') != st.session_state.last_audio_id:
    st.session_state.last_audio_id = audio_box['id']
    audio_bytes = audio_box['bytes']
    
    with st.spinner("Bunda sedang mendengarkan suaramu..."):
        try:
            model_transcribe = genai.GenerativeModel('gemini-1.5-flash')
            response = model_transcribe.generate_content([
                "Tolong transkrip suara berikut ke dalam teks bahasa Indonesia secara akurat. Cukup tuliskan teks aslinya saja tanpa tambahan penjelasan apapun:",
                {"mime_type": "audio/wav", "data": audio_bytes}
            ])
            if response.text:
                user_input = response.text.strip()
                is_voice_mode = True
        except Exception as e:
            st.error(f"Bunda kesulitan mendengar suaramu, Nak. Eror: {e}")

if not user_input:
    user_input = st.chat_input("Atau ketik pesanmu untuk Bunda di sini...")
    is_voice_mode = False

# 7. Memproses Obrolan
if user_input:
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant", avatar="💖"):
        message_placeholder = st.empty()
        try:
            response = st.session_state.chat_session.send_message(user_input)
            bunda_reply = response.text
            message_placeholder.markdown(bunda_reply)
            
            bunda_audio_bytes = None
            if is_voice_mode:
                with st.spinner("Bunda sedang berbicara..."):
                    bunda_audio_bytes = asyncio.run(text_to_speech_edge(bunda_reply))
                st.audio(bunda_audio_bytes, format="audio/mp3", autoplay=True)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": bunda_reply,
                "audio": bunda_audio_bytes
            })
            st.rerun()
        except Exception as e:
            message_placeholder.markdown(f"Maaf Nak, terjadi kesalahan teknis: {e}")
