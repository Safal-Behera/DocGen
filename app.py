import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("Groq_API_KEY"))

# Page setup
st.set_page_config(page_title="AI Doc Generator", page_icon="📄")
st.title("📄 AI Documentation Generator")
st.write("Paste your code below and get clean documentation instantly.")

# Input section
code_input = st.text_area("Paste your code here:", height=250, placeholder="def add(a, b):\n    return a + b")

doc_style = st.selectbox("Choose documentation style:", [
    "Detailed explanation",
    "Quick summary",
    "Beginner-friendly"
])

# Generate button
if st.button("Generate Documentation ✨"):
    if not code_input.strip():
        st.warning("⚠️ Please paste some code first!")
    else:
        with st.spinner("AI is analyzing your code..."):
            prompt = f"""You are a documentation expert.
Analyze the following code and generate {doc_style} documentation.
Include:
- What the code does
- Parameters/inputs (if any)
- Return value (if any)
- A usage example

Code:
{code_input}
"""
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content

        st.success("✅ Documentation generated!")
        st.markdown("### 📋 Generated Documentation")
        st.markdown(result)

        # Download button
        st.download_button(
            label="⬇️ Download as .txt",
            data=result,
            file_name="documentation.txt",
            mime="text/plain"
        )