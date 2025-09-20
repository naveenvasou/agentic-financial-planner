from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
load_dotenv()
import os

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.3,
)

# Create prompt template for AI-driven financial planning
financial_planning_prompt = ChatPromptTemplate.from_template("""
You are an expert financial advisor. Based on the following financial information, provide a comprehensive financial plan in JSON format.

Financial Data:
- Monthly Net Income: ₹{monthly_net_income}
- Monthly Expenses: ₹{monthly_expenses}
- Monthly Savings: ₹{monthly_savings}
- Total Assets: ₹{total_assets}
- Total Liabilities: ₹{total_liabilities}
- Net Worth: ₹{net_worth}
- Debt-to-Asset Ratio: {debt_to_asset_ratio}
- Risk Profile: {risk_profile}
- Employment Status: {employment_status}
- Number of Dependents: {number_of_dependents}
- Goals: {goals_summary}

Please provide a response in the following JSON structure:
{{
    "executive_summary": "A brief 2-3 sentence summary of their overall financial position and top priority",
    "quick_wins": [
        "2-3 actionable quick wins they can implement immediately"
    ],
    "debt_repayment_plan": {{
        "strategy_name": "Name of recommended debt repayment strategy",
        "recommendation": "Detailed explanation of the strategy and why it's recommended",
        "steps": [
            "Step-by-step instructions for debt repayment"
        ]
    }},
    "investment_strategy": "Investment recommendations based on risk profile and goals, mention specific Indian investment options like ELSS, PPF, NSC, etc.",
    "disclaimer": "This is an AI-generated plan and does not constitute financial advice. Please consult with a qualified financial professional."
}}

Keep all currency amounts in Indian Rupees (₹). Focus on Indian financial instruments and context.
""")

# Create the chain
financial_planning_chain = financial_planning_prompt | llm | StrOutputParser()

def generate_ai_plan(financial_data: dict, goals: list) -> dict:
    """Generate AI-driven financial plan using Gemini"""
    try:
        # Prepare goals summary
        goals_summary = []
        for goal in goals:
            goals_summary.append(f"{goal['goal_name']}: ₹{goal['target_amount']} by {goal['target_date']}")
        
        # Generate AI response
        response = financial_planning_chain.invoke({
            "monthly_net_income": financial_data["monthly_net_income"],
            "monthly_expenses": financial_data["monthly_expenses"],
            "monthly_savings": financial_data["monthly_savings"],
            "total_assets": financial_data["total_assets"],
            "total_liabilities": financial_data["total_liabilities"],
            "net_worth": financial_data["net_worth"],
            "debt_to_asset_ratio": financial_data["debt_to_asset_ratio"],
            "risk_profile": financial_data["risk_profile"],
            "employment_status": financial_data["employment_status"],
            "number_of_dependents": financial_data["number_of_dependents"],
            "goals_summary": "; ".join(goals_summary) if goals_summary else "No specific goals mentioned"
        })
        
        # Parse JSON response
        import json
        # Clean the response to extract JSON
        response_clean = response.strip()
        if response_clean.startswith("```json"):
            response_clean = response_clean[7:-3]
        elif response_clean.startswith("```"):
            response_clean = response_clean[3:-3]
            
        return json.loads(response_clean)
        
    except Exception as e:
        # Fallback response if AI fails
        return {
            "executive_summary": "Unable to generate AI analysis at this time. Your financial data has been processed successfully.",
            "quick_wins": [
                "Review your monthly expenses to identify areas for cost reduction",
                "Consider setting up automatic transfers to build your emergency fund"
            ],
            "debt_repayment_plan": {
                "strategy_name": "Avalanche Method",
                "recommendation": "Focus on paying off highest interest rate debts first while making minimum payments on others.",
                "steps": [
                    "List all debts with their interest rates",
                    "Make minimum payments on all debts",
                    "Apply extra payments to highest interest debt"
                ]
            },
            "investment_strategy": "Consider diversified mutual funds and SIPs based on your risk profile. Consult a financial advisor for personalized recommendations.",
            "disclaimer": "This is an AI-generated plan and does not constitute financial advice. Please consult with a qualified financial professional."
        }
