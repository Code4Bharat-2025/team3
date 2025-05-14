# 🌍 GeoJungle - Fun Geography Bot for Kids!

GeoJungle is an interactive Flask-based web application designed to provide fun, educational geography insights for kids aged 8–12. Using AI-generated responses, the app delivers engaging place descriptions, complete with location details, history, nearby places, fun facts, and cultural insights. It also fetches relevant images to enhance the learning experience.

## 🚀 Features
- 🧠 **AI-powered Place Descriptions** - Fun and engaging geography content tailored for kids.
- 📷 **Image Retrieval** - Fetches images dynamically using Unsplash API.
- 🔊 **Text-to-Speech** - Reads out descriptions for an immersive learning experience.
- 🎙️ **Speech Recognition** - Allows kids to speak place names instead of typing.
- 🎨 **Interactive UI** - Clean and fun design for an engaging experience.

## 🛠 Tech Stack
- **Backend:** Flask (Python), Flask-CORS
- **Frontend:** HTML, CSS, JavaScript
- **APIs:** Groq AI API, Unsplash API, Web Speech API
- **Libraries:** Requests, SpeechSynthesis API (Browser)
- **Deployment:** Local Flask server (can be deployed on AWS/GCP/Heroku)

## 🌐 APIs & Services Used
- **Groq AI API** (`https://api.groq.com/openai/v1/chat/completions`)  
  - Used to generate AI-powered place descriptions based on a structured prompt.
- **Unsplash API** (`https://api.unsplash.com/search/photos`)  
  - Used to retrieve relevant images of places for visual learning.
- **Web Speech API (Browser)**  
  - Used for speech recognition and text-to-speech functionality.

## 🔧 Installation
### Prerequisites
- Python 3.x
- Flask & Flask-CORS
- Requests package

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/Code4Bharat-2025/team3

2. Install dependencies:
pip install -r requirements.txt
- Run the application:
python app.py


3. Open in browser:
http://127.0.0.1:5000/


4. 📈 Future Scope & Improvements
- Interactive Features
- Gamification elements like quizzes and geography challenges.
- Integration of an interactive world map for deeper exploration.
- Improved Image Handling
- Multilingual & Accessibility
- Mobile & Cross-Platform Support
- Progressive Web App (PWA) for a seamless experience on all devices.


Let the learning adventure begin! 🚀✨
