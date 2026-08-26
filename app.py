import streamlit as st

from graph_state import create_shared_state
from ticket import create_ticket
from workflow import graph

st.set_page_config(page_title="Northstar Support Co.", page_icon="💬")

st.title("Northstar Support Co.")
st.caption("Employee Benefits Support")

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

        with st.spinner("Looking into your question..."):
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
