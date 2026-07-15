import streamlit as st 
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains import create_history_aware_retriever

from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os
from dotenv import load_dotenv
load_dotenv()

os.environ['HF_TOKEN']=os.getenv('HF_TOKEN')
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)   

## Streamlit app config
st.set_page_config(
    page_title="RAG // DOC-QUERY",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Theme: brutalist / raw. Concrete grays, monospace, one hazard-orange accent.
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg: #0d0d0d;
    --panel: #161616;
    --concrete: #2a2a2a;
    --line: #3d3d3d;
    --fg: #eaeaea;
    --fg-dim: #8c8c8c;
    --accent: #ff5c00;
}

.stApp {
    background: var(--bg);
    color: var(--fg);
    font-family: 'JetBrains Mono', monospace;
}

/* Header */
.brute-header {
    padding: 1.1rem 1.2rem;
    border: 2px solid var(--fg);
    background: var(--panel);
    margin-bottom: 1.6rem;
    position: relative;
}
.brute-header::before {
    content: "";
    position: absolute;
    top: -2px; left: -2px;
    width: 14px; height: 14px;
    background: var(--accent);
}
.brute-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
    line-height: 1.0;
    text-transform: uppercase;
}
.brute-title span { color: var(--accent); }
.brute-subtitle {
    font-family: 'Space Mono', monospace;
    color: var(--fg-dim);
    font-size: 0.85rem;
    margin-top: 0.5rem;
    letter-spacing: 0.01em;
}
.brute-tag {
    display: inline-block;
    font-size: 0.7rem;
    color: var(--bg);
    background: var(--accent);
    padding: 0.1rem 0.5rem;
    margin-top: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.08em;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--panel);
    border-right: 2px solid var(--fg);
}
section[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'JetBrains Mono', monospace;
    color: var(--fg);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-size: 0.85rem;
    border-bottom: 2px solid var(--accent);
    padding-bottom: 0.4rem;
    display: inline-block;
}

/* Inputs */
.stTextInput input, .stTextInput textarea {
    background: var(--concrete) !important;
    color: var(--fg) !important;
    border: 2px solid var(--line) !important;
    border-radius: 0px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: none !important;
}
label, .stTextInput label p {
    color: var(--fg-dim) !important;
    font-family: 'Space Mono', monospace !important;
    text-transform: uppercase;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em;
}

/* File uploader */
[data-testid="stFileUploaderDropzone"] {
    background: var(--concrete) !important;
    border: 2px dashed var(--fg-dim) !important;
    border-radius: 0px !important;
}

/* Buttons */
.stButton button, [data-testid="stFileUploaderDropzone"] button {
    background: var(--fg) !important;
    color: var(--bg) !important;
    border: 2px solid var(--fg) !important;
    border-radius: 0px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}
.stButton button:hover {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    color: var(--bg) !important;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background: var(--panel);
    border: 2px solid var(--line);
    border-radius: 0px;
    padding: 0.3rem 0.6rem;
    margin-bottom: 0.7rem;
}

/* Divider / caption text */
.stCaption, .brute-caption {
    color: var(--fg-dim) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem;
}

/* Expander (raw history) */
[data-testid="stExpander"] {
    border: 2px solid var(--line) !important;
    background: var(--panel) !important;
    border-radius: 0px !important;
}

::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--line); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="brute-header">
    <div class="brute-title">RAG <span>//</span> DOC-QUERY</div>
    <div class="brute-subtitle">upload a document. ask it a question. it answers, with memory.</div>
    <div class="brute-tag">STATUS: ONLINE</div>
</div>
""", unsafe_allow_html=True)

#input groq api key — sidebar, so the reading room stays uncluttered
with st.sidebar:
    st.markdown("### Credentials")
    api_key=st.text_input("Enter your Groq API key:",type="password")

    st.markdown("### Session")
    session_id=st.text_input("Sesson ID",value="default_session")

    st.markdown("### Manuscript")
    uploaded_files = st.file_uploader("Upload the file ",type="pdf",accept_multiple_files=True)

##check if api key is provided
if api_key:
    llm = ChatGroq(model='llama-3.1-8b-instant',groq_api_key=api_key)
    
    #chat Interface
    
    # Statefully manage Chat history
    
    if "store" not in st.session_state:
        st.session_state.store={}
        
    #process the uploaded file
    
    if uploaded_files:
        documents=[]
        for uploaded_file in uploaded_files:
            tempPdf=f"./temp.pdf"
            with open(tempPdf,'wb') as file:
                file.write(uploaded_file.getvalue())
                file_name=uploaded_file.name
                
            loader = PyPDFLoader(tempPdf)
            docs = loader.load()
            documents.extend(docs)
            
        #text splitting and embeddings        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000,chunk_overlap=200)
        splits = text_splitter.split_documents(documents)
        vectoreStore = Chroma.from_documents(documents=splits,embedding=embeddings)
        retriever = vectoreStore.as_retriever()
    
    
    
        contextualize_q_system_prompt=(
        "Given a chat history and the latest user question"
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
        )

        contextualize_q_prompt=ChatPromptTemplate.from_messages(
        [
        ("system",contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human","{input}")
        ]
        )

        history_aware_retriever = create_history_aware_retriever(llm,retriever,contextualize_q_prompt)

        ###Answer Question
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm,qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever,question_answer_chain)

        def get_session_history(session:str)->BaseChatMessageHistory:
            if session_id not in st.session_state.store:
                st.session_state.store[session_id]=ChatMessageHistory()
            return st.session_state.store[session_id]

        conversational_rag_chain=RunnableWithMessageHistory(
            rag_chain,get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        st.markdown('<p class="brute-caption">&gt; QUERY THE DOCUMENT</p>', unsafe_allow_html=True)
        user_input = st.text_input("Your question:")
        if user_input:
            session_history=get_session_history(session_id)
            response = conversational_rag_chain.invoke(
                {"input": user_input},
                config={
                    "configurable": {"session_id":session_id}
                },  # constructs a key "abc123" in `store`.
            )

            with st.chat_message("user"):
                st.markdown(user_input)
            with st.chat_message("assistant"):
                st.markdown(response['answer'])

            with st.expander("RAW SESSION STATE / LOG"):
                st.write(st.session_state.store)
                st.write("Chat History:", session_history.messages)
    else:
        st.markdown(
            '<p class="brute-caption">&gt; NO DOCUMENT LOADED. UPLOAD A PDF IN THE SIDEBAR.</p>',
            unsafe_allow_html=True
        )
else:
    st.warning("Failure")