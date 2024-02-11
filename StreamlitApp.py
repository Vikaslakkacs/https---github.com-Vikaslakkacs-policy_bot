import os
import traceback
from dotenv import load_dotenv
from src.policy_bot.policy_details import generate_evaluate_chain
from src.policy_bot.utils import read_file
import streamlit as st
from langchain.callbacks import get_openai_callback

##Crating title for application
# st.title("Policy bot: A Knowledge bot which provides you answers regarding policies exist in company")
st.header('Policy bot', divider='rainbow')
st.subheader('A Knowledge bot that answers your questions about all the policies available within organization.')
##Streamlit form creation
with st.form("user_inputs"):
    ##File upload (Can upload multiple files)
    upload_file_list= st.file_uploader("Upload one or more files", type=['txt'], accept_multiple_files=True)
    print(f"Type of Upload files folder")
    ## Input fields
    question=st.text_input("Ask anything about policies available", max_chars=100)
    
    # Set Tone of the question
    tone= st.text_input("Complexity level of question", max_chars=20, placeholder="Simple")
    
    ## Submit button
    ask_button= st.form_submit_button("Ask")

## Field Validations
if ask_button and upload_file_list is not None and question:
    with st.spinner("Fetching details..."):
        try:
            ## Get the text from files
            text= read_file(upload_file_list)
            ##Execute evaluate chain
            with get_openai_callback() as cb:
                response= generate_evaluate_chain(
                    {
                        "text": text,
                        "tone": tone,
                        "question": question
                    }
                )      
        except Exception as e:
            traceback.print_exception(type(e),e, e.__traceback__)
            st.error("Error")      
        
        else:
            
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion tokens: {cb.completion_tokens}")
            print(f"Total Cost:{cb.total_cost}")
            
            if isinstance(response, str):
                answer= response.get("policy_response")
                st.text_area(label= "Reponse", value= answer)
            else:
                st.write(response.get('policy_response'))