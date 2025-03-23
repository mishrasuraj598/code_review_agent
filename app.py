import os
import json
import streamlit as st

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from schemas import CodeReviewInput, CodeReviewOutput
from prompts import SYSTEM_MESSAGE, HUMAN_MESSAGE, INSTRUCTIONS

# Load environment variables
load_dotenv('.env')

# Define the Google Generative AI model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=2000,
    timeout=45,
    max_retries=2,
)

# Function to run code review
def run_review_chain(code):
    parser = PydanticOutputParser(pydantic_object=CodeReviewOutput)
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_MESSAGE),
            ("human", INSTRUCTIONS),
            ("human", HUMAN_MESSAGE),
        ]
    )

    chain = prompt | llm | parser
    output = chain.invoke({"code": code})
    return output.dict()

# Streamlit UI
st.set_page_config(page_title="Power Automate Code Review", layout="wide")

# Header
st.header("Power Automate Code Review Agent 🚀")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Code Review", "Power Automate Best Practices", "Contact Info", "How It Works"])

with tab1:
    st.header("Upload Power Automate Code for Review")

    # File Upload
    uploaded_file = st.file_uploader("Upload a JSON or XML file", type=["json", "xml"])

    if uploaded_file:
        file_name = uploaded_file.name
        file_extension = file_name.split(".")[-1]
        input_code = uploaded_file.read().decode("utf-8")
        
        # Run Review Button
        if st.button("Run Code Review"):
            review_result = run_review_chain(input_code)

            # # Display Output
            st.subheader("Review Results")

            # Format JSON for better readability
            if review_result["review_status"]:
                st.text("Code looks great. I have no recommendations to improve it further! Good Job!!")
            else:
                st.subheader("Issues Found:")
                st.markdown(("\n\n- ").join(review_result["problems_identified"]))
                st.markdown("*"*50)
                st.subheader("Recommendations:")
                st.markdown(("\n\n- ").join(review_result["recommendations"]))

            # Save to file
            output_path = f"outputs/review_{file_name.split('.')[0]}.json"
            os.makedirs("outputs", exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(review_result, f, indent=4)

            # Download Button
            with open(output_path, "rb") as f:
                st.download_button(label="Download Review Report", data=f, file_name=f"review_{file_name.split('.')[0]}.json", mime="application/json")

with tab2:
    st.header("Best Practices for Power Automate")
    st.markdown("""
    - **Use Clear Naming Conventions**: Meaningful names for flows, variables, and actions.
    - **Error Handling**: Implement 'Run After' settings, try-catch scopes, and log errors.
    - **Optimize Performance**: Avoid unnecessary loops, use parallel branching, and filter data early.
    - **Security & Access Control**: Use service accounts, restrict permissions, and store sensitive data securely.
    - **Version Control & Documentation**: Enable version history, add meaningful commit messages, and maintain documentation.
    """)

with tab3:
    st.header("Contact Information")
    st.markdown("""
    - 📧 **Email**: your_email@example.com
    - 📞 **Phone**: +123-456-7890
    - 🌐 **Website**: [Your Website](https://example.com)
    """)

with tab4:
    st.header("How This Tool Works")
    st.markdown("""
    1. **Upload** a Power Automate JSON or XML file.
    2. Click **Run Code Review** to analyze the code.
    3. AI Model processes the input and provides:
       - **Review Status**
       - **Identified Issues**
       - **Recommendations**
    4. **Download** the review report for future reference.
    """)

# st.success("Power Automate Code Review Tool is ready! 🚀")
