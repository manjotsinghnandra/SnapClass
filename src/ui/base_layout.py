import streamlit as st


# ---------------------------------------------------------------------------
# Theme handling
#
# The old toggle was an HTML <button> + <script> passed to st.markdown.
# Streamlit strips <script> tags from markdown, so the button never had a
# click handler. The toggle is now a real Streamlit button that flips
# st.session_state["theme"]; the matching CSS tokens are rendered server-side
# on every run, so it works on every screen and survives reruns.
# ---------------------------------------------------------------------------

_LIGHT_TOKENS = """
    --bg-main:            #F8F6F1;
    --bg-card:            #FFFFFF;
    --bg-secondary:       #EBE6DC;
    --color-primary:      #718BA4;
    --color-primary-hover:#5D7892;
    --color-accent:       #B8C9D7;
    --text-primary:       #303B46;
    --text-secondary:     #65717A;
    --border-color:       #E5E0D6;
    --focus-ring:         #718BA4;

    --present-bg:   #E3F0E6; --present-text: #326B48;
    --absent-bg:    #F5E5E2; --absent-text:  #9B514A;
    --late-bg:      #F7EED9; --late-text:    #8C692B;
    --pending-bg:   #E6EDF3; --pending-text: #526F8A;

    --shadow:       0 2px 12px rgba(48, 59, 70, 0.08);
    --shadow-card:  0 4px 20px rgba(48, 59, 70, 0.07);
    --transition:   background-color 0.25s ease, color 0.25s ease,
                    border-color 0.25s ease, box-shadow 0.25s ease;
"""

_DARK_TOKENS = """
    --bg-main:            #171C22;
    --bg-card:            #222A33;
    --bg-secondary:       #2B343E;
    --color-primary:      #8FAAC2;
    --color-primary-hover:#A8BED1;
    --color-accent:       #303E4C;
    --text-primary:       #F0EEE8;
    --text-secondary:     #B4BDC6;
    --border-color:       #343C45;
    --focus-ring:         #A8BED1;

    --present-bg:   #244033; --present-text: #A4D7B4;
    --absent-bg:    #482D2D; --absent-text:  #F0AAA2;
    --late-bg:      #493D26; --late-text:    #E8C77E;
    --pending-bg:   #303E4C; --pending-text: #B8C9D7;

    --shadow:       0 2px 12px rgba(0,0,0,0.35);
    --shadow-card:  0 4px 20px rgba(0,0,0,0.30);
    --transition:   background-color 0.25s ease, color 0.25s ease,
                    border-color 0.25s ease, box-shadow 0.25s ease;
"""

_BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

:root {
    --transition: background-color 0.25s ease, color 0.25s ease,
                  border-color 0.25s ease, box-shadow 0.25s ease;
    /*__TOKENS__*/
}

/* ── Global base ─────────────────────────────────────────────────── */
html, body, .stApp {
    transition: var(--transition) !important;
}
.stApp {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

/* hide Streamlit chrome */
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 5rem !important; }

/* ── Typography ──────────────────────────────────────────────────── */
h1 {
    font-family: 'Climate Crisis', sans-serif !important;
    font-size: 3.5rem !important;
    line-height: 1.1 !important;
    margin-bottom: 0rem !important;
    color: var(--text-primary) !important;
}
h2 {
    font-family: 'Climate Crisis', sans-serif !important;
    font-size: 2rem !important;
    line-height: 0.9 !important;
    margin-bottom: 0rem !important;
    color: var(--text-primary) !important;
}
h3, h4, p, label {
    font-family: 'Outfit', sans-serif !important;
    color: var(--text-primary) !important;
}

/* ── Buttons ─────────────────────────────────────────────────────── */
button[kind="primary"],
button[data-testid="baseButton-primary"] {
    border-radius: 1.5rem !important;
    background-color: var(--color-primary) !important;
    color: var(--bg-card) !important;
    padding: 10px 20px !important;
    border: none !important;
    font-family: 'Outfit', sans-serif !important;
    transition: transform 0.25s ease-in-out, background-color 0.2s ease !important;
}
button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    background-color: var(--color-primary-hover) !important;
    transform: scale(1.03) !important;
}

button[kind="secondary"],
button[data-testid="baseButton-secondary"] {
    border-radius: 1.5rem !important;
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    padding: 10px 20px !important;
    border: 1.5px solid var(--border-color) !important;
    font-family: 'Outfit', sans-serif !important;
    transition: transform 0.25s ease-in-out, background-color 0.2s ease !important;
}
button[kind="secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover {
    background-color: var(--color-accent) !important;
    transform: scale(1.03) !important;
}

button[kind="tertiary"],
button[data-testid="baseButton-tertiary"] {
    border-radius: 1.5rem !important;
    background-color: transparent !important;
    color: var(--text-secondary) !important;
    padding: 10px 20px !important;
    border: 1.5px solid var(--border-color) !important;
    font-family: 'Outfit', sans-serif !important;
    transition: transform 0.25s ease-in-out, background-color 0.2s ease !important;
}
button[kind="tertiary"]:hover,
button[data-testid="baseButton-tertiary"]:hover {
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    transform: scale(1.03) !important;
}

