# ==========================================
# AI Lecture Voice-to-Notes Generator
# Created By: Savitri Kumari
# ==========================================

import streamlit as st
import whisper
import tempfile
import os
from collections import Counter
import pandas as pd


# ===== FFMPEG PATH =====
os.environ["PATH"] += os.pathsep + r"D:\ffmpeg\ffmpeg-8.1.1-essentials_build\bin"

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="AI Lecture Assistant",
    page_icon="🎙️",
    layout="wide"
)

# ===== CUSTOM STYLE =====
st.markdown("""
<style>
.stButton>button{
    width:100%;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    theme = st.toggle("🌙 Dark Mode")
    st.header("👤 About")
    st.write("**Savitri Kumari**")
    st.write("🎙 AI Lecture Assistant")
    st.write("🚀 Internship Project")
    st.write("---")
    st.write("Convert lecture audio into study notes instantly.")

# ===== MAIN HEADER =====
st.markdown("""
<h1 style='text-align:center;'>🎙️ AI Lecture Assistant</h1>
<h3 style='text-align:center;'>Convert Audio → Transcript → Notes</h3>
""", unsafe_allow_html=True)

st.caption(
    "🎓 Upload any lecture audio and instantly generate transcript, insights and study notes."
)

# ===== AUDIO UPLOAD =====
audio_file = st.file_uploader(
    "📂 Upload your lecture audio",
    type=["mp3", "wav", "m4a", "ogg"]
)

# ===== PROCESS AUDIO =====
if audio_file is not None:

    st.success(f"📁 File Uploaded: {audio_file.name}")
    st.write(f"📦 Size: {round(audio_file.size/1024,2)} KB")

    st.audio(audio_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
        tmp.write(audio_file.read())
        audio_path = tmp.name

    try:

        progress = st.progress(0)

        st.info("🔄 Loading Whisper Model...")
        progress.progress(25)

        model = whisper.load_model("tiny")

        st.info("🎙 Converting Speech To Text...")
        progress.progress(75)

        result = model.transcribe(audio_path)

        transcript = result["text"]
        language = result["language"]

        progress.progress(100)

        st.success("✅ Notes Generated Successfully!")

        # ===== METRICS =====
        word_count = len(transcript.split())
        char_count = len(transcript)
        reading_time = round(word_count / 200, 2)

        difficulty = "Easy" if word_count < 100 else "Medium"

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("📝 Words", word_count)
        col2.metric("📄 Characters", char_count)
        col3.metric("⏱ Reading Time", f"{reading_time} min")
        col4.metric("🌍 Language", language.upper())
        st.metric("🎓 Difficulty", difficulty)
        

        # ===== AUDIO INFORMATION CARD =====
        st.info(
            f"""
        🎵 File Name: {audio_file.name}

        📦 File Size: {round(audio_file.size/1024,2)} KB

        🌍 Language: {language.upper()}
        """
        )

        # ===== TABS =====
        tab1, tab2, tab3 = st.tabs([
            "📝 Transcript",
            "📊 Insights",
            "❓ Quiz"
        ])

        # =====================================
        # TRANSCRIPT TAB
        # =====================================
        with tab1:

            st.subheader("📝 Generated Transcript")

            search = st.text_input(
                "🔍 Search in Transcript"
            )

            if search:
                if search.lower() in transcript.lower():
                    st.success("✅ Keyword Found")
                else:
                    st.warning("❌ Keyword Not Found")

            st.text_area(
                "Transcript",
                transcript,
                height=250
            )

            st.download_button(
                "📥 Download Transcript",
                transcript,
                file_name="transcript.txt"
            )

            # ===== QUICK SUMMARY =====
            st.subheader("📋 Quick Summary")

            sentences = transcript.split(".")
            summary = ".".join(sentences[:2])

            st.info(summary)

            # ===== STUDY NOTES =====
            st.subheader("📚 Study Notes")

            notes = transcript.replace(".", "\n•")

            st.markdown(f"• {notes}")

        # =====================================
        # INSIGHTS TAB
        # =====================================
        with tab2:

            st.subheader("🔥 Top Keywords")

            words = transcript.lower().split()

            words = [
                word for word in words
                if len(word) > 3
            ]

            keywords = Counter(words).most_common(5)

            for word, count in keywords:
                st.write(
                    f"• {word} ({count} times)"
                )

            # ===== CHART =====
            df = pd.DataFrame(
                keywords,
                columns=["Word", "Count"]
            )

            st.subheader(
                "📈 Keyword Frequency Chart"
            )

            st.bar_chart(
                df.set_index("Word")
            )

            # ===== LEARNING INSIGHTS =====
            st.subheader(
                "🎯 Learning Insights"
            )

            st.success(
                f"Total Words: {word_count}"
            )

            st.success(
                f"Reading Time: {reading_time} min"
            )

            st.success(
                f"Top Topic Keywords: {len(keywords)}"
            )

            st.download_button(
                "📥 Download Notes",
                transcript,
                file_name="lecture_notes.txt"
            )

        # =====================================
        # QUIZ TAB
        # =====================================
        with tab3:

            st.subheader(
                "❓ Practice Questions"
            )

            st.write(
                "1️⃣ What is the main topic discussed in this lecture?"
            )

            st.write(
                "2️⃣ Explain the lecture in your own words."
            )

            st.write(
                "3️⃣ What are the important concepts mentioned?"
            )

            st.write(
                "4️⃣ Write a short summary of this lecture."
            )

            st.write(
                "5️⃣ What new thing did you learn from this lecture?"
            )

            st.text_area(
                "✍️ Write your answer here",
                height=150
            )

            st.download_button(
                "📥 Download Quiz Questions",
                """
1. What is the main topic discussed?
2. Explain the lecture in your own words.
3. What are the important concepts mentioned?
4. Write a short summary of this lecture.
5. What new thing did you learn from this lecture?
                """,
                file_name="quiz_questions.txt"
            )

    except Exception as e:
        st.error(f"❌ Error: {e}")