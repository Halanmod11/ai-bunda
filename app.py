<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Bunda - Teman Ngobrolmu</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7f6;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .chat-container {
            width: 100%;
            max-width: 400px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 80vh;
        }
        .chat-header {
            background-color: #ff7675;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
        }
        .chat-box {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background-color: #fff9f9;
            display: flex;
            flex-direction: column;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 75%;
            word-wrap: break-word;
            line-height: 1.4;
        }
        .bunda-msg {
            background-color: #ffeaa7;
            color: #2d3436;
            align-self: flex-start;
        }
        .user-msg {
            background-color: #e0f7fa;
            color: #2d3436;
            align-self: flex-end;
        }
        .loading-msg {
            font-style: italic;
            color: #b2bec3;
            align-self: flex-start;
        }
        .user-input-area {
            display: flex;
            padding: 15px;
            background: white;
            border-top: 1px solid #eee;
        }
        .user-input-area input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 20px;
            outline: none;
        }
        .btn {
            background-color: #ff7675;
            color: white;
            border: none;
            padding: 10px 15px;
            margin-left: 5px;
            border-radius: 50%;
            cursor: pointer;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">
        👩‍🦰 AI Bunda Pintar
    </div>

    <div class="chat-box" id="chatBox">
        <div class="message bunda-msg">
            Halo sayang, ada yang bisa Bunda bantu hari ini? Kamu mau cerita apa?
        </div>
    </div>

    <div class="user-input-area">
        <input type="text" id="userInput" placeholder="Ketik pesan untuk Bunda..." onkeypress="cekEnter(event)">
        <button class="btn" onclick="kirimPesan()">➡️</button>
    </div>
</div>

<script>
    // Taruh API Key dari Google AI Studio di bawah ini
   GEMINI_API_KEY=AQ.Ab8RN6KS94PmEmZHXiuV3S5HnZt1VL-bNOwsPwRrc4t6KD5pSQ
    // Instruksi kepribadian agar AI bertingkah seperti Bunda
    const KepribadianBunda = "Kamu adalah seorang Ibu kandung bernama 'Bunda'. Kamu sangat penyayang, lemah lembut, sabar, dan protektif. Jawablah semua pertanyaan anakmu dengan panggilan hangat seperti 'sayang', 'nak', atau 'anakku'. Berikan nasihat yang bijak, memotivasi, dan selalu gunakan bahasa Indonesia yang santun dan penuh kasih sayang.";

    function suaraBicara(teks) {
        window.speechSynthesis.cancel(); // Hentikan suara sebelumnya jika ada
        let suaraBunda = new SpeechSynthesisUtterance(teks);
        suaraBunda.lang = 'id-ID'; 
        suaraBunda.pitch = 1.2;    
        suaraBunda.rate = 0.95;     
        window.speechSynthesis.speak(suaraBunda);
    }

    function cekEnter(event) {
        if (event.key === "Enter") {
            kirimPesan();
        }
    }

    async function kirimPesan() {
        let input = document.getElementById("userInput");
        let chatBox = document.getElementById("chatBox");
        let pesanTeks = input.value.trim();
        
        if(pesanTeks !== "") {
            // 1. Tampilkan pesan user
            let pesanUser = document.createElement("div");
            pesanUser.className = "message user-msg";
            pesanUser.innerText = pesanTeks;
            chatBox.appendChild(pesanUser);
            
            input.value = ""; 
            chatBox.scrollTop = chatBox.scrollHeight; 

            // 2. Tampilkan tulisan "Bunda sedang mengetik..."
            let loading = document.createElement("div");
            loading.className = "message loading-msg";
            loading.innerText = "Bunda sedang berpikir...";
            chatBox.appendChild(loading);
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                // 3. Panggil Otak AI Gemini
                let response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        contents: [{ 
                            parts: [{ text: `${KepribadianBunda}\n\nAnakmu bertanya: ${pesanTeks}` }] 
                        }]
                    })
                });

                let data = await response.json();
                let jawabanBunda = data.candidates[0].content.parts[0].text;

                // Hapus tulisan loading
                chatBox.removeChild(loading);

                // 4. Tampilkan jawaban asli dari AI Bunda
                let balasanBunda = document.createElement("div");
                balasanBunda.className = "message bunda-msg";
                balasanBunda.innerText = jawabanBunda;
                chatBox.appendChild(balasanBunda);
                chatBox.scrollTop = chatBox.scrollHeight;

                // 5. AI Bunda otomatis berbicara menceritakan jawabannya
                suaraBicara(jawabanBunda);

            } catch (error) {
                chatBox.removeChild(loading);
                console.error(error);
                let errorMsg = document.createElement("div");
                errorMsg.className = "message bunda-msg";
                errorMsg.innerText = "Aduh sayang, koneksi Bunda lagi terganggu nih. Coba cek API Key kamu ya.";
                chatBox.appendChild(errorMsg);
            }
        }
    }
</script>

</body>
</html>
