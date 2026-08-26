import streamlit as st

from graph_state import create_shared_state
from ticket import create_ticket
from workflow import graph

st.set_page_config(page_title="Northstar Support Co.", page_icon="💬", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 20% 20%, #0d1b2e 0%, #05070d 60%);
}

[data-testid="stHeader"] {
    background: transparent;
}

h1 {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900 !important;
    letter-spacing: 4px;
    background: linear-gradient(90deg, #00f5ff, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(0, 245, 255, 0.35);
    text-transform: uppercase;
}

[data-testid="stCaptionContainer"] {
    color: #7dd3fc !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-size: 0.8rem !important;
    font-family: 'Share Tech Mono', monospace !important;
}

[data-testid="stForm"] {
    background: rgba(13, 27, 46, 0.6);
    border: 1px solid rgba(0, 245, 255, 0.35);
    border-radius: 14px;
    padding: 2rem;
    box-shadow: 0 0 25px rgba(0, 245, 255, 0.08), inset 0 0 40px rgba(168, 85, 247, 0.03);
}

.stTextInput input, .stTextArea textarea {
    background-color: #0a121f !important;
    color: #e0f7fa !important;
    border: 1px solid rgba(0, 245, 255, 0.3) !important;
    border-radius: 8px !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border: 1px solid #00f5ff !important;
    box-shadow: 0 0 12px rgba(0, 245, 255, 0.5) !important;
}

label {
    color: #7dd3fc !important;
    text-transform: uppercase;
    font-size: 0.75rem !important;
    letter-spacing: 1px;
}

.stFormSubmitButton button {
    background: linear-gradient(90deg, #00f5ff, #a855f7) !important;
    color: #05070d !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.25s ease;
    box-shadow: 0 0 15px rgba(0, 245, 255, 0.4);
}

.stFormSubmitButton button:hover {
    box-shadow: 0 0 30px rgba(0, 245, 255, 0.8), 0 0 45px rgba(168, 85, 247, 0.5);
    transform: translateY(-1px);
}

hr {
    border-color: rgba(0, 245, 255, 0.25) !important;
}

h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00f5ff !important;
    letter-spacing: 2px;
    text-transform: uppercase;
}

[data-testid="stAlert"] {
    background: rgba(13, 27, 46, 0.7) !important;
    border: 1px solid rgba(168, 85, 247, 0.4) !important;
    border-radius: 10px !important;
}

[data-testid="stMarkdownContainer"] p {
    color: #e0f7fa;
}
</style>
""", unsafe_allow_html=True)

st.title("Northstar Support Co.")
st.caption("Employee Benefits Support · Multi-Agent Triage System")

with st.form("ticket_form"):
    customer_name = st.text_input("Your name")
    question = st.text_area("Your benefits question")
    additional_info = st.text_area("Additional info (optional)", height=80)
    submitted = st.form_submit_button("Submit")

if submitted:
    if not customer_name.strip() or not question.strip():
        st.error("Please enter your name and a question before submitting.")
    else:
        ticket = create_ticket(customer_name.strip(), question.strip(), additional_info.strip())
        state = create_shared_state(ticket)

        with st.spinner("Analyzing your request..."):
            result = graph.invoke(state)

        st.session_state["last_result"] = result

if "last_result" in st.session_state:
    result = st.session_state["last_result"]
    st.divider()
    st.subheader("Response")

    if result["human_review"]:
        st.info("This request has been routed to a human specialist for review. You'll receive a follow-up shortly.")
    else:
        st.write(result["final_response"])

    st.caption(f"Reference ticket ID: {result['ticket']['id']}")
