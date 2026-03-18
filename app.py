import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="SmartQuery",
    page_icon="📡",
    layout="wide"
)

st.title("📡 SmartQuery")
st.caption("Ask questions about smart TV telemetry schemas, Kafka topics, and on-call runbooks.")

st.markdown("---")

def ask_question(question: str):
    with st.spinner("Searching knowledge base..."):
        try:
            response = requests.post(
                f"{API_URL}/query",
                json={"question": question}
            )
            if response.status_code == 200:
                result = response.json()
                st.markdown("### Answer")
                st.success(result["answer"])
                st.markdown("### Sources")
                for source in result["sources"]:
                    st.code(source)
            else:
                st.error(f"API error: {response.status_code} — {response.text}")
        except Exception as e:
            st.error(f"Could not connect to API: {e}")

col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### Try These Questions")
    sample_questions = [
        "What fields does a BufferingEvent contain?",
        "What is the retention period for the heartbeat topic?",
        "What should I do if a Kafka broker times out?",
        "What causes a CrashReport event?",
        "How do I handle missing device heartbeats?",
        "What is the partition key for tv.events.playback?"
    ]
    for q in sample_questions:
        if st.button(q, key=q):
            st.session_state["current_question"] = q
            st.session_state["trigger"] = True

with col1:
    question = st.text_input(
        label="Your question",
        placeholder="e.g. What should I do if consumer lag is high?",
        value=st.session_state.get("current_question", "")
    )

    if st.button("Ask", type="primary"):
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            st.session_state["current_question"] = question
            st.session_state["trigger"] = True

if st.session_state.get("trigger", False):
    st.session_state["trigger"] = False
    current = st.session_state.get("current_question", "")
    if current.strip():
        ask_question(current)