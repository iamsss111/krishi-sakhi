
import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import tempfile
import os
from googletrans import Translator
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="Krishi Sakhi", page_icon="🌱", layout="centered")

# Initialize translator
translator = Translator()

# Helper: translate UI text
def tr(text, lang):
    if lang == "മലയാളം":
        try:
            return translator.translate(text, dest='ml').text
        except Exception:
            return text
    return text

# TTS
def speak(text, lang):
    try:
        code = 'ml' if lang == "மലയാളம்" or lang == "മലയാളം" else ('ml' if lang=="മലയാളം" else 'en')
    except Exception:
        code = 'ml' if lang == "മലയാളം" else 'en'
    # Use gTTS
    tts = gTTS(text=text, lang='ml' if lang == "മലയാളം" else 'en')
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tmp_name = tmp.name
    tmp.close()
    tts.save(tmp_name)
    audio_bytes = open(tmp_name, "rb").read()
    st.audio(audio_bytes, format='audio/mp3')
    try:
        os.remove(tmp_name)
    except:
        pass

# Speech to text
def listen(language_code="en-IN"):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Listening... Speak now.")
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
        text = r.recognize_google(audio, language=language_code)
        return text
    except Exception as e:
        return f"__ERROR__:{str(e)}"

# -- UI --
st.markdown("<style>body{background-color:#f6fff6;} .big{font-size:18px}</style>", unsafe_allow_html=True)
st.image("logo.png", width=140)
st.title("🌱 Krishi Sakhi")

# Language selection
lang = st.radio("Choose language / ഭാഷ തിരഞ്ഞെടുക്കുക", ["English", "മലയാളം"])
lang_code = "ml-IN" if lang == "മലയാളം" else "en-IN"

# Show small instructions translated
st.caption(tr("Use the 'Fetch GPS' button to auto-detect location. Allow location in your browser.", lang))

# GPS autofetch via HTML+JS: if coords not in query params, show JS button to fetch
query_params = st.experimental_get_query_params()
coords = query_params.get("coords", [None])[0]

st.markdown("---")
st.header(tr("Profile Setup", lang))

if not coords:
    st.write(tr("Step A: Auto-detect location (optional)", lang))
    gps_html = f"""
    <button onclick="getLoc()" style="background:#138000;color:white;padding:10px;border-radius:8px;border:none">📍 {tr('Fetch GPS', lang)}</button>
    <script>
    function getLoc(){{
      if (!navigator.geolocation) {{
        alert('Geolocation not supported');
        return;
      }}
      navigator.geolocation.getCurrentPosition(success, error);
      function success(position) {{
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const params = new URLSearchParams(window.location.search);
        params.set('coords', lat + ',' + lon);
        window.location.search = params.toString();
      }}
      function error(){{
        alert('Unable to fetch location or permission denied.');
      }}
    }}
    </script>
    """
    st.components.v1.html(gps_html, height=80)
else:
    # parse coords
    try:
        lat, lon = coords.split(",")
        st.success(tr(f"Location detected: {lat}, {lon}", lang))
    except:
        lat = lon = None

# Profile fields with voice prompts
st.subheader(tr("Basic Information", lang))
# Name
st.write(tr("Name", lang))
if st.button(tr("🎤 Speak Name", lang)):
    val = listen(lang_code)
    if val.startswith("__ERROR__"):
        st.error(tr("Speech recognition failed. Please type.", lang))
        name = st.text_input(tr("Enter your name", lang))
    else:
        name = val
        st.success(tr("Saved: ", lang) + name)
        speak(tr("Saved", lang), lang)
else:
    name = st.text_input(tr("Enter your name", lang))

# Mobile
st.write(tr("Mobile Number", lang))
if st.button(tr("🎤 Speak Mobile Number", lang)):
    val = listen(lang_code)
    if val.startswith("__ERROR__"):
        st.error(tr("Speech recognition failed. Please type.", lang))
        mobile = st.text_input(tr("Enter mobile number", lang))
    else:
        mobile = val
        st.success(tr("Saved: ", lang) + mobile)
