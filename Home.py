import streamlit as st

st.set_page_config(
    page_title="RBI NBFC Chatbot",
    page_icon="🤖",
)

st.title("Welcome to RBI NBFC Chatbot")

st.write("""
Welcome to the **RBI NBFC Chatbot**, your friendly assistant for quickly finding information from **RBI notifications** and **NBFC rules**.
This app makes it easy to search official documents in a conversational way.
""")

st.markdown("---")

# How to Use Section
st.subheader("How to Use")
st.write("""
1. Go to the **Chatbot** page from the sidebar.  
2. Type your question about RBI notifications or NBFC regulations.  
3. Click **Ask** to get an instant answer.  
4. Review previous questions and answers in the **History** page.
""")

st.markdown("---")

# Search Tips Section
st.subheader("Tips for Effective Searching")
st.write("""
- Use **specific keywords** from the RBI notifications (e.g., "NBFC registration", "capital requirements").  
- Ask **direct questions**, such as:  
  - "What is the minimum net owned fund for an NBFC?"  
  - "What are the RBI guidelines for NBFC lending?"  
- Ask multiple related questions **one by one** for better responses.
""")

st.markdown("---")

# RBI Logo Image
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Reserve_Bank_of_India_logo.svg/1920px-Reserve_Bank_of_India_logo.svg.png",
    caption="Reserve Bank of India (RBI) Logo",
    use_container_width=True
)

st.markdown("---")

st.write("Start exploring **RBI regulations** easily and efficiently!")
