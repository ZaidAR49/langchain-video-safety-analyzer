from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from video_safety.schemas import SafetyReport

load_dotenv()

DEFAULT_CATEGORIES = [
    "Alcohol & Drinking",
    "Smoking / Vaping / Drugs",
    "Gambling & Betting",
    "Profanity & Hate Speech",
    "Adult / Suggestive Content",
    "Violence / Dangerous Activities",
]


def analyze_video(
    video_url: str,
    categories: list[str] = None,
    sensitivity: str = "Strict",
    custom_notes: str = "",
    model_name: str = "gemini-3.5-flash-lite",
    language: str = "English",
) -> SafetyReport:
    cats = categories or DEFAULT_CATEGORIES
    categories_str = ", ".join(cats)

    lang_instr = (
        "Write summary, descriptions, and edits in Arabic (اللغة العربية)."
        if language in ("Arabic", "العربية")
        else "Write summary, descriptions, and edits in English."
    )

    system_prompt = (
        f"You are a Brand Safety Compliance Officer. Audit the video across: {categories_str}. "
        f"Sensitivity: {sensitivity}. Notes: {custom_notes}. {lang_instr} "
        "Return overall verdict (SAFE, CAUTION, FLAGGED), safety score (0-100), timestamps, violations, and recommended edits."
    )

    llm = ChatGoogleGenerativeAI(model=model_name or "gemini-3.5-flash-lite")
    chain = llm.with_structured_output(SafetyReport)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=[
                {"type": "media", "file_uri": video_url, "mime_type": "video/*"},
                {"type": "text", "text": "Audit this video for brand safety compliance."},
            ]
        ),
    ]

    return chain.invoke(messages)
