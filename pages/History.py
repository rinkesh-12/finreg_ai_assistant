import streamlit as st

st.title("Full Conversation History")

if "history" in st.session_state and st.session_state.history:
    for entry in reversed(st.session_state.history):
        st.markdown(f"**Q:** {entry['q']}")
        st.markdown(f"**A:** {entry['a']}")
        st.markdown("---")
else:
    st.write("No conversations yet.")
