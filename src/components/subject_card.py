import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style="background:white; border-left: 8px solid #EB459E; padding: 25px; border-radius: 20px; border: 1px solid black; margin-bottom: 20px;">

        <h3 style="margin=0; color:#1e293b; font-size:1.5rem">{name}</h3>
        <p style="color:#64784b; margin:10px 0">Code : <span style:"background:#E0E3FF; color:#5865F2; padding:2px 8px; border-radius:5px"> {code} </span> | Section: {section}</p>
        """

    if stats:
        html+="""
        <div style="display: flex; gap:8px; flex-wrap:wrap;">
        """
        for icon, label, value in stats:
            html+= f'<div style="background: #EB459E10; padding: 5px 12px; border-radius: 12px; font-size:0.9rem">{icon} <b>{value}</b> {label} </div>'

            html+="</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()







# import streamlit as st
# import textwrap


# def subject_card(
#     name,
#     code,
#     section,
#     stats=None,
#     footer_callback=None,
#     accent_color="#EB459E",
# ):
#   # Advanced modern CSS styling with transitions, soft gradients, and shadows
#   card_html = textwrap.dedent(
#       f"""
#     <style>
#         .custom-subject-card {{
#             background: linear-gradient(135deg, #ffffff 0%, #fcfdfe 100%);
#             border-left: 6px solid {accent_color};
#             padding: 22px 26px;
#             border-radius: 16px;
#             box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
#             border-top: 1px solid #f1f5f9;
#             border-right: 1px solid #f1f5f9;
#             border-bottom: 1px solid #f1f5f9;
#             margin-bottom: 20px;
#             transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
#         }}
#         .custom-subject-card:hover {{
#             transform: translateY(-3px);
#             box-shadow: 0 16px 32px -6px rgba(235, 69, 158, 0.12), 0 10px 15px -5px rgba(0, 0, 0, 0.05);
#             border-color: #e2e8f0;
#         }}
#     </style>

#     <div class="custom-subject-card">
#         <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;">
#             <div>
#                 <h3 style="margin: 0 0 6px 0; color: #0f172a; font-size: 1.35rem; font-weight: 700; letter-spacing: -0.01em;">{name}</h3>
#                 <div style="display: flex; align-items: center; gap: 8px; font-size: 0.9rem; color: #64748b;">
#                     <span style="background: #f8fafc; border: 1px solid #e2e8f0; color: #334155; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-family: monospace; font-size: 0.85rem;">{code}</span>
#                     <span style="color: #cbd5e1;">•</span>
#                     <span>Section: <strong style="color: #334155; font-weight: 600;">{section}</strong></span>
#                 </div>
#             </div>
#         </div>
#     """
#   )

#   # Render stats badges horizontally
#   if stats:
#     stats_html = (
#         '<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top:'
#         ' 16px; padding-top: 14px; border-top: 1px dashed #f1f5f9;">'
#     )
#     for icon, label, value in stats:
#       stats_html += (
#           f'<div style="background: #f8fafc; border: 1px solid #e2e8f0;'
#           f' padding: 6px 12px; border-radius: 10px; font-size: 0.85rem; color:'
#           f' #475569; display: inline-flex; align-items: center; gap: 6px;'
#           f' transition: background 0.2s;"><span style="font-size:'
#           f' 1rem;">{icon}</span> <b style="color: #0f172a; font-weight:'
#           f' 600;">{value}</b> <span style="color: #64748b; font-weight:'
#           f' 400;">{label}</span></div>'
#       )
#     stats_html += "</div>"
#     card_html += stats_html

#   card_html += "</div>"

#   st.markdown(card_html, unsafe_allow_html=True)

#   if footer_callback:
#     footer_callback()







# import streamlit as st
# import textwrap


# def subject_card(
#     name,
#     code,
#     section,
#     stats=None,
#     footer_callback=None,
#     accent_color="#EB459E",
# ):
#   card_html = textwrap.dedent(
#       f"""
#     <style>
#         .premium-card {{
#             background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
#             border: 1px solid #e2e8f0;
#             border-left: 5px solid {accent_color};
#             padding: 24px 28px;
#             border-radius: 18px;
#             box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.04), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
#             margin-bottom: 20px;
#             transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
#             position: relative;
#             overflow: hidden;
#         }}
#         .premium-card::after {{
#             content: '';
#             position: absolute;
#             top: 0;
#             right: 0;
#             width: 100px;
#             height: 100px;
#             background: radial-gradient(circle, {accent_color}08 0%, transparent 70%);
#             pointer-events: none;
#         }}
#         .premium-card:hover {{
#             transform: translateY(-4px);
#             box-shadow: 0 20px 40px -10px {accent_color}20, 0 10px 15px -5px rgba(0, 0, 0, 0.05);
#             border-color: {accent_color}40;
#         }}
#     </style>

#     <div class="premium-card">
#         <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 16px;">
#             <div>
#                 <h3 style="margin: 0 0 8px 0; color: #0f172a; font-size: 1.4rem; font-weight: 700; letter-spacing: -0.02em;">{name}</h3>
#                 <div style="display: flex; align-items: center; gap: 10px; font-size: 0.9rem;">
#                     <span style="background: #ffffff; border: 1px solid #cbd5e1; color: #1e293b; padding: 3px 10px; border-radius: 6px; font-weight: 600; font-family: monospace; font-size: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">{code}</span>
#                     <span style="color: #94a3b8;">•</span>
#                     <span style="color: #64748b;">Section <strong style="color: #334155; font-weight: 600;">{section}</strong></span>
#                 </div>
#             </div>
#         </div>
#     """
#   )

