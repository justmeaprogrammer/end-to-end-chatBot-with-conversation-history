```
██████╗  █████╗  ██████╗       ██████╗  ██████╗  ██████╗
██╔══██╗██╔══██╗██╔════╝       ██╔══██╗██╔═══██╗██╔════╝
██████╔╝███████║██║  ███╗█████╗██║  ██║██║   ██║██║
██╔══██╗██╔══██║██║   ██║╚════╝██║  ██║██║   ██║██║
██║  ██║██║  ██║╚██████╔╝      ██████╔╝╚██████╔╝╚██████╗
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝       ╚═════╝  ╚═════╝  ╚═════╝
```

`STATUS: ONLINE` &nbsp; `STACK: LANGCHAIN + GROQ + CHROMA` &nbsp; `UI: STREAMLIT`

upload a document. ask it a question. it answers, with memory.

---

## // WHAT THIS IS

A conversational RAG system. Upload one or more PDFs, ask questions in natural
language, get answers grounded in the document content — with chat history
maintained per session, so follow-up questions resolve correctly against
prior context.

```
[ PDF(s) ] → [ split ] → [ embed ] → [ chroma vectorstore ]
                                            │
[ question ] → [ history-aware retriever ] ─┘
                        │
              [ groq llm ] → [ answer ]
```

---

## // STACK

| LAYER            | COMPONENT                                  |
|------------------|---------------------------------------------|
| LLM              | Groq (`llama-3.1-8b-instant`)                |
| ORCHESTRATION    | LangChain (`langchain_classic`)              |
| EMBEDDINGS       | HuggingFace (`all-MiniLM-L6-v2`)             |
| VECTOR STORE     | Chroma                                       |
| CHAT MEMORY      | `RunnableWithMessageHistory` (in-session)    |
| UI               | Streamlit                                    |

---

## // RUN IT

```bash
# 1. clone + enter
git clone <this-repo>
cd <this-repo>

# 2. create + activate venv
python -m venv venv
source venv/bin/activate

# 3. install deps
pip install -r requirements.txt

# 4. set your HuggingFace token
echo "HF_TOKEN=your_token_here" > .env

# 5. run
streamlit run app.py
```

You will need a **Groq API key** — enter it directly in the sidebar at
runtime. It is not stored anywhere; it lives only in the Streamlit session.

---

## // USAGE

```
1. paste groq api key           → sidebar
2. set a session id             → sidebar (default_session is fine)
3. upload one or more pdfs      → sidebar
4. type your question           → main panel
5. read the answer              → chat window
6. inspect raw state if needed  → "RAW SESSION STATE / LOG" expander
```

Follow-up questions ("what about the second one?") resolve correctly —
each session's history is tracked and used to reformulate ambiguous
queries before retrieval.

---

## // KNOWN LIMITATIONS

```
[ ] embeddings + vectorstore rebuild on every rerun   → slow on large PDFs
[ ] no API key validation before first query           → bad key fails late
[ ] single machine / in-memory store                   → no persistence across restarts
```

---

## // ROADMAP

```
- [ ] cache embedding model + vectorstore (st.cache_resource)
- [ ] validate groq key on entry, fail fast with a clear message
- [ ] persist chat history across restarts
- [ ] swap RunnableWithMessageHistory → LangGraph persistence
```

---

`BUILT BY OM` // `AI & DATA SCIENCE, D.Y. PATIL COE, PUNE````
██████╗  █████╗  ██████╗       ██████╗  ██████╗  ██████╗
██╔══██╗██╔══██╗██╔════╝       ██╔══██╗██╔═══██╗██╔════╝
██████╔╝███████║██║  ███╗█████╗██║  ██║██║   ██║██║
██╔══██╗██╔══██║██║   ██║╚════╝██║  ██║██║   ██║██║
██║  ██║██║  ██║╚██████╔╝      ██████╔╝╚██████╔╝╚██████╗
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝       ╚═════╝  ╚═════╝  ╚═════╝
```

`STATUS: ONLINE` &nbsp; `STACK: LANGCHAIN + GROQ + CHROMA` &nbsp; `UI: STREAMLIT`

upload a document. ask it a question. it answers, with memory.

---

## // WHAT THIS IS

A conversational RAG system. Upload one or more PDFs, ask questions in natural
language, get answers grounded in the document content — with chat history
maintained per session, so follow-up questions resolve correctly against
prior context.

```
[ PDF(s) ] → [ split ] → [ embed ] → [ chroma vectorstore ]
                                            │
[ question ] → [ history-aware retriever ] ─┘
                        │
              [ groq llm ] → [ answer ]
```

---

## // STACK

| LAYER            | COMPONENT                                  |
|------------------|---------------------------------------------|
| LLM              | Groq (`llama-3.1-8b-instant`)                |
| ORCHESTRATION    | LangChain (`langchain_classic`)              |
| EMBEDDINGS       | HuggingFace (`all-MiniLM-L6-v2`)             |
| VECTOR STORE     | Chroma                                       |
| CHAT MEMORY      | `RunnableWithMessageHistory` (in-session)    |
| UI               | Streamlit                                    |

---

## // RUN IT

```bash
# 1. clone + enter
git clone <this-repo>
cd <this-repo>

# 2. create + activate venv
python -m venv venv
source venv/bin/activate

# 3. install deps
pip install -r requirements.txt

# 4. set your HuggingFace token
echo "HF_TOKEN=your_token_here" > .env

# 5. run
streamlit run app.py
```

You will need a **Groq API key** — enter it directly in the sidebar at
runtime. It is not stored anywhere; it lives only in the Streamlit session.

---

## // USAGE

```
1. paste groq api key           → sidebar
2. set a session id             → sidebar (default_session is fine)
3. upload one or more pdfs      → sidebar
4. type your question           → main panel
5. read the answer              → chat window
6. inspect raw state if needed  → "RAW SESSION STATE / LOG" expander
```

Follow-up questions ("what about the second one?") resolve correctly —
each session's history is tracked and used to reformulate ambiguous
queries before retrieval.

---

## // KNOWN LIMITATIONS

```
[ ] embeddings + vectorstore rebuild on every rerun   → slow on large PDFs
[ ] no API key validation before first query           → bad key fails late
[ ] single machine / in-memory store                   → no persistence across restarts
```

---

## // ROADMAP

```
- [ ] cache embedding model + vectorstore (st.cache_resource)
- [ ] validate groq key on entry, fail fast with a clear message
- [ ] persist chat history across restarts
- [ ] swap RunnableWithMessageHistory → LangGraph persistence
```

---

`BUILT BY OM` // `AI & DATA SCIENCE, D.Y. PATIL COE, PUNE`