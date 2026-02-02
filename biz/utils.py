# biz/utils.py

import os
from groq import Groq
from typing import Optional
import math
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


# calculations
"""
Revenue = Q x P
Total Costs(monthly) = C_fixed + (Q x C_variable) + market budget
gross burn = Total Costs
net burn = gross burn - Revenue
runway = c_start + net burn per month
break even point (units) = C_fixed / (P - C_variable)
profit margin % = (Revenue - Total Costs) / Revenue * 100
cash flow after n months = c_start + (Revenue - Total Costs) * n
operating cash flow = Revenue - Total Costs + depreciation - taxes
free cash flow = operating cash flow - capital expenditures

AI's job is to fill in the variables with realistic assumptions based on business type and location. and calculate the values below
enterprise value = ebitda x industry multiple
ebitda = Revenue - C_fixed - C_variable
industry multiple = varies by industry, market conditions
"""


def revenue(Q: float, P: float) -> float:
    return Q * P

def total_costs(C_fixed: float, Q: float, C_variable: float) -> float:
    return C_fixed + (Q * C_variable)

def gross_burn(total_costs: float) -> float:
    return total_costs

def net_burn(gross_burn: float, revenue: float) -> float:
    return gross_burn - revenue

def runway(c_start: float, net_burn: float) -> Optional[float]:
    if net_burn <= 0:
        return None  # Infinite runway if not burning cash
    return c_start / abs(net_burn)

def break_even_point(C_fixed: float, P: float, C_variable: float) -> Optional[float]:
    if P <= C_variable:
        return None  # No break-even point if price is less than or equal to variable cost
    return C_fixed / (P - C_variable)

def profit_margin(revenue: float, total_costs: float) -> Optional[float]:
    if revenue == 0:
        return None
    return (revenue - total_costs) / revenue * 100

def cash_flow_after_n_months(c_start: float, revenue: float, total_costs: float, t: int) -> float:
    return c_start + (revenue - total_costs) * t

"""
operating cash flow = Revenue - Total Costs + depreciation - taxes
free cash flow = operating cash flow - capital expenditures

ebitda = Revenue - C_fixed - C_variable
industry multiple = varies by industry, market conditions
enterprise value = ebitda x industry multiple
"""
