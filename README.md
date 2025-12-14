# Dify-like Backend System

This is a backend system similar to Dify, built with Python, FastAPI, and SQLite.

## Features
- Workflow management
- Large model integration (Qwen-Plus)
- RESTful API for frontend integration

## Project Structure
```
app/
├── api/              # API routes
├── core/             # Core modules (config, database, etc.)
├── crud/             # Database operations
├── models/           # Database models
├── schemas/          # Pydantic models for data validation
├── services/         # Business logic
└── utils/            # Utility functions

front/
├── src/              # Frontend source code
├── package.json      # Frontend dependencies
└── vite.config.js    # Vite configuration
```

## Setup
1. Install backend dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   Set your Qwen API key and base URL:
   ```
   QWEN_API_KEY=your_api_key_here
   QWEN_BASE_URL=your_base_url_here
   ```

3. Install frontend dependencies:
   ```
   cd front
   npm install
   ```

4. Run the backend application:
   ```
   python app/main.py
   ```
   or
   ```
   uvicorn app.main:app --reload
   ```

5. Run the frontend application (in a separate terminal):
   ```
   cd front
   npm run dev
   ```

## API Documentation
Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Frontend Development

To start the frontend development server:

```bash
cd front
npm install  # Install dependencies
npm run dev  # Start development server
```

The frontend will be available at http://localhost:5173 by default.

To build the frontend for production:

```bash
cd front
npm run build
```

## API Endpoints

### Workflow Management
- `POST /api/v1/workflows/` - Create a new workflow
- `GET /api/v1/workflows/{id}` - Get a workflow by ID
- `GET /api/v1/workflows/` - List workflows
- `PUT /api/v1/workflows/{id}` - Update a workflow
- `DELETE /api/v1/workflows/{id}` - Delete a workflow
- `POST /api/v1/workflows/{id}/execute` - Execute a workflow

### Model Integration
- `POST /api/v1/models/qwen-plus` - Call Qwen-Plus model

## Usage Examples

### Create a Workflow
```bash
curl -X POST "http://localhost:8000/api/v1/workflows/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Sample Workflow",
  "description": "A sample workflow for testing",
  "tasks": [
    {
      "name": "LLM Task",
      "description": "Call Qwen-Plus model",
      "type": "llm",
      "config": "{\"prompt\": \"Hello, world!\", \"temperature\": 0.7}",
      "order": 1
    }
  ]
}'
```

### Execute a Workflow
```bash
curl -X POST "http://localhost:8000/api/v1/workflows/1/execute"
```

### Call Qwen-Plus Model Directly
```bash
curl -X POST "http://localhost:8000/api/v1/models/qwen-plus" \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Write a poem about technology",
  "max_tokens": 200,
  "temperature": 0.8
}'
```