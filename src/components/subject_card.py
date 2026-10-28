import html as _html
import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    name = _html.escape(str(name))
    code = _html.escape(str(code))
    section = _html.escape(str(section))

    parts = [
        '<div style="background:var(--bg-card); border-left:5px solid var(--color-primary); padding:25px; border-radius:16px; border:1px solid var(--border-color); margin-bottom:20px; box-shadow:var(--shadow); transition:var(--transition, all 0.25s ease);">',
        f'<h3 style="margin:0; color:var(--text-primary); font-size:1.4rem">{name}</h3>',
        f'<p style="color:var(--text-secondary); margin:10px 0">Code : <span style="background:var(--color-accent); color:var(--text-primary); padding:2px 8px; border-radius:5px; font-weight:600">{code}</span> | Section: {section}</p>',
    ]

    if stats:
        parts.append('<div style="display:flex; gap:8px; flex-wrap:wrap;">')
        for icon, label, value in stats:
            parts.append(
                f'<div style="background:var(--bg-secondary); border:1px solid var(--border-color); padding:5px 12px; border-radius:12px; font-size:0.9rem; color:var(--text-primary)">'
                f'{icon} <b>{value}</b> {_html.escape(str(label))}</div>'
            )
        parts.append('</div>')

    parts.append('</div>')

    # single line, no indentation / blank lines, so markdown never turns it into a code block
    st.markdown("".join(parts), unsafe_allow_html=True)

    if footer_callback:
        footer_callback()