#   if stats:
#     stats_html = (
#         '<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top:'
#         ' 18px; padding-top: 16px; border-top: 1px solid #edf2f7;">'
#     )
#     for icon, label, value in stats:
#       stats_html += (
#           f'<div style="background: #ffffff; border: 1px solid #e2e8f0;'
#           f' padding: 6px 14px; border-radius: 12px; font-size: 0.85rem; color:'
#           f' #475569; display: inline-flex; align-items: center; gap: 8px;'
#           f' box-shadow: 0 1px 3px rgba(0,0,0,0.02);"><span style="font-size:'
#           f' 1.05rem;">{icon}</span> <b style="color: #0f172a; font-weight:'
#           f' 700;">{value}</b> <span style="color: #64748b; font-weight:'
#           f' 400;">{label}</span></div>'
#       )
#     stats_html += "</div>"
#     card_html += stats_html

#   card_html += "</div>"

#   st.markdown(card_html, unsafe_allow_html=True)

#   if footer_callback:
#     footer_callback()








# import streamlit as st
# import textwrap


# def subject_card(
#     name,
#     code,
#     section,
#     stats=None,
#     footer_callback=None,
#     accent_color="#EB459E",
# ):
#   card_html = textwrap.dedent(
#       f"""
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

#         .pinnacle-card-wrapper {{
#             font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
#             background: linear-gradient(135deg, #ffffff 0%, #fcfdfe 100%);
#             border: 1px solid rgba(226, 232, 240, 0.8);
#             border-left: 6px solid {accent_color};
#             padding: 26px 30px;
#             border-radius: 20px;
#             box-shadow: 0 12px 40px -10px rgba(15, 23, 42, 0.06), 0 4px 12px -2px rgba(15, 23, 42, 0.03);
#             margin-bottom: 22px;
#             transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
#             position: relative;
#             overflow: hidden;
#         }}

#         .pinnacle-card-wrapper::before {{
#             content: '';
#             position: absolute;
#             top: -50px;
#             right: -50px;
#             width: 160px;
#             height: 160px;
#             background: radial-gradient(circle, {accent_color}12 0%, transparent 70%);
#             pointer-events: none;
#             transition: transform 0.4s ease;
#         }}

#         .pinnacle-card-wrapper:hover {{
#             transform: translateY(-5px);
#             box-shadow: 0 24px 50px -12px {accent_color}25, 0 12px 20px -6px rgba(15, 23, 42, 0.08);
#             border-color: {accent_color}60;
#         }}

#         .pinnacle-card-wrapper:hover::before {{
#             transform: scale(1.3) translate(-10px, 10px);
#         }}

#         .pinnacle-title {{
#             margin: 0 0 8px 0;
#             color: #0f172a;
#             font-size: 1.45rem;
#             font-weight: 800;
#             letter-spacing: -0.03em;
#             line-height: 1.2;
#         }}

#         .pinnacle-meta {{
#             display: flex;
#             align-items: center;
#             gap: 12px;
#             font-size: 0.92rem;
#         }}

#         .pinnacle-code-badge {{
#             background: #f8fafc;
#             border: 1px solid #e2e8f0;
#             color: #1e293b;
#             padding: 4px 10px;
#             border-radius: 8px;
#             font-weight: 700;
#             font-family: monospace;
#             font-size: 0.82rem;
#             box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);
#             letter-spacing: 0.02em;
#         }}

#         .pinnacle-stats-container {{
#             display: flex;
#             gap: 10px;
#             flex-wrap: wrap;
#             margin-top: 20px;
#             padding-top: 16px;
#             border-top: 1px dashed #e2e8f0;
#         }}

#         .pinnacle-stat-pill {{
#             background: #f8fafc;
#             border: 1px solid #e2e8f0;
#             padding: 7px 14px;
#             border-radius: 12px;
#             font-size: 0.85rem;
#             color: #475569;
#             display: inline-flex;
#             align-items: center;
#             gap: 8px;
#             box-shadow: 0 2px 4px rgba(0,0,0,0.01);
#             transition: all 0.2s ease;
#         }}

#         .pinnacle-stat-pill:hover {{
#             background: #ffffff;
#             border-color: {accent_color}50;
#             transform: translateY(-1px);
#         }}
#     </style>

#     <div class="pinnacle-card-wrapper">
#         <div>
#             <h3 class="pinnacle-title">{name}</h3>
#             <div class="pinnacle-meta">
#                 <span class="pinnacle-code-badge">{code}</span>
#                 <span style="color: #cbd5e1; font-weight: 300;">•</span>
#                 <span style="color: #64748b;">Section <strong style="color: #1e293b; font-weight: 700;">{section}</strong></span>
#             </div>
#         </div>
#     """
#   )

#   if stats:
#     stats_html = '<div class="pinnacle-stats-container">'
#     for icon, label, value in stats:
#       # Single-line string to prevent markdown code block rendering bugs
#       stats_html += f'<div class="pinnacle-stat-pill"><span style="font-size: 1.1rem; line-height: 1;">{icon}</span><b style="color: #0f172a; font-weight: 700;">{value}</b><span style="color: #64748b; font-weight: 500;">{label}</span></div>'
#     stats_html += "</div>"
#     card_html += stats_html

#   card_html += "</div>"

#   st.markdown(card_html, unsafe_allow_html=True)

#   if footer_callback:
#     footer_callback()