else:
    mobile = st.text_input(tr("Enter mobile number", lang))

# Location field (manual or auto)
st.write(tr("Location (place name)", lang))
if st.button(tr("🎤 Speak Location", lang)):
    val = listen(lang_code)
    if val.startswith("__ERROR__"):
        st.error(tr("Speech recognition failed. Please type.", lang))
        place = st.text_input(tr("Enter place name", lang))
    else:
        place = val
        st.success(tr("Saved: ", lang) + place)
else:
    place = st.text_input(tr("Enter place name (if not auto-detected)", lang))

# Farm details
st.subheader(tr("Farm Details", lang))
if st.button(tr("🎤 Speak Land Size (acres)", lang)):
    val = listen(lang_code)
    if val.startswith("__ERROR__"):
        st.error(tr("Speech recognition failed. Please type.", lang))
        land_size = st.text_input(tr("Land size (in acres)", lang))
    else:
        land_size = val
        st.success(tr("Saved: ", lang) + land_size)
else:
    land_size = st.text_input(tr("Land size (in acres)", lang))

water = st.selectbox(tr("Water Source", lang), [tr("Well", lang), tr("Rain", lang), tr("Canal", lang), tr("Borewell", lang)])
irrig = st.selectbox(tr("Irrigation Method", lang), [tr("Drip", lang), tr("Sprinkler", lang), tr("Flood", lang)])
soil = st.selectbox(tr("Soil Type", lang), [tr("Clay", lang), tr("Sandy", lang), tr("Loamy", lang), tr("Laterite", lang)])

# Crop details
st.subheader(tr("Crop Details", lang))
st.write(tr("Select current crop", lang))
col1, col2, col3, col4 = st.columns(4)
current_crop = None
if col1.button("🌾 " + tr("Paddy", lang)):
    current_crop = "Paddy"
if col2.button("🍌 " + tr("Banana", lang)):
    current_crop = "Banana"
if col3.button("🥥 " + tr("Coconut", lang)):
    current_crop = "Coconut"
if col4.button("🥦 " + tr("Vegetables", lang)):
    current_crop = "Vegetables"

if st.button(tr("🎤 Speak Variety Name (or say none)", lang)):
    val = listen(lang_code)
    variety = val if not val.startswith("__ERROR__") else st.text_input(tr("Variety (or none)", lang))
else:
    variety = st.text_input(tr("Variety (or none)", lang))

sowing = st.date_input(tr("Date of sowing (leave if not applicable)", lang))
season = st.selectbox(tr("Season", lang), [tr("Kharif", lang), tr("Rabi", lang), tr("Summer", lang)])

# Preferences
st.subheader(tr("Preferences", lang))
farming_type = st.radio(tr("Farming Type", lang), [tr("Organic", lang), tr("Chemical", lang)])
comm = st.multiselect(tr("Preferred Communication Mode", lang), [tr("SMS", lang), tr("WhatsApp", lang), tr("Voice Call", lang)])
reminder = st.selectbox(tr("Reminders Preference", lang), [tr("Daily", lang), tr("Weekly", lang), tr("Only Critical Alerts", lang)])

# Submit and show profile summary
if st.button(tr("✅ Complete Profile", lang)):
    profile = {
        "name": name,
        "mobile": mobile,
        "coords": coords if coords else None,
        "place": place,
        "land_size_acres": land_size,
        "water_source": water,
        "irrigation_method": irrig,
        "soil_type": soil,
        "current_crop": current_crop,
        "variety": variety,
        "date_of_sowing": str(sowing),
        "season": season,
        "farming_type": farming_type,
        "communication_modes": comm,
        "reminder_pref": reminder,
        "created_at": datetime.utcnow().isoformat()
    }
    st.success(tr("Profile saved locally. You can export or proceed to dashboard.", lang))
    st.json(profile)
    # read back in chosen language
    summary = f"{tr('Saved profile for', lang)} {profile['name']}. {tr('Crop', lang)}: {profile['current_crop'] or tr('Not selected', lang)}. {tr('Land size', lang)}: {profile['land_size_acres']}."
    speak(summary, lang)
