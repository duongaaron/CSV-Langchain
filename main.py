from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import tempfile

def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV 📈")

    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    tmp_path = None
    if csv_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmpfile:
            tmpfile.write(csv_file.read())
            tmp_path = tmpfile.name

        agent = create_csv_agent(
            ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0), tmp_path, verbose=True)

        user_question = st.text_input("Ask a question about your CSV: ")

        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                st.write(agent.run(user_question))
                
    if tmp_path:
        os.remove(tmp_path)

if __name__ == "__main__":
    main()
