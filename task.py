import streamlit as st
import json
from difflib import SequenceMatcher

# FAQ Database (Replace with your own FAQs)
FAQ_DATA = {
    "What are your business hours?": "We are open Monday-Friday, 9 AM - 6 PM IST",
    "How do I reset my password?": "Go to login page, click 'Forgot Password', enter your email, and follow the link",
    "What is your refund policy?": "We offer 30-day money-back guarantee for all products",
    "How do I contact support?": "Email us at support@company.com or use the escalate button below",
    "Do you offer free trial?": "Yes, we offer a 14-day free trial with full access",
}

def find_best_faq_match(user_question):
    """Find the most similar FAQ using string matching"""
    best_match = None
    best_score = 0
    
    for faq_question in FAQ_DATA.keys():
        score = SequenceMatcher(None, user_question.lower(), faq_question.lower()).ratio()
        if score > best_score:
            best_score = score
            best_match = faq_question
    
    # Return answer if similarity is above 60%
    if best_score > 0.6:
        return FAQ_DATA[best_match], best_score
    return None, best_score

# Streamlit UI
st.set_page_config(page_title="Support Assistant", layout="wide")
st.title("🤖 Support Assistant Agent")
st.write("Ask me anything about our services!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_question = st.chat_input("Type your question here...")

if user_question:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_question)
    
    # Find FAQ match
    answer, confidence = find_best_faq_match(user_question)
    
    if answer:
        # FAQ matched - show answer
        response = f"✅ **FAQ Answer** (Confidence: {confidence*100:.1f}%)\n\n{answer}"
        source = "FAQ Database"
    else:
        # No match - provide generic response
        response = "I couldn't find a direct answer in our FAQ database. Please escalate this to our support team for better assistance."
        source = "Escalation Needed"
    
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display bot response
    with st.chat_message("assistant"):
        st.write(response)
    
    # Escalation button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📞 Escalate to Human Support"):
            st.success("✅ Your query has been escalated. A support agent will contact you soon!")
    with col2:
        if st.button("📧 Email Support"):
            st.info("Support email: support@company.com")

# Footer
st.divider()
st.caption("Support Assistant v1.0 | AI-Powered FAQ Resolver")