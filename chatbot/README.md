1️⃣ OVERALL FLOW (BIG PICTURE)

    User types message in browser
            ↓
    Browser sends POST /chat (JSON)
            ↓
    FastAPI receives request
            ↓
    FastAPI calls OpenRouter LLM
            ↓
    LLM returns response
            ↓
    FastAPI sends response back
            ↓
    UI displays chatbot reply

2️⃣ app/main.py — FASTAPI (UI + API)

    from fastapi import FastAPI, HTTPException
    from fastapi.responses import FileResponse
    from pydantic import BaseModel
    from app.llm_client import get_chat_response

    What this does

        FastAPI → web framework
        FileResponse → send HTML file to browser
        BaseModel → validate JSON request
        get_chat_response → function that talks to OpenRouter
