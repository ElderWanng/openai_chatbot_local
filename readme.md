# Openai Chatbot

## restful api
| Endpoint                        | Method | Description                                     | Request                      | Response                                       |
|---------------------------------|--------|-------------------------------------------------|------------------------------|------------------------------------------------|
| `/api/sessions`                | POST   | Creates a new chat session and returns the ID   | None                         | `{ "session_id": "some_unique_id" }`           |
| `/api/sessions`                | GET    | Lists all active chat sessions                  | None                         | `[ { "session_id": "some_unique_id" }, ... ]`  |
| `/api/sessions/<session_id>/history` | GET  | Retrieves the chat history for a given session | None                         | `[ { "user": "user message", "bot": "bot response" }, ... ]` |
| `/api/sessions/<session_id>/chat`    | POST | Sends a user message and receives a response   | `{ "message": "user message" }` | `{ "response": "bot response" }`               |
| `/api/sessions/<session_id>`    | DELETE | Deletes a chat session and its chat history     | None                         | `{ "status": "success" }`                      |
ue_id" }