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


def revenueCalculation(price: float, quantity: int) -> float:
    """
    Calculate total revenue.
    Assumes quantity is number of units sold.
    """
    return price * quantity


def costBreakdown(fixed_costs: float, variable_costs: float) -> float:
    """
    Calculate total costs.
    Assumes both values are for the same period.
    """
    return fixed_costs + variable_costs


def grossNetMargin(revenue: float, costs: float) -> float:
    """
    Calculate margin percentage.
    """
    if revenue <= 0:
        return 0.0
    return ((revenue - costs) / revenue) * 100


from typing import Optional

def breakEvenPoint(
    fixed_costs: float,
    price_per_unit: float,
    variable_cost_per_unit: float
) -> Optional[int]:
    """
    Calculate break-even point in units.
    Returns None if break-even is not achievable.
    """

    # Basic validation
    if fixed_costs < 0 or price_per_unit < 0 or variable_cost_per_unit < 0:
        return None

    contribution_margin = price_per_unit - variable_cost_per_unit

    # If margin is zero or negative, break-even is impossible
    if contribution_margin <= 0:
        return None

    return math.ceil(fixed_costs / contribution_margin)



def cashRunway(cash_on_hand: float, monthly_burn_rate: float) -> int:
    """
    Calculate cash runway in months.
    """
    if monthly_burn_rate <= 0:
        raise ValueError("Monthly burn rate must be greater than zero.")

    return math.floor(cash_on_hand / monthly_burn_rate)
