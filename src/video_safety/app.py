"""Streamlit Web UI for Video Brand Safety & Compliance Analyzer.

Provides bilingual (English & Arabic) auditing of YouTube videos
using LangChain LCEL and Google Gemini.
"""

import json
import importlib
import streamlit as st
import video_safety.schemas as schemas_module
import video_safety.analyzer as analyzer_module

# Reload modules on rerun to ensure updated function signatures
importlib.reload(schemas_module)
importlib.reload(analyzer_module)

from video_safety.analyzer import analyze_video, DEFAULT_CATEGORIES
from video_safety.schemas import SafetyReport

# Page configuration
st.set_page_config(
    page_title="Brand Safety & Compliance Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Multilingual UI Dictionary (English & Arabic)
UI_TEXT = {
    "English": {
        "title": "🛡️ Video Brand Safety & Compliance Analyzer",
        "subtitle": "Audit public YouTube videos for sponsor suitability, brand safety guidelines, and advertiser compliance.",
        "sidebar_lang": "🌐 Language / اللغة",
        "sidebar_title": "🛡️ Audit Settings",
        "sidebar_caption": "Powered by **LangChain LCEL** & **Google Gemini**",
        "categories_header": "🎯 Sensitive Categories",
        "policy_header": "⚙️ Policy Severity",
        "sensitivity_label": "Sensitivity Threshold",
        "sensitivity_options": ["Lenient", "Moderate", "Strict"],
        "model_label": "Gemini Model",
        "concepts_title": "🧠 LangChain Capabilities",
        "concepts_body": """
* **Multimodal Reasoning**: Gemini inspects the YouTube video stream directly.
* **Structured Output**: `.with_structured_output(SafetyReport)` ensures validated Pydantic schema output.
* **LCEL Composition**: Clean chaining of prompts and structured model output.
""",
        "url_label": "YouTube Video URL:",
        "notes_label": "Optional Sponsor Context or Custom Instructions:",
        "notes_placeholder": "e.g. Sponsoring family-friendly brand, strictly no alcohol mentions.",
        "audit_button": "🔍 Run Brand Safety Audit",
        "audit_warning_no_cat": "Please select at least one sensitive category in the sidebar.",
        "audit_warning_no_url": "Please enter a YouTube video URL above to analyze.",
        "spinner_text": "🤖 Gemini is watching & analyzing video streams for compliance violations...",
        "results_header": "📊 Compliance Audit Results",
        "card_verdict": "Overall Verdict",
        "card_score": "Safety Score",
        "card_violations": "Violations Logged",
        "summary_header": "📝 Executive Summary",
        "table_header": "⏱️ Timestamped Incident Log",
        "no_violations": "🎉 No policy violations detected! Video is clean.",
        "recommendations_header": "✂️ Actionable Recommendations for Editors",
        "no_recommendations": "No edits required. Video is ready for publication or sponsorship.",
        "raw_json_header": "🛠️ View Raw Structured Pydantic Output (JSON)",
        "download_button": "📥 Download Audit Report (JSON)",
        "verdict_safe": "SAFE",
        "verdict_caution": "CAUTION",
        "verdict_flagged": "FLAGGED",
        "col_timestamp": "Timestamp",
        "col_category": "Category",
        "col_severity": "Severity",
        "col_description": "Description",
    },
    "العربية": {
        "title": "🛡️ أداة فحص ومطابقة أمان العلامة التجارية للفيديو",
        "subtitle": "فحص وتحليل مقاطع يوتيوب للتحقق من ملاءمتها للإعلانات والرعاية ومطابقتها لمعايير أمان العلامة التجارية.",
        "sidebar_lang": "🌐 اللغة / Language",
        "sidebar_title": "🛡️ إعدادات الفحص",
        "sidebar_caption": "مدعوم بواسطة **LangChain LCEL** و **Google Gemini**",
        "categories_header": "🎯 الفئات الحساسة المستهدفة",
        "policy_header": "⚙️ صرامة السياسة",
        "sensitivity_label": "مستوى التدقيق والحساسية",
        "sensitivity_options": ["مرن", "متوسط", "صارم"],
        "model_label": "نموذج Gemini",
        "concepts_title": "🧠 قدرات LangChain",
        "concepts_body": """
* **الاستدلال متعدد الوسائط**: قيام نموذج Gemini بفحص محتوى الفيديو مباشرة.
* **المخرجات المهيكلة**: تطبيق `.with_structured_output(SafetyReport)` لضمان مخرجات Pydantic مطابقة بدقة.
* **لغة التعبير LCEL**: ربط سلس للموجهات والنموذج المهيكل.
""",
        "url_label": "رابط مقطع يوتيوب (YouTube Video URL):",
        "notes_label": "ملاحظات إضافية أو تعليمات خاصة بالراعي (اختياري):",
        "notes_placeholder": "مثال: رعاية لعلامة تجارية عائلية، يمنع ذكر الكحول تماماً.",
        "audit_button": "🔍 بدء فحص أمان الفيديو",
        "audit_warning_no_cat": "يرجى تحديد فئة حساسة واحدة على الأقل من القائمة الجانبية.",
        "audit_warning_no_url": "يرجى إدخال رابط فيديو يوتيوب أعلاه لبدء الفحص.",
        "spinner_text": "🤖 يقوم Gemini بمشاهدة وتحليل الفيديو للتحقق من المخالفات ومعايير الأمان...",
        "results_header": "📊 نتائج تقرير الفحص والامتثال",
        "card_verdict": "الحكم النهائي",
        "card_score": "درجة الأمان",
        "card_violations": "المخالفات المرصودة",
        "summary_header": "📝 التقرير التنفيذي",
        "table_header": "⏱️ سجل الحوادث والمخالفات الزمني",
        "no_violations": "🎉 لم يتم رصد أي مخالفات! محتوى الفيديو آمن تماماً.",
        "recommendations_header": "✂️ توصيات وتعديلات مقترحة للمحررين",
        "no_recommendations": "لا توجد تعديلات مطلوبة. الفيديو جاهز للنشر والرعاية الإعلانية.",
        "raw_json_header": "🛠️ عرض بيانات المخرجات المهيكلة الأصلية (JSON)",
        "download_button": "📥 تحميل تقرير الفحص (JSON)",
        "verdict_safe": "آمن (SAFE)",
        "verdict_caution": "تحذير (CAUTION)",
        "verdict_flagged": "مخالف / غير آمن (FLAGGED)",
        "col_timestamp": "التوقيت",
        "col_category": "الفئة",
        "col_severity": "مستوى الخطورة",
        "col_description": "الوصف والملابسات",
    },
}

# Category labels with bilingual mapping
CATEGORIES_MAPPING = {
    "Alcohol & Drinking": {"en": "Alcohol & Drinking", "ar": "الكحول والمشروبات", "emoji": "🍺"},
    "Smoking / Vaping / Drugs": {"en": "Smoking / Vaping / Drugs", "ar": "التدخين / الشيشة / المخدرات", "emoji": "🚬"},
    "Gambling & Betting": {"en": "Gambling & Betting", "ar": "القمار والمراهنات", "emoji": "🎲"},
    "Profanity & Hate Speech": {"en": "Profanity & Hate Speech", "ar": "الألفاظ النابية وخطاب الكراهية", "emoji": "🤬"},
    "Adult / Suggestive Content": {"en": "Adult / Suggestive Content", "ar": "محتوى للبالغين / غير لائق", "emoji": "🔞"},
    "Violence / Dangerous Activities": {"en": "Violence / Dangerous Activities", "ar": "العنف والأنشطة الخطرة", "emoji": "⚔️"},
}

SEVERITY_TRANSLATION_AR = {
    "LOW": "منخفض (LOW)",
    "MEDIUM": "متوسط (MEDIUM)",
    "HIGH": "مرتفع (HIGH)",
    "CRITICAL": "حرج (CRITICAL)",
}


def apply_custom_styles(is_arabic: bool):
    """Injects CSS styling with RTL support if Arabic is selected."""
    rtl_css = """
    body, .stApp, [data-testid="stSidebar"], [data-testid="stMarkdownContainer"] {
        direction: rtl;
        text-align: right;
    }
    .stTextInput input, .stTextArea textarea {
        direction: rtl;
        text-align: right;
    }
    .recommendation-pill {
        border-left: none !important;
        border-right: 4px solid #3b82f6 !important;
        text-align: right;
    }
    pre, code {
        direction: ltr !important;
        text-align: left !important;
    }
    """ if is_arabic else ""

    st.markdown(
        f"""
        <style>
        .metric-card {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            text-align: {'right' if is_arabic else 'left'};
        }}
        
        .verdict-badge {{
            display: inline-block;
            padding: 8px 18px;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 1.1rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}
        
        .badge-safe {{
            background-color: rgba(16, 185, 129, 0.2);
            color: #10b981;
            border: 1px solid #10b981;
        }}
        
        .badge-caution {{
            background-color: rgba(245, 158, 11, 0.2);
            color: #f59e0b;
            border: 1px solid #f59e0b;
        }}
        
        .badge-flagged {{
            background-color: rgba(239, 68, 68, 0.2);
            color: #ef4444;
            border: 1px solid #ef4444;
        }}

        .recommendation-pill {{
            background: rgba(59, 130, 246, 0.15);
            border-left: 4px solid #3b82f6;
            padding: 10px 14px;
            margin: 6px 0;
            border-radius: 4px;
            font-size: 0.95rem;
        }}

        {rtl_css}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Renders configuration controls and returns selected settings."""
    # Language selector at top of sidebar
    selected_lang = st.sidebar.radio(
        "🌐 Language / اللغة",
        options=["English", "العربية"],
        horizontal=True,
    )
    is_arabic = selected_lang == "العربية"
    t = UI_TEXT[selected_lang]

    st.sidebar.markdown("---")
    st.sidebar.title(t["sidebar_title"])
    st.sidebar.caption(t["sidebar_caption"])

    st.sidebar.markdown("---")
    st.sidebar.subheader(t["categories_header"])

    selected_categories = []
    for default_cat, mapping in CATEGORIES_MAPPING.items():
        label = f"{mapping['emoji']} {mapping['ar'] if is_arabic else mapping['en']}"
        checked = st.sidebar.checkbox(label, value=True, key=f"cat_{default_cat}")
        if checked:
            selected_categories.append(default_cat)

    st.sidebar.markdown("---")
    st.sidebar.subheader(t["policy_header"])

    sensitivity_idx = st.sidebar.select_slider(
        t["sensitivity_label"],
        options=[0, 1, 2],
        value=2,
        format_func=lambda i: t["sensitivity_options"][i],
    )
    raw_sensitivity = ["Lenient", "Moderate", "Strict"][sensitivity_idx]

    model_choice = st.sidebar.selectbox(
        t["model_label"],
        options=["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.8-flash"],
        index=0,
    )

    st.sidebar.markdown("---")
    with st.sidebar.expander(t["concepts_title"], expanded=False):
        st.markdown(t["concepts_body"])

    return selected_lang, is_arabic, t, selected_categories, raw_sensitivity, model_choice


def main():
    """Main application loop."""
    selected_lang, is_arabic, t, selected_categories, sensitivity, model_choice = render_sidebar()

    # Apply typography & RTL styles
    apply_custom_styles(is_arabic)

    st.title(t["title"])
    st.markdown(t["subtitle"])

    # URL Input Field
    video_url = st.text_input(
        t["url_label"],
        value="",
        placeholder="https://www.youtube.com/watch?v=...",
    )

    custom_notes = st.text_input(
        t["notes_label"],
        placeholder=t["notes_placeholder"],
    )

    # Video Preview (if URL entered)
    if video_url.strip():
        st.video(video_url.strip())

    analyze_clicked = st.button(
        t["audit_button"],
        type="primary",
        use_container_width=True,
        disabled=len(selected_categories) == 0,
    )

    if len(selected_categories) == 0:
        st.warning(t["audit_warning_no_cat"])
    elif not video_url.strip() and analyze_clicked:
        st.warning(t["audit_warning_no_url"])

    # Results Section
    if analyze_clicked and video_url.strip():
        with st.spinner(t["spinner_text"]):
            try:
                report: SafetyReport = analyze_video(
                    video_url=video_url.strip(),
                    categories=selected_categories,
                    sensitivity=sensitivity,
                    custom_notes=custom_notes or "Perform standard brand safety evaluation.",
                    model_name=model_choice,
                    language=selected_lang,
                )
                st.session_state["last_report"] = report
                st.session_state["report_lang"] = selected_lang
            except Exception as e:
                st.error(f"Error: {e}")
                return

    if "last_report" in st.session_state:
        report: SafetyReport = st.session_state["last_report"]

        st.markdown("---")
        st.header(t["results_header"])

        # Metric Summary Cards
        score = report.safety_score
        verdict = report.overall_verdict

        badge_class = (
            "badge-safe" if verdict == "SAFE"
            else ("badge-caution" if verdict == "CAUTION" else "badge-flagged")
        )
        badge_icon = (
            "✅" if verdict == "SAFE"
            else ("⚠️" if verdict == "CAUTION" else "🚫")
        )
        verdict_display = (
            t["verdict_safe"] if verdict == "SAFE"
            else (t["verdict_caution"] if verdict == "CAUTION" else t["verdict_flagged"])
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>{t["card_verdict"]}</h4>
                    <span class="verdict-badge {badge_class}">{badge_icon} {verdict_display}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            score_color = '#10b981' if score >= 80 else ('#f59e0b' if score >= 50 else '#ef4444')
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>{t["card_score"]}</h4>
                    <h2 style="margin: 0; color: {score_color}">{score} / 100</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>{t["card_violations"]}</h4>
                    <h2 style="margin: 0;">{len(report.violations)}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Executive Summary
        st.subheader(t["summary_header"])
        st.info(report.summary)

        # Timestamped Incidents Table
        st.subheader(t["table_header"])
        if report.violations:
            table_data = [
                {
                    t["col_timestamp"]: v.timestamp,
                    t["col_category"]: v.category,
                    t["col_severity"]: SEVERITY_TRANSLATION_AR.get(v.severity, v.severity) if is_arabic else v.severity,
                    t["col_description"]: v.description,
                }
                for v in report.violations
            ]
            st.dataframe(table_data, use_container_width=True)
        else:
            st.success(t["no_violations"])

        # Actionable Recommendations
        st.subheader(t["recommendations_header"])
        if report.recommended_edits:
            for edit in report.recommended_edits:
                st.markdown(f"<div class='recommendation-pill'>📌 {edit}</div>", unsafe_allow_html=True)
        else:
            st.write(t["no_recommendations"])

        # Raw JSON Export
        with st.expander(t["raw_json_header"], expanded=False):
            json_str = report.model_dump_json(indent=2)
            st.code(json_str, language="json")
            st.download_button(
                t["download_button"],
                data=json_str,
                file_name="brand_safety_report.json",
                mime="application/json",
            )


if __name__ == "__main__":
    main()
