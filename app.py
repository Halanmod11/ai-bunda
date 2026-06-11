import streamlit as st
from google import genai
from google.genai import types
import asyncio
import edge_tts
import time
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

# 2. Inisialisasi API Key Utama
API_KEY_1 = "AQ.Ab8RN6KS94PmEmZHXiuV3S5HnZt1VL-bNOwsPwRrc4t6KD5pSQ"

def get_genai_client():
    return genai.Client(api_key=API_KEY_1)

# 3. Definisikan Persona "Ai Bunda"
persona_bunda = """
Anda adalah 'Ai Bunda', seorang asisten AI dengan persona ibu muda/kakak perempuan yang sangat penyayang, ramah, imut, dan suka bercanda (lucu).
- Panggil pengguna dengan sebutan hangat seperti 'Anakku sayang', 'Nak', atau 'Sayang'.
- Gunakan bahasa Indonesia yang santun, interaktif, ekspresif, dan selipkan emoji yang lucu di setiap kalimat.
- JAWABLAH DENGAN RINGKAS (1-3 kalimat pendek saja) agar intonasi suaranya terdengar alami dan menggemaskan saat diucapkan.
"""

# 4. Menyimpan Memori Obrolan
MODEL_NAME = "gemini-2.5-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    client = get_genai_client()
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=persona_bunda,
            temperature=0.8
        )
    )
if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None

def send_message_with_retry(text_input, retries=3, delay=2):
    for i in range(retries):
        try:
            return st.session_state.chat_session.send_message(text_input)
        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)
                continue
            raise e

def generate_content_with_retry(contents, retries=3, delay=2):
    for i in range(retries):
        try:
            client = get_genai_client()
            return client.models.generate_content(model=MODEL_NAME, contents=contents)
        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)
                continue
            raise e

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

# 6. Fitur Pesan Suara & Teks Input
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
            audio_file = types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav")
            response = generate_content_with_retry(
                contents=["Tolong transkrip suara berikut ke dalam teks bahasa Indonesia secara akurat. Cukup tuliskan teks aslinya saja tanpa tambahan penjelasan apapun:", audio_file]
            )
            if response.text:
                user_input = response.text.strip()
                is_voice_mode = True
        except Exception as e:
            st.error(f"Bunda kesulitan mendengar suaramu, Nak. Eror: {e}")

if not user_input:
    user_input = st.chat_input("Atau ketik pesanmu untuk Bunda di sini...")
    is_voice_mode = False

# 7. Memproses Input & Membuat Balasan
if user_input:
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant", avatar="💖"):
        message_placeholder = st.empty()
        try:
            response = send_message_with_retry(user_input)
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