button:focus-visible {
    outline: 2px solid var(--focus-ring) !important;
    outline-offset: 2px !important;
}

/* ── Inputs ──────────────────────────────────────────────────────── */
input, textarea,
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
    font-family: 'Outfit', sans-serif !important;
    transition: var(--transition) !important;
}
div[data-baseweb="input"]:focus-within,
div[data-baseweb="textarea"]:focus-within {
    border-color: var(--focus-ring) !important;
}
.stTextInput label, .stSelectbox label,
.stTextArea label, .stNumberInput label, .stFileUploader label {
    color: var(--text-secondary) !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── Selectbox / Dropdowns ───────────────────────────────────────── */
div[data-baseweb="select"] {
    background-color: var(--bg-card) !important;
    border-color: var(--border-color) !important;
}
div[data-baseweb="select"] div {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
}
div[data-baseweb="popover"], div[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
}
ul[role="listbox"] li { color: var(--text-primary) !important; }
ul[role="listbox"] li:hover,
ul[role="listbox"] li[aria-selected="true"] {
    background-color: var(--bg-secondary) !important;
}

/* ── Dividers ────────────────────────────────────────────────────── */
hr { border-color: var(--border-color) !important; }

/* ── Dataframe / Tables ──────────────────────────────────────────── */
.stDataFrame, [data-testid="stDataFrame"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
.stDataFrame thead th {
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    font-family: 'Outfit', sans-serif !important;
}
.stDataFrame tbody tr:nth-child(even) {
    background-color: var(--bg-secondary) !important;
}
.stDataFrame tbody td {
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── Alerts ──────────────────────────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid var(--border-color) !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── Dialogs ─────────────────────────────────────────────────────── */
div[data-testid="stModal"] > div,
div[role="dialog"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    box-shadow: var(--shadow-card) !important;
}

/* ── Bordered containers ─────────────────────────────────────────── */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    box-shadow: var(--shadow) !important;
    transition: var(--transition) !important;
}

/* ── Camera / Audio inputs ───────────────────────────────────────── */
div[data-testid="stCameraInput"],
div[data-testid="stAudioInput"] {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-color) !important;
}

/* ── Toast ───────────────────────────────────────────────────────── */
div[data-testid="stToast"] {
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
}

/* ── Code blocks ─────────────────────────────────────────────────── */
.stCode, code, pre {
    background-color: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}

/* ── Theme toggle (fixed, top-right) ─────────────────────────────── */
.st-key-theme_toggle {
    position: fixed !important;
    top: 14px;
    right: 18px;
    z-index: 999999;
    width: auto !important;
}
.st-key-theme_toggle button {
    padding: 7px 16px !important;
    font-size: 13px !important;
    box-shadow: var(--shadow) !important;
}
</style>
"""


def _default_theme():
    """Follow the browser/Streamlit theme on first load, else light."""
    try:
        if st.context.theme.type == "dark":
            return "dark"
    except Exception:
        pass
    return "light"


def _flip_theme():
    st.session_state["theme"] = "dark" if st.session_state.get("theme") == "light" else "light"


def init_theme():
    if "theme" not in st.session_state:
        st.session_state["theme"] = _default_theme()


def _apply_css():
    tokens = _DARK_TOKENS if st.session_state["theme"] == "dark" else _LIGHT_TOKENS
    st.markdown(_BASE_CSS.replace("/*__TOKENS__*/", tokens), unsafe_allow_html=True)


def theme_toggle():
    is_dark = st.session_state["theme"] == "dark"
    st.button(
        "Light mode" if is_dark else "Dark mode",
        key="theme_toggle",
        icon=":material/light_mode:" if is_dark else ":material/dark_mode:",
        type="secondary",
        on_click=_flip_theme,
        help="Switch to light mode" if is_dark else "Switch to dark mode",
    )


# ---------------------------------------------------------------------------
# Screen-specific backgrounds
# ---------------------------------------------------------------------------

def style_background_home():
    st.markdown("""
        <style>
        .stApp { background-color: var(--bg-main) !important; }
        .stApp div[data-testid="stColumn"] {
            background-color: var(--bg-card) !important;
            padding: 3rem !important;
            border-radius: 2rem !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: var(--shadow-card) !important;
            transition: var(--transition) !important;
        }
        </style>
    """, unsafe_allow_html=True)


def style_base_dashboard():
    st.markdown("""
        <style>
        .stApp { background-color: var(--bg-main) !important; }
        </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Main entry point - call ONCE per run on every screen
# ---------------------------------------------------------------------------

def style_base_layout():
    """Initialise theme state, inject CSS tokens, render the theme toggle."""
    init_theme()
    _apply_css()
    theme_toggle()
