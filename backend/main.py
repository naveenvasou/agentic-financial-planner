from fastapi import FastAPI
from pydantic import BaseModel, Field, conlist
from typing import Literal
from datetime import date
from fastapi.middleware.cors import CORSMiddleware

class Goal(BaseModel):
    goal_name: str = Field(..., description="Name of the goal (e.g., 'Retirement', 'Home Down Payment').")
    target_amount: float = Field(..., description="The financial amount needed for the goal.", ge=0)
    target_date: date = Field(..., description="The target date for achieving the goal.")
    
class FinancialPlanInput(BaseModel):
    monthly_net_income: float = Field(..., description="User's total monthly net income after taxes.", ge=0)
    monthly_expenses: float = Field(..., description="User's total monthly expenses.", ge=0)
    total_assets: float = Field(..., description="Total value of all assets (e.g., cash, investments).", ge=0)
    total_liabilities: float = Field(..., description="Total value of all liabilities (e.g., loans, credit card debt).", ge=0)
    goals: conlist(Goal, min_length=0) = Field(..., description="A list of the user's financial goals.")
    risk_profile: Literal["conservative", "moderate", "aggressive"] = Field(..., description="The user's general risk tolerance.")

app = FastAPI(title = "Agentic Financial Planner")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-plan")
def generate_plan(plan_data: FinancialPlanInput):
    
    monthly_savings = plan_data.monthly_net_income - plan_data.monthly_expenses
    processed_goals = []
    today = date.today()
    
    for goal in plan_data.goals:
        # Calculate months remaining
        # We'll use a simple approximation for months_until_target
        if goal.target_date <= today:
            months_until_target = 0
            monthly_required = goal.target_amount  # Treat as an immediate lump sum required
        else:
            months_until_target = (goal.target_date.year - today.year) * 12 + (goal.target_date.month - today.month)
            if months_until_target == 0:
                months_until_target = 1
            monthly_required = goal.target_amount / months_until_target
        
        # 3. Flag goal as on_track
        on_track = monthly_savings >= monthly_required
        
        # Create a new object with the original goal data plus calculations
        processed_goal = {
            **goal.dict(),
            "monthly_required": round(monthly_required, 2),
            "on_track": on_track
        }
        processed_goals.append(processed_goal)
        
    return {
        "monthly_savings": round(monthly_savings, 2),
        "goals_status": processed_goals,
        "raw_data": plan_data
    }