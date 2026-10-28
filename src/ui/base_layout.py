import streamlit as st
import streamlit.components.v1 as components


# ---------------------------------------------------------------------------
# Theme initialiser – reads localStorage and sets data-theme on <html>.
# Must be called ONCE per page before other st.markdown calls.
# ---------------------------------------------------------------------------

def init_theme():
    """Inject JS that reads localStorage, respects OS preference, and sets
    data-theme on the parent document to prevent flash-of-wrong-theme."""

    if "theme" not in st.session_state:
        st.session_state["theme"] = "light"

    components.html(
        """
        <script>
        (function(){
            function applyTheme(theme){
                try {
                    window.parent.document.documentElement.setAttribute('data-theme', theme);
                } catch(e){}
            }
            var stored = null;
            try { stored = window.localStorage.getItem('snapclass_theme'); } catch(e){}
            var preferred = (window.matchMedia &&
                             window.matchMedia('(prefers-color-scheme: dark)').matches)
                            ? 'dark' : 'light';
            var theme = stored || preferred;
            applyTheme(theme);

            window.addEventListener('message', function(e){
                if(e.data && e.data.type === 'snapclass_set_theme'){
                    var t = e.data.theme;
                    try { window.localStorage.setItem('snapclass_theme', t); } catch(err){}
                    applyTheme(t);
                }
            });
        })();
        </script>
        """,
        height=0,
    )


# ---------------------------------------------------------------------------
# CSS variables – complete Warm Sand & Dusty Blue palette
# ---------------------------------------------------------------------------

_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

/* ── Light tokens (default) ──────────────────────────────────────── */
:root, html[data-theme="light"] {
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
}

/* ── Dark tokens ─────────────────────────────────────────────────── */
html[data-theme="dark"] {
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
</style>
"""


def _apply_css():
    st.markdown(_THEME_CSS, unsafe_allow_html=True)


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
# Main entry point – call on every screen
# ---------------------------------------------------------------------------

def style_base_layout():
    """Initialise theme (localStorage sync), inject all CSS tokens, and
    render the fixed top-right theme toggle button."""
    init_theme()
    _apply_css()
    _inject_fixed_toggle()


# ---------------------------------------------------------------------------
# Fixed top-right theme toggle (injected into the parent DOM via st.markdown)
# ---------------------------------------------------------------------------

def _inject_fixed_toggle():
    """
    Injects a permanently-visible, fixed-position sun/moon toggle button
    directly into the Streamlit page DOM (NOT inside an iframe), so it
    always sits in the top-right corner on every screen.
    """
    st.markdown("""
    <style>
    /* ── Fixed toggle pill ─────────────────────────────────────────── */
    #sc-theme-btn {
        position: fixed;
        top: 14px;
        right: 18px;
        z-index: 999999;
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: var(--bg-secondary);
        border: 1.5px solid var(--border-color);
        border-radius: 2rem;
        padding: 7px 16px;
        cursor: pointer;
        font-family: 'Outfit', 'Segoe UI', sans-serif;
        font-size: 13px;
        font-weight: 500;
        color: var(--text-secondary);
        box-shadow: var(--shadow);
        transition: background 0.2s ease, border-color 0.2s ease,
                    color 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
        outline: none;
        white-space: nowrap;
        letter-spacing: 0.01em;
    }
    #sc-theme-btn:hover {
        background: var(--color-accent);
        border-color: var(--color-primary);
        color: var(--text-primary);
        transform: scale(1.05);
        box-shadow: 0 4px 16px rgba(113, 139, 164, 0.25);
    }
    #sc-theme-btn:active { transform: scale(0.97); }
    #sc-theme-btn:focus-visible {
        outline: 2px solid var(--focus-ring);
        outline-offset: 3px;
    }
    #sc-theme-btn svg {
        flex-shrink: 0;
        transition: transform 0.4s ease;
    }
    #sc-theme-btn:hover svg { transform: rotate(20deg); }
    </style>

    <button id="sc-theme-btn" aria-label="Switch to dark mode" title="Toggle theme">
        <!-- Moon (shown in light mode) -->
        <svg id="sc-moon" xmlns="http://www.w3.org/2000/svg" width="15" height="15"
             viewBox="0 0 24 24" fill="currentColor">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
        <!-- Sun (shown in dark mode, hidden initially) -->
        <svg id="sc-sun" xmlns="http://www.w3.org/2000/svg" width="15" height="15"
             viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"
             style="display:none">
            <circle cx="12" cy="12" r="5"/>
            <line x1="12" y1="1" x2="12" y2="3"/>
            <line x1="12" y1="21" x2="12" y2="23"/>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
            <line x1="1" y1="12" x2="3" y2="12"/>
            <line x1="21" y1="12" x2="23" y2="12"/>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
        <span id="sc-lbl">Dark mode</span>
    </button>

    <script>
    (function () {
        var btn  = document.getElementById('sc-theme-btn');
        var moon = document.getElementById('sc-moon');
        var sun  = document.getElementById('sc-sun');
        var lbl  = document.getElementById('sc-lbl');
        var html = document.documentElement;

        function getTheme() {
            return html.getAttribute('data-theme') || 'light';
        }

        function applyUI(theme) {
            if (theme === 'dark') {
                moon.style.display = 'none';
                sun.style.display  = 'inline';
                lbl.textContent    = 'Light mode';
                btn.setAttribute('aria-label', 'Switch to light mode');
                btn.title = 'Switch to light mode';
            } else {
                moon.style.display = 'inline';
                sun.style.display  = 'none';
                lbl.textContent    = 'Dark mode';
                btn.setAttribute('aria-label', 'Switch to dark mode');
                btn.title = 'Switch to dark mode';
            }
        }

        function setTheme(theme) {
            html.setAttribute('data-theme', theme);
            try { window.localStorage.setItem('snapclass_theme', theme); } catch(e) {}
            applyUI(theme);
            // Broadcast into any component iframes so they can sync too
            try {
                document.querySelectorAll('iframe').forEach(function(f) {
                    try {
                        f.contentWindow.postMessage(
                            { type: 'snapclass_set_theme', theme: theme }, '*'
                        );
                    } catch(e) {}
                });
            } catch(e) {}
        }

        // Init from localStorage / OS preference
        var stored = null;
        try { stored = window.localStorage.getItem('snapclass_theme'); } catch(e) {}
        var preferred = (window.matchMedia &&
                         window.matchMedia('(prefers-color-scheme: dark)').matches)
                        ? 'dark' : 'light';
        var initial = stored || preferred;
        html.setAttribute('data-theme', initial);
        applyUI(initial);

        btn.addEventListener('click', function () {
            setTheme(getTheme() === 'light' ? 'dark' : 'light');
        });

        // Keyboard: Space / Enter already trigger click on <button>
        // Listen for theme changes from component iframes
        window.addEventListener('message', function (e) {
            if (e.data && e.data.type === 'snapclass_set_theme') {
                html.setAttribute('data-theme', e.data.theme);
                applyUI(e.data.theme);
            }
        });
    })();
    </script>
    """, unsafe_allow_html=True)


# Keep old name as no-op so existing import sites don't break
def theme_toggle():
    pass