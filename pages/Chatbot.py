import streamlit as st
from app.chatbot_chain import get_predictor

st.title("Chat with RBI NBFC Chatbot")

# Load predictor (you can cache it for performance)
@st.cache_resource
def load_predictor():
    return get_predictor(faiss_folder="data/faiss_index")

predict = load_predictor()

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_history" not in st.session_state:
    st.session_state.selected_history = None

# Main input
query = st.text_input("Ask about the RBI notification / NBFC rules", key="q")
if st.button("Ask"):
    if query:
        with st.spinner("Searching RBI docs..."):
            run = predict({"input": query})
            answer = run.get("output", "")
        st.session_state.history.append({"q": query, "a": answer})
        st.session_state.selected_history = {"q": query, "a": answer}

# Show selected conversation
if st.session_state.selected_history:
    st.subheader("Selected Conversation")
    st.markdown(f"**Q:** {st.session_state.selected_history['q']}")
    st.markdown(f"**A:** {st.session_state.selected_history['a']}")

# Sidebar: Conversation history
with st.sidebar:
    st.header("Conversation History")
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history)):
            if st.button(entry["q"], key=f"hist_{i}"):
                st.session_state.selected_history = entry
    else:
        st.write("No history yet. Start asking questions!")
