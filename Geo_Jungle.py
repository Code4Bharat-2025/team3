from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Replace this with your actual Groq API key
groq_api_key = "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"
# Unsplash API key
unsplash_api_key = "iH2yhvxYy2zlFnvrvVbQzISufXlGXmd3xpLV1vWs3Vw"

PROMPT_TEMPLATE = """
You are a geography bot for kids aged 8–12. When given a place name, give a fun, educational, and easy-to-read description that includes the following:

1. 📍 *Location* – Country, continent, and a simple description of where it is on Earth.
2. 🏰 *History* – A very short, kid-friendly summary of its historical background.
3. 🧭 *Nearby Places* – Famous cities, landmarks, or natural features close to it.
4. 🎉 *Fun Facts* – 2 to 3 cool, surprising, or fun facts about the place.
5. 🗣️ *Language & Culture* – What language people speak there, a common greeting, a popular food, or a famous festival.

Use emojis, short sentences, and a fun tone. Keep it under 300 words.

Place: {place}
"""

groq_api_url = "https://api.groq.com/openai/v1/chat/completions"

def get_unsplash_image(place):
    try:
        # Unsplash API to get images
        res = requests.get(
            "https://api.unsplash.com/search/photos",
            params={"query": place, "per_page": 1},
            headers={"Authorization": f"Client-ID {unsplash_api_key}"}
        )
        res.raise_for_status()
        data = res.json()
        if data["results"]:
            return data["results"][0]["urls"]["regular"]
    except Exception as e:
        print("Unsplash error:", e)
    return None

@app.route('/place-info', methods=['POST'])
def get_place_info():
    data = request.json
    place = data.get("place", "").strip()

    if not place:
        return jsonify({"error": "Missing 'place' in request"}), 400

    try:
        prompt = PROMPT_TEMPLATE.format(place=place)

        headers = {
            'Authorization': f'Bearer {groq_api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a fun geography teacher for kids."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        response = requests.post(groq_api_url, json=payload, headers=headers)

        if response.status_code == 200:
            content = response.json().get('choices', [{}])[0].get('message', {}).get('content', 'No text returned')
            image_url = get_unsplash_image(place)
            return jsonify({"place": place, "info": content, "image_url": image_url})
        else:
            return jsonify({"error": response.json().get('error', 'Unknown error')}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>World Geo Bot 🌍</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
                max-width: 800px;
                margin: auto;
                background-color: #f4f4f9;
                color: #333;
                transition: background-image 0.8s ease-in-out;
            }
            .container {
                padding: 20px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h2 {
                text-align: center;
                font-size: 2.5rem;
                color: #4CAF50;
            }
            p {
                font-size: 1.2rem;
                color: #555;
            }
            input, button {
                width: 80%;
                padding: 12px;
                margin-top: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            button {
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            .control-buttons {
                display: flex;
                justify-content: space-around;
                margin-top: 20px;
            }
            .control-buttons button {
                width: 45%;
            }
            pre {
                background-color: #f1f1f1;
                padding: 10px;
                border-radius: 8px;
                margin-top: 15px;
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            .image-container {
                margin-top: 20px;
                text-align: center;
            }
            .image-container img {
                max-width: 100%;
                height: auto;
                border-radius: 10px;
                background-color: transparent;
            }
            .foreground-image {
                position: relative;
                z-index: 1;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>GeoJungle 🌍</h2><br><center><h3>Combines learning about the world with a sense of adventure. </h3></center>
            <p>Enter a place name or use your voice to get a fun geography lesson!</p>
            <form onsubmit="event.preventDefault(); getPlaceInfo();">
                <input type="text" id="placeInput" placeholder="Enter a place (e.g. Tokyo)" required> 
                <div class="control-buttons">
                    <button type="submit">Get Info</button>
                    <button type="button" onclick="startListening()">🎙️Speak</button>
                </div>
            </form>
            <pre id="output"></pre>
            <div class="control-buttons">
                <button onclick="speakOutput()">🔊 Restart</button>
                <button onclick="pauseSpeech()">⏸️ Pause</button>
            </div>

            <div class="image-container">
                <img id="placeImage" src="" alt="Place Image" style="display:none;" class="foreground-image"/>
            </div>
        </div>
        
        <script>
        let currentUtterance = null;
        let pausedText = "";

        async function getPlaceInfo() {
            const place = document.getElementById("placeInput").value;
            const res = await fetch("/place-info", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({place})
            });
            const data = await res.json();
            document.getElementById("output").innerText = data.info || JSON.stringify(data, null, 2);
            
            if (data.image_url) {
                const img = document.getElementById("placeImage");
                img.src = data.image_url;
                img.style.display = "block";
            } else {
                document.getElementById("placeImage").style.display = "none";
            }
            speakOutput();
        }

        function speakOutput() {
            const text = document.getElementById("output").innerText;
            if (!text) return;
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            utterance.rate = 1;

            if (currentUtterance) {
                window.speechSynthesis.cancel(); // Stop any ongoing speech
            }

            currentUtterance = utterance;
            window.speechSynthesis.speak(utterance);
        }

        function pauseSpeech() {
            if (currentUtterance) {
                window.speechSynthesis.pause(); // Pause speech
                pausedText = currentUtterance.text; // Save the current text
            }
        }

        function resumeSpeech() {
            if (pausedText) {
                const utterance = new SpeechSynthesisUtterance(pausedText);
                utterance.lang = 'en-US';
                utterance.rate = 1;
                window.speechSynthesis.speak(utterance); // Resume from paused text
                pausedText = ""; // Reset paused text after resuming
            }
        }

        function startListening() {
            if (!('webkitSpeechRecognition' in window)) {
                alert("Speech recognition not supported in this browser.");
                return;
            }
            const recognition = new webkitSpeechRecognition();
            recognition.lang = "en-US";
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById("placeInput").value = transcript;
                getPlaceInfo();
            };
            recognition.onerror = function(event) {
                alert("Speech recognition error: " + event.error);
            };
            recognition.start();
        }
        </script>
    </body>
    </html>
    '''
    
if __name__ == '__main__':
    app.run(debug=True)
