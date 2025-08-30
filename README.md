
Krishi Sakhi - Streamlit prototype
---------------------------------

Contents:
- app.py : Streamlit application
- requirements.txt : Python dependencies
- logo.png : Placeholder logo

How to run locally:
1. Create a Python virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

   NOTE: 'pyaudio' may require system libraries. On Ubuntu:
     sudo apt-get install portaudio19-dev python3-pyaudio
     pip install pyaudio

   On Windows, install PyAudio wheel from:
   https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

3. Run the app:
   streamlit run app.py

GPS auto-fetch:
- Click 'Fetch GPS' button and allow location in browser. The page will reload with coordinates and the app will show detected coords.

Deploy to Streamlit Cloud:
1. Create a GitHub repo with these files (app.py, requirements.txt, logo.png, README.md).
2. On https://streamlit.io/cloud, connect your GitHub repo and deploy.
3. Note: Microphone/SpeechRecognition on the server may not work in Streamlit Cloud. For voice input, run locally or use an alternative client-side STT.

Important notes:
- Browser TTS/gTTS will convert text to Malayalam/English for prompts and readbacks.
- Speech recognition uses the server's microphone (requires local run). For web-based STT, consider using Web Speech API in a front-end component.

