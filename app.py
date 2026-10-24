"""
StyleScope + ToolWise - Streamlit Web Application
CSS Intelligence Studio and AI Agent Lab
"""
import streamlit as st
import os
import sys
import html

# Ensure src is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.css_parser import parse_css, result_to_json
from src.css_analyzer import analyze, generate_report, export_stats_json
from src.agent import Agent

# ---------------------------------------------------------------------------
# Page Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="StyleScope + ToolWise",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _inject_custom_styles():
    """Apply the shared visual theme to the Streamlit interface."""
    st.markdown(
        """
        <style>
        :root {
            --ink: #211b3d;
            --muted: #514b68;
            --violet: #4f46e5;
            --violet-deep: #3730a3;
            --purple: #7c3aed;
            --line: rgba(79, 70, 229, 0.16);
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(ellipse at 5% 0%, rgba(124, 58, 237, 0.10), transparent 34%),
                radial-gradient(ellipse at 95% 8%, rgba(79, 70, 229, 0.09), transparent 30%),
                linear-gradient(135deg, #f7f7ff 0%, #f1f2fb 54%, #fbf8ff 100%);
        }
        [data-testid="stHeader"] { background: rgba(247, 247, 255, 0.88); }
        [data-testid="stMainBlockContainer"] {
            max-width: 1280px;
            padding-top: 2.1rem;
            padding-right: clamp(1.25rem, 4vw, 3rem);
            padding-left: clamp(1.25rem, 4vw, 3rem);
            padding-bottom: 3rem;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(165deg, #17152f 0%, #292256 55%, #432879 100%);
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: #f4f2ff;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #e2ddff;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] > label {
            font-weight: 700;
            color: #ffffff;
        }
        [data-testid="stSidebar"] [role="radiogroup"] {
            gap: 0.45rem;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label {
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 0.55rem 0.7rem;
            background: rgba(255, 255, 255, 0.07);
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.14);
        }
        [data-testid="stMain"] {
            color: var(--ink);
        }
        [data-testid="stMain"] p,
        [data-testid="stMain"] li,
        [data-testid="stMain"] label,
        [data-testid="stMain"] [data-testid="stWidgetLabel"] {
            color: #302a49;
        }
        h1, h2, h3, h4 { color: var(--ink); letter-spacing: -0.025em; }
        h2, h3 { margin-top: 0.6rem; }
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p {
            color: #514b68;
        }

        .brand-lockup {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.45rem 0 0.8rem;
        }
        .brand-mark {
            display: grid;
            place-items: center;
            width: 2.65rem;
            height: 2.65rem;
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 14px;
            background: linear-gradient(145deg, #8b72ff, #34c9e8);
            box-shadow: 0 8px 24px rgba(19, 14, 57, 0.28);
            color: white;
            font-size: 1.35rem;
        }
        .brand-name { color: white; font-size: 1.02rem; font-weight: 800; }
        .brand-caption {
            margin-top: 0.12rem;
            color: #c4c9e7;
            font-size: 0.68rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }
        .hero-card {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1.5rem;
            overflow: hidden;
            margin: 0.25rem 0 1.7rem;
            padding: clamp(1.5rem, 4vw, 2.5rem);
            border: 1px solid rgba(255, 255, 255, 0.32);
            border-radius: 22px;
            background: linear-gradient(115deg, #3730a3 0%, #4f46e5 52%, #7c3aed 100%);
            box-shadow: 0 20px 52px rgba(67, 56, 202, 0.24), inset 0 1px 0 rgba(255,255,255,0.16);
            color: #ffffff;
        }
        .hero-card::after {
            position: absolute;
            top: -7rem;
            right: 9rem;
            width: 20rem;
            height: 20rem;
            border: 1px solid rgba(255, 255, 255, 0.13);
            border-radius: 50%;
            box-shadow: 0 0 0 2.4rem rgba(255, 255, 255, 0.035),
                        0 0 0 4.8rem rgba(255, 255, 255, 0.025);
            content: "";
            pointer-events: none;
        }
        .hero-copy { position: relative; z-index: 1; }
        .hero-copy { flex: 1; min-width: 0; }
        .hero-eyebrow {
            margin-bottom: 0.6rem;
            color: #f0edff;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }
        .hero-title {
            margin: 0;
            color: #ffffff;
            font-size: clamp(1.5rem, 2.5vw, 1.65rem);
            font-weight: 800;
            letter-spacing: -0.045em;
            line-height: 1.12;
        }
        [data-testid="stMain"] .hero-card h1.hero-title {
            font-size: clamp(1.5rem, 2.5vw, 1.65rem);
        }
        .hero-description {
            max-width: 42rem;
            margin: 0.65rem 0 0;
            color: #f4f2ff;
            font-size: 1rem;
            line-height: 1.6;
        }
        [data-testid="stMain"] .hero-description { color: #f4f2ff; }
        .hero-icon {
            position: relative;
            z-index: 1;
            display: grid;
            flex: 0 0 auto;
            place-items: center;
            width: clamp(4.25rem, 9vw, 5.75rem);
            height: clamp(4.25rem, 9vw, 5.75rem);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 20px;
            background: linear-gradient(145deg, rgba(255,255,255,0.22), rgba(255,255,255,0.09));
            box-shadow: 0 12px 26px rgba(30, 22, 91, 0.18), inset 0 1px 0 rgba(255,255,255,0.3);
            backdrop-filter: blur(10px);
        }
        .hero-icon svg {
            display: block;
            width: 58%;
            height: 58%;
            overflow: visible;
        }
        [data-testid="stTabs"] [role="tabpanel"] {
            margin-top: 0.75rem;
            padding: clamp(1rem, 2.4vw, 1.6rem);
            border: 1px solid rgba(255, 255, 255, 0.9);
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.78);
            box-shadow: 0 12px 34px rgba(42, 35, 90, 0.075);
            backdrop-filter: blur(14px);
        }
        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            gap: 0.45rem;
            border-bottom: 1px solid var(--line);
        }
        [data-testid="stTabs"] button[role="tab"] {
            height: 2.8rem;
            padding: 0 1rem;
            border-radius: 12px 12px 0 0;
            color: #514b68;
            font-weight: 700;
        }
        [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            background: linear-gradient(110deg, rgba(79, 70, 229, 0.14), rgba(124, 58, 237, 0.12));
            color: #3730a3;
        }
        [data-testid="stTabs"] button[role="tab"]:focus-visible,
        [data-testid="stSidebar"] [role="radiogroup"] label:focus-within {
            outline: 3px solid #a78bfa;
            outline-offset: 2px;
        }
        div.stButton > button {
            width: 100%;
            min-height: 2.65rem;
            border: 1px solid var(--line);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.94);
            color: #302a49;
            font-weight: 700;
            line-height: 1.35;
            text-align: left;
            white-space: normal;
            overflow-wrap: anywhere;
            box-shadow: 0 4px 14px rgba(39, 43, 85, 0.07);
            transition: all 160ms ease;
        }
        div.stButton > button:hover {
            border-color: rgba(79, 70, 229, 0.6);
            background: linear-gradient(110deg, #4f46e5, #7c3aed);
            color: #ffffff;
            transform: translateY(-1px);
        }
        div.stButton > button[kind="primary"] {
            border: 0;
            background: linear-gradient(110deg, #4f46e5, #7c3aed);
            color: #ffffff;
            box-shadow: 0 8px 22px rgba(79, 70, 229, 0.34), inset 0 1px 0 rgba(255,255,255,0.2);
        }
        [data-testid="stMain"] div.stButton > button[kind="primary"] p,
        [data-testid="stMain"] div.stButton > button[kind="primary"] span {
            color: #ffffff;
        }
        div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(110deg, #4338ca, #6d28d9);
            box-shadow: 0 10px 26px rgba(79, 70, 229, 0.42);
        }
        div.stButton > button:focus-visible {
            outline: 3px solid #a78bfa;
            outline-offset: 2px;
        }
        [data-testid="stMetric"] {
            min-height: 6rem;
            padding: 1.1rem 1.2rem;
            border: 1px solid rgba(79, 70, 229, 0.18);
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.94);
            box-shadow: 0 8px 22px rgba(39, 43, 85, 0.075);
            transition: transform 160ms ease, box-shadow 160ms ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 26px rgba(79, 70, 229, 0.13);
        }
        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p { color: #514b68; }
        [data-testid="stMetricValue"] { color: #30206f; }
        [data-testid="stTextArea"] textarea,
        [data-testid="stChatInput"] textarea {
            border: 1px solid rgba(79, 70, 229, 0.22);
            border-radius: 14px;
            background: #ffffff;
            color: #211b3d;
            caret-color: #4f46e5;
        }
        [data-testid="stTextArea"] textarea::placeholder,
        [data-testid="stChatInput"] textarea::placeholder {
            color: #625b78;
            opacity: 1;
        }
        [data-testid="stChatInput"] {
            margin-top: 0.75rem;
            padding: 0.35rem;
            border: 1px solid rgba(79, 70, 229, 0.24);
            border-radius: 18px;
            background: linear-gradient(135deg, #ffffff, #faf9ff);
            box-shadow: 0 10px 26px rgba(55, 48, 163, 0.11),
                        inset 0 1px 0 rgba(255, 255, 255, 0.95);
            transition: border-color 160ms ease, box-shadow 160ms ease;
        }
        [data-testid="stChatInput"]:focus-within {
            border-color: rgba(79, 70, 229, 0.72);
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.12),
                        0 12px 28px rgba(55, 48, 163, 0.13);
        }
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInput"] textarea {
            border: 0 !important;
            border-radius: 14px;
            background: transparent !important;
            box-shadow: none !important;
        }
        [data-testid="stChatInput"] textarea {
            min-height: 3.25rem;
            padding: 0.85rem 0.9rem;
            color: #211b3d;
            font-size: 0.97rem;
            line-height: 1.5;
        }
        [data-testid="stChatInput"] button {
            width: 2.85rem;
            height: 2.85rem;
            margin-right: 0.2rem;
            border: 0;
            border-radius: 13px;
            background: linear-gradient(110deg, #4f46e5, #7c3aed);
            color: #ffffff;
            box-shadow: 0 5px 14px rgba(79, 70, 229, 0.26);
            transition: transform 160ms ease, box-shadow 160ms ease,
                        background 160ms ease;
        }
        [data-testid="stChatInput"] button:hover:not(:disabled) {
            transform: translateY(-1px);
            background: linear-gradient(110deg, #4338ca, #6d28d9);
            box-shadow: 0 7px 18px rgba(79, 70, 229, 0.34);
        }
        [data-testid="stChatInput"] button:disabled {
            background: linear-gradient(110deg, #756cf0, #9564ea);
            color: #ffffff;
            opacity: 0.78;
            box-shadow: none;
        }
        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stChatInput"] textarea:focus {
            border-color: #4f46e5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.16);
        }
        [data-testid="stFileUploader"],
        [data-testid="stExpander"] {
            border: 1px solid rgba(79, 70, 229, 0.18);
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.9);
        }
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {
            border: 1px dashed rgba(79, 70, 229, 0.46);
            border-radius: 12px;
            background: linear-gradient(135deg, #f5f3ff, #eef2ff);
            color: #302a49;
        }
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] button {
            border: 0;
            border-radius: 10px;
            background: linear-gradient(110deg, #4f46e5, #7c3aed);
            color: #ffffff;
            box-shadow: 0 5px 14px rgba(79, 70, 229, 0.24);
        }
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] button:hover {
            background: linear-gradient(110deg, #4338ca, #6d28d9);
            color: #ffffff;
        }
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] button p,
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] button span,
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] button [data-testid="stIconMaterial"] {
            color: #ffffff !important;
            fill: currentColor;
        }
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"],
        [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"] span {
            color: #514b68 !important;
        }
        [data-testid="stChatMessage"] {
            border: 1px solid rgba(79, 70, 229, 0.14);
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.92);
            color: #211b3d;
        }
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
            color: #211b3d;
        }
        [data-testid="stAlert"] {
            border: 1px solid rgba(79, 70, 229, 0.2);
            border-radius: 12px;
            box-shadow: 0 5px 16px rgba(39, 43, 85, 0.06);
        }
        [data-testid="stAlert"] p,
        [data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
            color: #211b3d;
        }
        [data-testid="stCode"],
        [data-testid="stJson"] {
            border: 1px solid rgba(167, 139, 250, 0.28);
            border-radius: 12px;
            background: #17152b;
            color: #f4f2ff;
            box-shadow: 0 8px 22px rgba(23, 21, 43, 0.16);
        }
        [data-testid="stCode"] code,
        [data-testid="stJson"] * {
            color: #f4f2ff;
        }
        .report-card {
            margin: 0.7rem 0 0;
            padding: clamp(1rem, 2vw, 1.5rem);
            border: 1px solid rgba(79, 70, 229, 0.16);
            border-left: 4px solid #4f46e5;
            border-radius: 14px;
            background: #ffffff;
            box-shadow: 0 8px 24px rgba(39, 43, 85, 0.06);
            color: #211b3d;
        }
        .report-card pre {
            margin: 0;
            overflow-x: auto;
            background: transparent;
            color: #211b3d;
            font-family: "Cascadia Code", "Consolas", monospace;
            font-size: 0.88rem;
            line-height: 1.75;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
        }
        .result-section-heading {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            margin: 0 0 0.45rem;
            color: #211b3d;
            font-size: 1.2rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }
        .result-section-heading::before {
            width: 0.35rem;
            height: 1.35rem;
            border-radius: 999px;
            background: linear-gradient(180deg, #4f46e5, #7c3aed);
            content: "";
        }
        .result-section-description {
            margin: 0 0 1rem;
            color: #514b68;
            font-size: 0.9rem;
            line-height: 1.55;
        }
        .variables-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
            gap: 0.85rem;
            margin: 1rem 0 1.4rem;
        }
        .variable-card {
            min-width: 0;
            padding: 1rem 1.1rem;
            border: 1px solid rgba(79, 70, 229, 0.18);
            border-radius: 14px;
            background: linear-gradient(145deg, #ffffff, #f7f6ff);
            box-shadow: 0 6px 18px rgba(39, 43, 85, 0.055);
        }
        .variable-name {
            display: inline-block;
            margin-bottom: 0.55rem;
            padding: 0.25rem 0.55rem;
            border: 1px solid rgba(79, 70, 229, 0.16);
            border-radius: 7px;
            background: #eeecff;
            color: #3730a3;
            font-family: "Cascadia Code", "Consolas", monospace;
            font-size: 0.8rem;
            font-weight: 700;
            overflow-wrap: anywhere;
        }
        .variable-value {
            display: block;
            color: #211b3d;
            font-family: "Cascadia Code", "Consolas", monospace;
            font-size: 0.95rem;
            font-weight: 700;
            overflow-wrap: anywhere;
        }
        .variable-source {
            display: block;
            margin-top: 0.5rem;
            color: #514b68;
            font-size: 0.76rem;
        }
        .st-key-chat_panel [data-testid="stChatMessage"] {
            max-width: 100%;
        }
        .st-key-agent_tool_selector {
            margin: 0 0 1.15rem;
            padding: 0.9rem 1.1rem;
            border: 1px solid rgba(79, 70, 229, 0.18);
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.88);
            box-shadow: 0 8px 22px rgba(39, 43, 85, 0.055);
        }
        .st-key-agent_tool_selector [data-testid="stRadio"] > label {
            margin-bottom: 0.35rem;
            color: #3730a3;
            font-weight: 800;
        }
        .st-key-agent_tool_selector [data-testid="stRadio"] [role="radiogroup"] {
            gap: 0.5rem;
        }
        .st-key-agent_tool_selector input[type="radio"] {
            accent-color: #4f46e5;
        }
        .tool-description-card {
            min-height: 4.8rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 0.75rem 1rem;
            border-left: 3px solid #7c3aed;
            border-radius: 0 12px 12px 0;
            background: linear-gradient(110deg, #f5f3ff, #f8f7ff);
        }
        .tool-description-title {
            margin: 0 0 0.2rem;
            color: #3730a3;
            font-size: 0.9rem;
            font-weight: 800;
        }
        .tool-description-copy {
            margin: 0;
            color: #514b68;
            font-size: 0.82rem;
            line-height: 1.45;
        }
        .st-key-agent_activity {
            margin-top: 0.9rem;
            padding: 0.65rem 0.85rem;
            border: 1px solid rgba(79, 70, 229, 0.16);
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.78);
        }
        .st-key-agent_activity [data-testid="stButton"] button {
            text-align: center;
        }
        .st-key-live_text_stats {
            margin: 0.4rem 0 0.85rem;
        }
        .st-key-live_text_stats [data-testid="stMetric"] {
            min-height: 4.6rem;
            padding: 0.65rem 0.85rem;
            border-radius: 12px;
            box-shadow: none;
        }
        .st-key-live_text_stats [data-testid="stMetricValue"] {
            font-size: 1.3rem;
        }
        .st-key-chat_panel [data-testid="stChatMessage"] pre {
            padding: 0.85rem 1rem;
            border: 1px solid rgba(167, 139, 250, 0.28);
            border-radius: 12px;
            background: #17152b;
            color: #f4f2ff;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
        }
        .st-key-chat_panel [data-testid="stChatMessage"] pre code {
            color: #f4f2ff;
        }
        [data-testid="stJson"] {
            padding: 0.85rem;
            overflow-x: auto;
        }
        [data-testid="stVegaLiteChart"] svg {
            border-radius: 12px;
            background-color: #ffffff !important;
        }
        [data-testid="stVegaLiteChart"] svg text {
            fill: #302a49 !important;
        }
        [data-testid="stVegaLiteChart"] svg line {
            stroke: #d6d3e1 !important;
        }
        [data-testid="stVegaLiteChart"] svg path[fill="#83c9ff"] {
            fill: #4f46e5 !important;
        }
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            border: 1px solid rgba(79, 70, 229, 0.16);
            border-radius: 12px;
            overflow: hidden;
        }
        .st-key-chat_panel,
        .st-key-analysis_results {
            border: 1px solid rgba(79, 70, 229, 0.2) !important;
            border-radius: 18px !important;
            background: rgba(255, 255, 255, 0.82);
            box-shadow: 0 12px 30px rgba(39, 43, 85, 0.075);
        }
        .results-heading {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin: 0 0 1.15rem;
            padding: 1.1rem 1.25rem;
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 16px;
            background: linear-gradient(110deg, #312e81 0%, #4f46e5 55%, #7c3aed 100%);
            box-shadow: 0 12px 28px rgba(79, 70, 229, 0.2);
            color: #ffffff;
        }
        .results-heading-icon {
            display: grid;
            flex: 0 0 auto;
            place-items: center;
            width: 2.8rem;
            height: 2.8rem;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.15);
        }
        .results-heading-icon svg { width: 1.55rem; height: 1.55rem; }
        .results-heading-copy { flex: 1; min-width: 0; }
        .results-heading-title {
            margin: 0;
            color: #ffffff;
            font-size: 1.08rem;
            font-weight: 800;
        }
        .results-heading-subtitle {
            margin: 0.2rem 0 0;
            color: #f1efff;
            font-size: 0.84rem;
        }
        [data-testid="stMain"] .results-heading p.results-heading-title { color: #ffffff; }
        [data-testid="stMain"] .results-heading p.results-heading-subtitle { color: #f1efff; }
        .results-status {
            flex: 0 0 auto;
            padding: 0.35rem 0.7rem;
            border: 1px solid rgba(255, 255, 255, 0.32);
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.14);
            color: #ffffff;
            font-size: 0.76rem;
            font-weight: 800;
        }
        [data-testid="stChatMessage"] {
            box-shadow: 0 6px 18px rgba(39, 43, 85, 0.055);
        }
        [data-testid="column"] > div[data-testid="stVerticalBlock"] {
            border-radius: 14px;
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                scroll-behavior: auto !important;
                transition-duration: 0.01ms !important;
                animation-duration: 0.01ms !important;
            }
        }
        @media (max-width: 640px) {
            [data-testid="stMainBlockContainer"] { padding-top: 1rem; }
            .hero-card { border-radius: 18px; padding: 1.35rem; }
            .hero-icon { border-radius: 17px; }
            [data-testid="stTabs"] [role="tabpanel"] { padding: 1rem; }
            .results-heading { flex-wrap: wrap; gap: 0.7rem; }
            .results-status { margin-left: 3.5rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_hero(icon, eyebrow, title, description):
    st.markdown(
        f"""
        <section class="hero-card">
            <div class="hero-copy">
                <div class="hero-eyebrow">{eyebrow}</div>
                <h1 class="hero-title">{title}</h1>
                <p class="hero-description">{description}</p>
            </div>
            <div class="hero-icon" aria-hidden="true">{icon}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _submit_text_analysis():
    """Add the text editor contents to the chat and run the selected analysis tool."""
    text = st.session_state.get("text_analysis_input", "").strip()
    if not text:
        return

    st.session_state.chat_history.append({"role": "user", "content": text})
    response = st.session_state.agent.process(f"analyze text: {text}")
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response["response_text"]}
    )
    st.session_state.text_analysis_input = ""


