# Agentic Financial Planner
A financial planning tool powered by AI agents.
Work in Progress.

## Getting Started

To run the project, you need two separate processes: one for the backend API and one for the frontend web server.

### 1. Run the Backend API

Ensure you have FastAPI and Uvicorn installed:
`pip install "fastapi[all]"`

Then, from your project's root directory, start the server:
`uvicorn backend.main:app --reload`

The API will be running at `http://127.0.0.1:8000`.

### 2. Run the Frontend

The frontend is a single `index.html` file. To avoid CORS issues, you must serve it from a local web server.

From your project's root directory, start a simple Python server:
`python -m http.server 5500`

The frontend will be available at `http://127.0.0.1:5500/index.html`.

### 3. API Testing

You can test the API directly by sending a POST request with a sample JSON payload to `http://127.0.0.1:8000/generate-plan`.

**Sample JSON Payload:**
```json
{
  "monthly_net_income": 5000,
  "monthly_expenses": 3500,
  "total_assets": 15000,
  "total_liabilities": 2000,
  "goals": [
    {
      "goal_name": "Emergency Fund",
      "target_amount": 10000,
      "target_date": "2026-06-01"
    },
    {
      "goal_name": "New Car Down Payment",
      "target_amount": 12000,
      "target_date": "2027-01-01"
    }
  ],
  "risk_profile": "moderate"
}
