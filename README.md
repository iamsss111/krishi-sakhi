
# Krishi Sakhi (Streamlit Cloud Version)

### ✅ Features
- ✅ Language selection (English / Malayalam)
- ✅ Voice prompts via gTTS
- ✅ Voice input using browser Web Speech API (works on Chrome)
- ✅ GPS auto-detection using HTML5 Geolocation
- ✅ Simple green-white UI

---
### ✅ How to Deploy on Streamlit Cloud
1. Upload these files to a **public GitHub repo**.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Connect your GitHub account.
4. Create a **New App**:
   - **Repository:** `yourusername/yourrepo`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Deploy. After build, you will get a live URL.

---
### ✅ How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
---
### ✅ Notes
- Voice input works in **Chrome desktop or Android browsers**.
- GPS detection needs location permission.
- Internet required for gTTS.