def _display_css_results(result, stats, report):
    """Display CSS analysis results in tabs."""
    status = "Needs review" if stats.error_count else "Analysis ready"
    st.markdown(
        f"""
        <div class="results-heading">
            <div class="results-heading-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="m5 12.5 4.2 4.2L19 7" stroke="white" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 2.8a9.2 9.2 0 1 0 0 18.4 9.2 9.2 0 0 0 0-18.4Z" stroke="white" stroke-width="1.7"/>
                </svg>
            </div>
            <div class="results-heading-copy">
                <p class="results-heading-title">CSS analysis results</p>
                <p class="results-heading-subtitle">Explore the summary, rules, report, and export.</p>
            </div>
            <span class="results-status">{status}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True, key="analysis_results"):
        r1, r2, r3, r4 = st.tabs(["Summary", "Text Report", "Variables & Rules", "JSON Export"])

        with r1:
            st.markdown(
                '<p class="result-section-heading">At a glance</p>'
                '<p class="result-section-description">A clear breakdown of the stylesheet structure and any parse issues.</p>',
                unsafe_allow_html=True,
            )
            metrics = [
                ("Rules", stats.rule_count),
                ("Selectors", stats.selector_count),
                ("Declarations", stats.declaration_count),
                ("At-Rules", stats.at_rule_count),
                ("Media Queries", stats.media_query_count),
                ("Keyframes", stats.keyframe_count),
                ("CSS Variables", stats.variable_count),
                ("Comments", stats.comment_count),
                ("Parse Errors", stats.error_count),
            ]
            metric_columns = st.columns(2, gap="medium")
            for index, (label, value) in enumerate(metrics):
                with metric_columns[index % 2]:
                    st.metric(label, value)

            if stats.most_used_properties:
                st.subheader("Top Properties")
                prop_data = {p: c for p, c in stats.most_used_properties}
                st.bar_chart(prop_data)

        with r2:
            st.markdown(
                '<p class="result-section-heading">Readable text report</p>'
                '<p class="result-section-description">A print-friendly summary of the stylesheet analysis.</p>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="report-card"><pre>{html.escape(report)}</pre></div>',
                unsafe_allow_html=True,
            )

        with r3:
            st.markdown(
                '<p class="result-section-heading">Variables &amp; rules</p>'
                '<p class="result-section-description">Inspect extracted design tokens, declarations, and parser feedback.</p>',
                unsafe_allow_html=True,
            )
            if result.variables:
                st.markdown(
                    '<p class="result-section-description"><strong>CSS variables</strong></p>',
                    unsafe_allow_html=True,
                )
                variable_cards = []
                for var in result.variables:
                    source_line = (
                        f"Line {var.source_line}"
                        if var.source_line is not None
                        else "Source line unavailable"
                    )
                    variable_cards.append(
                        f'<article class="variable-card">'
                        f'<span class="variable-name">{html.escape(str(var.name))}</span>'
                        f'<strong class="variable-value">{html.escape(str(var.value))}</strong>'
                        f'<small class="variable-source">{source_line}</small>'
                        f'</article>'
                    )
                st.markdown(
                    f'<div class="variables-grid">{"".join(variable_cards)}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.info("No CSS custom properties were found.")

            if result.rules:
                st.markdown(
                    '<p class="result-section-description"><strong>Parsed rules</strong></p>',
                    unsafe_allow_html=True,
                )
                for rule in result.rules:
                    with st.expander(", ".join(rule.selectors)):
                        for decl in rule.declarations:
                            imp = " !important" if decl.important else ""
                            st.code(f"{decl.property}: {decl.value}{imp};", language="css")

            if result.errors:
                st.markdown(
                    '<p class="result-section-description"><strong>Parse issues</strong></p>',
                    unsafe_allow_html=True,
                )
                for err in result.errors:
                    st.error(f"[Line {err.source_line}] {err.message}")

        with r4:
            st.markdown(
                '<p class="result-section-heading">Structured JSON export</p>'
                '<p class="result-section-description">Copy or inspect the machine-readable parser output and summary statistics.</p>',
                unsafe_allow_html=True,
            )
            st.markdown("**Parse result**")
            st.code(result_to_json(result), language="json")
            st.markdown("**Analysis statistics**")
            st.code(export_stats_json(stats), language="json")


_inject_custom_styles()

# ---------------------------------------------------------------------------
# Session State
# ---------------------------------------------------------------------------
if "agent" not in st.session_state:
    st.session_state.agent = Agent(base_dir=os.path.dirname(os.path.abspath(__file__)))

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.markdown(
    """
    <div class="brand-lockup">
        <div class="brand-mark">✦</div>
        <div>
            <div class="brand-name">StyleScope</div>
            <div class="brand-caption">Creative toolkit</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
workspace = st.sidebar.radio(
    "WORKSPACE",
    ["CSS Intelligence Studio", "AI Agent Lab"],
)
st.sidebar.markdown(
    "<p style='margin-top:1.2rem;font-size:0.82rem;'>"
    "✨ Analyze stylesheets or explore your smart tool lab.</p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# CSS Intelligence Studio
# ---------------------------------------------------------------------------
if workspace == "CSS Intelligence Studio":
    _render_hero(
        '<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 8h17l12 12v36H20V8Z" stroke="white" stroke-width="3.2" stroke-linejoin="round"/><path d="M37 9v12h12M27 32h15M27 40h15M27 48h10" stroke="white" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><path d="m13 16-1.5 3.5L8 21l3.5 1.5L13 26l1.5-3.5L18 21l-3.5-1.5L13 16Z" fill="#C4B5FD"/></svg>',
        "STYLESCOPE",
        "CSS Intelligence Studio",
        "Turn any stylesheet into clear insights. Parse rules, explore variables, "
        "and generate a detailed report in seconds.",
    )

    tab1, tab2 = st.tabs(["Paste CSS", "Upload File"])

    with tab1:
        st.subheader("Paste CSS Code")
        css_input = st.text_area(
            "Enter CSS code here:",
            height=300,
            placeholder=":root { --primary: #6c63ff; }\nbody { margin: 0; color: var(--primary); }",
        )
        if st.button("✨ Analyze Pasted CSS", key="analyze_paste", type="primary"):
            if css_input.strip():
                with st.spinner("Parsing CSS..."):
                    result = parse_css(css_input)
                    stats = analyze(result)
                    report = generate_report(result, stats, title="CSS Analysis — Pasted Code")
                _display_css_results(result, stats, report)
            else:
                st.warning("Please paste some CSS code first.")

    with tab2:
        st.subheader("Upload a CSS File")
        uploaded_file = st.file_uploader("Choose a CSS file", type=["css", "txt"])
        if uploaded_file is not None:
            css_content = uploaded_file.read().decode("utf-8")
            st.code(css_content[:1000] + ("..." if len(css_content) > 1000 else ""), language="css")
            if st.button("✨ Analyze Uploaded File", key="analyze_upload", type="primary"):
                with st.spinner("Parsing CSS..."):
                    result = parse_css(css_content)
                    stats = analyze(result)
                    report = generate_report(result, stats, title=f"CSS Analysis — {uploaded_file.name}")
                _display_css_results(result, stats, report)

# ---------------------------------------------------------------------------
# AI Agent Lab
# ---------------------------------------------------------------------------
elif workspace == "AI Agent Lab":
    _render_hero(
        '<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M32 10v7" stroke="white" stroke-width="3.2" stroke-linecap="round"/><circle cx="32" cy="7" r="3" fill="#C4B5FD"/><rect x="12" y="19" width="40" height="34" rx="11" stroke="white" stroke-width="3.2"/><path d="M21 34a4 4 0 1 0 8 0 4 4 0 0 0-8 0ZM35 34a4 4 0 1 0 8 0 4 4 0 0 0-8 0Z" fill="white"/><path d="M24 44c2.2 2.2 4.8 3.3 8 3.3s5.8-1.1 8-3.3" stroke="#DDD6FE" stroke-width="3" stroke-linecap="round"/><path d="M7 29v13M57 29v13" stroke="white" stroke-width="3.2" stroke-linecap="round"/></svg>',
        "TOOLWISE",
        "AI Agent Lab",
        "Your focused assistant for quick calculations and clear text insights.",
    )

    with st.container(key="agent_tool_selector"):
        selector_column, description_column = st.columns(
            [1, 1.55], vertical_alignment="center"
        )
        with selector_column:
            selected_tool = st.radio(
                "Choose a tool",
                ["Calculator", "Text Analysis"],
                horizontal=True,
                key="agent_tool_choice",
            )
        if selected_tool == "Calculator":
            description_title = "Calculator"
            description = (
                "Ask a math question or enter an expression. Supports +, -, *, /, %, "
                "powers, and parentheses."
            )
        else:
            description_title = "Text Analysis"
            description = (
                "Paste text and see live word, character, and line counts before "
                "running an analysis."
            )
        with description_column:
            st.markdown(
                f"""
                <div class="tool-description-card">
                    <p class="tool-description-title">{description_title}</p>
                    <p class="tool-description-copy">{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with st.container(border=True, key="chat_panel"):
        st.subheader("ToolWise Assistant")
        for msg in st.session_state.chat_history:
            role = msg["role"]
            content = msg["content"]
            st.chat_message(role).write(content)

        if selected_tool == "Calculator":
            user_input = st.chat_input(
                "Enter a calculation or math question...",
                key="calculator_chat_input",
            )
            if user_input:
                st.session_state.chat_history.append(
                    {"role": "user", "content": user_input}
                )
                with st.spinner("Working with the selected tool..."):
                    response = st.session_state.agent.process(user_input)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": response["response_text"]}
                )
                st.rerun()
        else:
            analysis_text = st.text_area(
                "Text to analyze",
                key="text_analysis_input",
                height=130,
                placeholder="Paste text here, or ask a question about it...",
            )
            word_count = len(analysis_text.split())
            line_count = len(analysis_text.splitlines()) if analysis_text else 0
            with st.container(key="live_text_stats"):
                word_metric, character_metric, line_metric = st.columns(3)
                word_metric.metric("Words", word_count)
                character_metric.metric("Characters", len(analysis_text))
                line_metric.metric("Lines", line_count)
            st.button(
                "Analyze text",
                key="analyze_text_input",
                type="primary",
                disabled=not analysis_text.strip(),
                on_click=_submit_text_analysis,
            )

    with st.container(key="agent_activity"):
        history = st.session_state.agent.get_history_summary()
        history_column, clear_column = st.columns(
            [3, 1], vertical_alignment="center"
        )
        with history_column:
            if history:
                with st.expander("Recent tool activity"):
                    for entry in reversed(history[-5:]):
                        status = "✅" if entry["success"] else "❌"
                        st.markdown(
                            f"{status} **{entry['tool_used']}** — "
                            f"`{entry['request'][:60]}`"
                        )
            else:
                st.caption("Your recent tool activity will appear here.")
        with clear_column:
            if st.button("Clear conversation", key="clear_chat"):
                st.session_state.chat_history = []
                st.session_state.agent.clear_history()
                st.rerun()
