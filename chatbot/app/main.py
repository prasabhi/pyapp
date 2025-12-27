# Import FastAPI framework and HTTPException for error handling
from fastapi import FastAPI, HTTPException

# Import Prometheus utilities
# Counter       → used to count events (like number of requests)
# generate_latest → generates metrics data in Prometheus format
# CONTENT_TYPE_LATEST → correct content-type header for Prometheus
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# Used to return raw responses (not JSON)
from fastapi.responses import Response

# Used to serve static files like HTML
from fastapi.responses import FileResponse

# Pydantic BaseModel is used for request body validation
from pydantic import BaseModel

# Import function that communicates with the LLM (OpenRouter)
from llm_client import get_chat_response

import os  # Optional: commonly used for environment variables

# Create FastAPI application instance
app = FastAPI(title="Chatbot with UI")


# -------------------------------
# Serve the Chatbot UI
# -------------------------------
# When a user opens http://localhost:8000,
# this endpoint returns the chatbot HTML page
@app.get("/")
def serve_ui():
    # Serve the index.html file from the ui folder
    return FileResponse("ui/index.html")


# -------------------------------
# Request Body Schema
# -------------------------------
# This class defines the expected JSON structure
# for the /chat POST request
class ChatRequest(BaseModel):
    # User's message sent from the UI
    message: str


# -------------------------------
# Chat API Endpoint
# -------------------------------
# This endpoint receives user input, sends it to the LLM,
# and returns the AI-generated response
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # Call the LLM client with the user's message
        reply = get_chat_response(request.message)

        # Return chatbot response as JSON
        return {
            "bot_response": reply
        }

    except Exception as e:
        # Handle unexpected errors gracefully
        # Return HTTP 500 instead of crashing the server
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -------------------------------
# Prometheus Metric Definition
# -------------------------------

# Create a Counter metric
# Name: http_requests_total
# Description: Total number of HTTP requests received
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests"
)

# -------------------------------
# Root API Endpoint
# -------------------------------

#@app.get("/")
def root():
    """
    This endpoint is called when user accesses "/"
    Each request increments the Prometheus counter
    """
    # Increment request counter by 1
    REQUEST_COUNT.inc()

    # Return normal JSON response
    return {"status": "ok"}

# -------------------------------
# Metrics Endpoint
# -------------------------------

@app.get("/metrics")
def metrics():
    """
    This endpoint exposes metrics in Prometheus format.
    Prometheus server scrapes this URL periodically.
    """
    return Response(
        # Generate all metrics in Prometheus text format
        generate_latest(),

        # Set correct content-type so Prometheus understands it
        media_type=CONTENT_TYPE_LATEST
    )