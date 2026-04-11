# urban-nest-services

# 🧠 AI-Powered Customer Support System (FastAPI + LangChain + AstraDB)

## 📌 Overview

* **FastAPI** (backend framework)
* **MySQL + SQLAlchemy (Async)** (data persistence)
* **Redis** (session memory + caching)
* **LangChain + OpenAI** (LLM orchestration)
* **AstraDB Vector Store** (RAG & semantic search)

---

## 🚀 Key Features

### 🤖 AI Customer Support

* Natural language query handling
* Context-aware responses based on:

  * User role (Tenant, Landlord, Agent)
  * Past conversations (Redis memory)
  * Current session context

---

### 🧠 Retrieval-Augmented Generation (RAG)

* Semantic search using AstraDB
* Retrieves:

  * Property listings
  * FAQs
  * Policies
  * Lease documents

---

### 🏠 Property Recommendation Engine

* AI-powered property suggestions
* Query examples:

  * *"Show me a 2 bedroom house in Nairobi under 50k"*
* Uses:

  * Vector similarity search
  * LLM reasoning

---

### 🎯 Intelligent Ticketing System

* Automatically creates tickets when AI fails
* Categorizes issues:

  * PAYMENT
  * BOOKING
  * MAINTENANCE
  * OTHER

---

### 🔐 Guardrails (AI Safety)

* **Pre-processing**

  * Blocks unsafe queries (e.g. hacking attempts)
* **Post-processing**

  * Filters unsafe or policy-violating responses

---

### 💾 Memory System (Redis)

* Stores conversation history per session
* Enables:

  * Context-aware follow-ups
  * Personalized responses

---

## 🏗️ Project Structure

```
app/
├── models/
│   └── support_ticket_model.py
├── repositories/
│   └── support_ticket_repository.py
├── services/
│   ├── ai_support_service.py
│   ├── vector_store.py
│   ├── ticket_service.py
├── domain/
│   ├── entities/
│   ├── interfaces/
├── routes/
│   └── support_routes.py
├── redis/
│   └── redis_client.py
├── vector_store/
│   └── vector_store.py
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd project
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key

ASTRA_DB_API_ENDPOINT=your_endpoint
ASTRA_DB_APPLICATION_TOKEN=your_token
ASTRA_DB_COLLECTION=your_collection

REDIS_HOST=localhost
REDIS_PORT=6379
```

---

### 5. Run Services

#### Start Redis

```bash
redis-server
```

#### Run FastAPI

```bash
uvicorn app.main:app --reload
```

---

## 📡 API Endpoints

### 🎫 Support Tickets

| Method | Endpoint        | Description     |
| ------ | --------------- | --------------- |
| POST   | `/support/`     | Create ticket   |
| GET    | `/support/{id}` | Get ticket      |
| GET    | `/support/`     | Get all tickets |
| PUT    | `/support/{id}` | Update ticket   |
| DELETE | `/support/{id}` | Soft delete     |

---

### 🤖 AI Support

```http
POST /support/ai
```

#### Request:

```json
{
  "session_id": "abc123",
  "role": "TENANT",
  "user_id": "1",
  "query": "Show me a 2 bedroom house"
}
```

#### Response:

```json
{
  "ai_response": "...",
  "recommendations": "...",
  "ticket_created": false
}
```

---

## 🧠 AI Flow

1. User sends query
2. Pre-guardrail validation
3. Redis loads conversation history
4. AstraDB retrieves relevant documents
5. Prompt is constructed (RAG)
6. LLM generates response
7. Post-guardrail filters output
8. Memory updated in Redis
9. If AI fails → Ticket created

---

## 🔎 Core AI Methods

### AISupportServiceAdvanced

* `ask()` → Main AI handler
* `build_full_prompt()` → RAG prompt builder
* `get_search_results()` → Vector search
* `embed()` → Text embeddings
* `get_possible_recommended_properties()` → Raw retrieval
* `get_recommended_properties()` → LLM-enhanced recommendations

---

## 🧪 Example Use Cases

### 👤 Tenant

> “Show me a 2 bedroom house”

✔ Gets property recommendations
✔ Booking guidance

---

### 🧑‍💼 Landlord

> “Why haven't I received rent?”

✔ Payment insights
✔ System explanation

---

### ⚠️ AI Failure

> “There is an issue with rent deduction”

✔ AI unsure → Ticket created
✔ Categorized as PAYMENT

---

## 📈 Future Enhancements

* 🔥 LangChain Agents (tool-based reasoning)
* 🔥 Hybrid search (SQL + Vector DB)
* 🔥 WebSocket streaming responses
* 🔥 Multi-tenant AI isolation
* 🔥 Admin dashboard (ticket analytics)
* 🔥 LangSmith observability

---

## 🛡️ Security Considerations

* Input validation (guardrails)
* Output moderation
* Secure API keys via `.env`
* Role-based response control

---

## 👨‍💻 Author

Developed as an **enterprise-grade AI support system** integrating:

* LLMs
* Vector databases
* Backend engineering best practices

---

## 📜 License

MIT License
