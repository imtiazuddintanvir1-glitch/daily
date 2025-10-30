import streamlit as st
import pandas as pd
import datetime as dt
import json
import yaml

# ---------- Load feedback rules ----------
@st.cache_data
def load_rules(path="feedback_rules.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------- Feedback logic ----------
def generate_feedback(entry: str, rules: dict, lang: str = "ja") -> str:
    entry_lower = entry.lower()
    for rule in rules["rules"]:
        if any(word in entry_lower for word in rule["keywords"]):
            return rule["feedback"].get(lang, "")
    return rules["default"]["feedback"].get(lang, "")

# ---------- Initialize ----------
def init():
    if "entries" not in st.session_state:
        st.session_state.entries = []

# ---------- UI ----------
def main():
    st.set_page_config(page_title="Daily Reflection Journal", page_icon="🌿", layout="centered")
    init()
    rules = load_rules()

    st.title("🌿 Daily Reflection Journal / 日々のふりかえり")
    st.caption("Write about your day and receive gentle encouragement.")

    date = st.date_input("Date / 日付", dt.date.today())
    reflection = st.text_area("How was your day? / 今日どんな一日でしたか？", height=200)

    lang = st.segmented_control("Language / 言語", ["ja", "en"], default="ja")

    if st.button("💬 Get Feedback / フィードバックを見る"):
        fb = generate_feedback(reflection, rules, lang)
        st.success(fb)
        st.session_state.entries.append({
            "date": str(date),
            "reflection": reflection,
            "feedback_ja": generate_feedback(reflection, rules, "ja"),
            "feedback_en": generate_feedback(reflection, rules, "en"),
        })

    if st.session_state.entries:
        st.divider()
        st.subheader("📘 My Reflections / マイ日記")
        df = pd.DataFrame(st.session_state.entries)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Download
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("Download CSV / CSVをダウンロード", csv, "reflections.csv", "text/csv")

if __name__ == "__main__":
    main()
