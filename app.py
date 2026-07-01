import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO

st.set_page_config(
    page_title="Language Translator",
    page_icon="🌐",
    layout="centered",
)

LANGUAGES = {
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "it": "Italian", "pt": "Portuguese", "nl": "Dutch", "ru": "Russian",
    "zh-CN": "Chinese (Simplified)", "ja": "Japanese", "ko": "Korean",
    "ar": "Arabic", "hi": "Hindi", "bn": "Bengali", "pa": "Punjabi",
    "ur": "Urdu", "tr": "Turkish", "vi": "Vietnamese", "th": "Thai",
    "pl": "Polish", "sv": "Swedish", "el": "Greek", "he": "Hebrew",
    "id": "Indonesian", "uk": "Ukrainian", "fa": "Persian", "ta": "Tamil",
    "te": "Telugu", "ms": "Malay", "ro": "Romanian",
}

# gTTS uses slightly different codes for a couple of languages
GTTS_CODE_OVERRIDES = {"zh-CN": "zh-CN", "he": "iw"}

CUSTOM_CSS = """
<style>
    .stApp { background-color: #F6F2E9; }
    h1 { color: #1F4B4A; font-weight: 700; }
    .stButton>button {
        background-color: #E2572B;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.6rem 1.6rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .stButton>button:hover { background-color: #c94a23; color: white; }
    .swap-button>button {
        background-color: #1F4B4A;
        border-radius: 50%;
        width: 44px;
        height: 44px;
        padding: 0;
    }
    .swap-button>button:hover { background-color: #E2572B; }
    div[data-testid="stTextArea"] textarea { font-size: 1.05rem; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "source_lang" not in st.session_state:
    st.session_state.source_lang = "en"
if "target_lang" not in st.session_state:
    st.session_state.target_lang = "es"
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

st.title("🌐 Language Translator")
st.caption("Type text, choose your languages, and translate instantly.")

lang_codes = list(LANGUAGES.keys())
lang_names = list(LANGUAGES.values())

col1, col_swap, col2 = st.columns([5, 1, 5])

with col1:
    source_lang = st.selectbox(
        "Source language",
        options=lang_codes,
        format_func=lambda code: LANGUAGES[code],
        index=lang_codes.index(st.session_state.source_lang),
        key="source_select",
    )
    input_text = st.text_area(
        "Enter text",
        value=st.session_state.input_text,
        height=220,
        max_chars=4000,
        placeholder="Begin writing here...",
        key="input_area",
    )
    st.caption(f"{len(input_text)} / 4000 characters")

with col_swap:
    st.markdown("<div style='height: 38px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="swap-button">', unsafe_allow_html=True)
    if st.button("⇄", key="swap_btn", help="Swap languages"):
        st.session_state.source_lang = st.session_state.target_lang
        st.session_state.target_lang = source_lang
        if st.session_state.translated_text:
            st.session_state.input_text = st.session_state.translated_text
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    target_lang = st.selectbox(
        "Target language",
        options=lang_codes,
        format_func=lambda code: LANGUAGES[code],
        index=lang_codes.index(st.session_state.target_lang),
        key="target_select",
    )
    output_placeholder = st.empty()
    if st.session_state.translated_text:
        output_placeholder.text_area(
            "Translation",
            value=st.session_state.translated_text,
            height=220,
            disabled=True,
            key="output_area",
        )
    else:
        output_placeholder.text_area(
            "Translation",
            value="",
            height=220,
            disabled=True,
            placeholder="Your translation will appear here.",
            key="output_area_empty",
        )
    if st.session_state.translated_text:
        st.caption(f"{len(st.session_state.translated_text)} characters")

st.session_state.source_lang = source_lang
st.session_state.target_lang = target_lang
st.session_state.input_text = input_text

st.write("")
_, mid, _ = st.columns([2, 2, 2])
with mid:
    translate_clicked = st.button("Get Translation →", use_container_width=True)

if translate_clicked:
    text = input_text.strip()
    if not text:
        st.warning("Write something first.")
    elif source_lang == target_lang:
        st.session_state.translated_text = text
        st.info("Source and target are the same language.")
        st.rerun()
    else:
        with st.spinner("Translating..."):
            try:
                translated = GoogleTranslator(
                    source=source_lang, target=target_lang
                ).translate(text)
                st.session_state.translated_text = translated
                st.rerun()
            except Exception as e:
                st.error(f"Translation failed: {e}")

if st.session_state.translated_text:
    st.write("")
    col_copy, col_listen_src, col_listen_tgt = st.columns(3)

    with col_copy:
        st.code(st.session_state.translated_text, language=None)
        st.caption("Click the copy icon above to copy the translation")

    with col_listen_src:
        if st.button("🔊 Listen to source", use_container_width=True):
            try:
                tts = gTTS(
                    text=st.session_state.input_text,
                    lang=GTTS_CODE_OVERRIDES.get(source_lang, source_lang),
                )
                buf = BytesIO()
                tts.write_to_fp(buf)
                buf.seek(0)
                st.audio(buf, format="audio/mp3")
            except Exception as e:
                st.warning(f"Couldn't generate audio for this language: {e}")

    with col_listen_tgt:
        if st.button("🔊 Listen to translation", use_container_width=True):
            try:
                tts = gTTS(
                    text=st.session_state.translated_text,
                    lang=GTTS_CODE_OVERRIDES.get(target_lang, target_lang),
                )
                buf = BytesIO()
                tts.write_to_fp(buf)
                buf.seek(0)
                st.audio(buf, format="audio/mp3")
            except Exception as e:
                st.warning(f"Couldn't generate audio for this language: {e}")

st.write("")
st.divider()
st.caption("Powered by Google Translate (via deep-translator) · Text-to-speech via gTTS")
