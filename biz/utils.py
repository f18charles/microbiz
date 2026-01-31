# biz/utils.py

import os
from groq import Groq
from typing import Optional


def get_groq_completion(prompt: str, system_prompt: Optional[str] = None, api_key: Optional[str] = None) -> str:
    """Generate a text completion using the Groq API.

    Args:
        prompt: The user's prompt content.
        system_prompt: Optional system prompt to provide higher-level instructions.
        api_key: Optional Groq API key. If not provided, falls back to the GROQ_API_KEY env var.

    Returns:
        The assistant's response text.
    """
    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError("Groq API key not provided")

    client = Groq(api_key=key)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.1-8b-instant",
        temperature=0.7,
        max_tokens=2048,
    )

    # Support different return shapes safely
    choice = chat_completion.choices[0]
    # Groq SDK returns .message.content similar to other SDKs
    return getattr(getattr(choice, "message", None), "content", str(choice))


import math



def startupCosts(capital: float, unit_cost: float, startup_units: int, contingency_fund: float) -> float:
    """
    Calculate total startup costs.
    preopening expenses(the capital)
    """
    return capital + (unit_cost * startup_units)  + contingency_fund

def breakEvenAnalysis(fixe_expenses: float, cost_per_unit: float, target_selling_price: float) -> Optional[int]:
    """
    Calculate break-even point in units.
    Returns None if break-even is not achievable.
    """
    
    # Basic validation
    if fixe_expenses < 0 or target_selling_price < 0 or cost_per_unit < 0:
        return None

    contribution_margin = target_selling_price - cost_per_unit

    # If margin is zero or negative, break-even is impossible
    if contribution_margin <= 0:
        return None

    return math.ceil(fixe_expenses / contribution_margin)

def cashFlowProjection(capital: float, monthly_revenue: float, monthly_expenses: float, months: int) -> float:
    """
    Calculate projected cash flow after a given number of months.
    """
    return capital + (monthly_revenue - monthly_expenses) * months

def revenueCalculation(price: float, quantity: int) -> float:
    """
    Calculate total revenue.
    Assumes quantity is number of units sold.
    """
    return price * quantity

def profitMargin(price: float, quantity: int,expenses: float) -> float:
    """
    Calculate profit margin percentage.
    """
    revenue = revenueCalculation(price,quantity)
    if revenue <= 0:
        return 0.0
    return ((revenue - expenses) / revenue) * 100

def monthlyBurn(fixe_expenses: float, variable_expenses: float) -> float:
    """
    Calculate total costs.
    Assumes both values are for the same period.
    """
    return fixe_expenses + variable_expenses

def netBurn(price: float, quantity: float, fixe_expenses: float, variable_expenses: float) -> float:
    """
    Calculate net burn after a given number of months.
    """
    return monthlyBurn(fixe_expenses,variable_expenses) - revenueCalculation(price,quantity)

def grossNetMargin(revenue: float, costs: float) -> float:
    """
    Calculate margin percentage.
    """
    if revenue <= 0:
        return 0.0
    return ((revenue - costs) / revenue) * 100

def cashRunway(capital: float, price: float, quantity: int, fixe_expenses: float, variable_expenses: float) -> int:
    """
    Calculate cash runway in months.
    """
    netburn = netBurn(price, quantity, fixe_expenses, variable_expenses)
    if netBurn <= 0:
        raise ValueError("Monthly burn rate must be greater than zero.")

    return math.floor(capital / netBurn)


from typing import Optional

def breakEvenPoint(fixe_expenses: float,price_per_unit: float,cost_per_unit: float) -> Optional[int]:
    """
    Calculate break-even point in units.
    Returns None if break-even is not achievable.
    """

    # Basic validation
    if fixe_expenses < 0 or price_per_unit < 0 or cost_per_unit < 0:
        return None

    contribution_margin = price_per_unit - cost_per_unit

    # If margin is zero or negative, break-even is impossible
    if contribution_margin <= 0:
        return None

    return math.ceil(fixe_expenses / contribution_margin)




