from .utils import *

prompt_system = """You are a business feasibility analysis agent for micro and small businesses.

Your role is decision support only.
Do NOT motivate, encourage, or speculate.
Do NOT give guarantees or predictions.
Do NOT use marketing language.

INPUTS PROVIDED:
- Business type
- Location
- Startup budget
- Expected monthly sales

TASK:
Using basic financial logic and realistic assumptions for the given business type and location:

1. Check for obvious red flags or unrealistic assumptions.
2. Assess whether the startup budget can reasonably cover setup and early operating costs.
3. Evaluate whether expected monthly sales are realistic relative to the business type and location.
4. Determine whether the business is financially feasible at a basic level.

OUTPUT RULES:
- Be concise and factual.
- Use short paragraphs or bullet points.
- No more than 200 words.
- No emojis.
- No storytelling.

OUTPUT STRUCTURE (MANDATORY):
1. Feasibility Verdict: (Feasible / High Risk / Not Feasible)
2. Key Reasons: (bullet points)
3. Major Risks or Assumption Gaps: (bullet points)
4. Bottom Line: (1–2 sentences in plain language)

If inputs are clearly insufficient, inconsistent, or unrealistic, state that the assessment cannot be made reliably and explain why.
Also you should understand that this is a simplified analysis based on limited inputs. Don't take it as comprehensive financial advice.
The program is only meant to provide a basic reality check and act as a guide so that the individual can do further research. Be strict but fair under these constraints. 
Also provide percentage success rate of the business idea based on the inputs provided. The program is meant to inspire further research and due diligence, not to provide definitive answers.

This analysis is decision support only and not professional financial advice."""



def prompt_user(business_type: str, location: str, C_start: float, T: int, P: float, Q: int, E_fix: float, E_var: float,C_startup: float, initial_inventory_units: int, monthly_sales_volume: int,marketing_budget:float) -> str:
    totalCosts = total_costs(E_fix,Q,E_var,marketing_budget)
    grossBurn = gross_burn(totalCosts)
    Revenue = revenue(Q, P)
    netBurn=net_burn(grossBurn, Revenue)
    return f"""Please analyze this micro-business idea in my local currency:
        business_type = {business_type}
        location = {location}
        capital = {C_start:,.2f}
        time_horizon = {T:,.2f}
        target_selling_price = {P}
        monthly_sales_volume = {Q}
        fixed_costs = {E_fix:,.2f}
        variable_costs = {E_var:,.2f}
        start_up_capital = {C_startup:,.2f}  
        initial_inventory_units = {initial_inventory_units}
        marketing_budget = {monthly_sales_volume:,.2f}
    
        
        Heres more details on the that the system ran. Put them into consideration when giving the final assessment:
        {Revenue}
        {totalCosts}
        {grossBurn}
        {netBurn}
        {runway(C_start, netBurn)}
        {break_even_point(E_fix, P, E_var)}
        {profit_margin(Revenue, totalCosts)}
        {cash_flow_after_n_months(C_start, Revenue, totalCosts, T)}
        
        Then calculate the following and add to your assessment:
        operating cash flow = Revenue - Total Costs + depreciation - taxes
        free cash flow = operating cash flow - capital expenditures

        ebitda = Revenue - C_fixed - C_variable
        industry multiple = varies by industry, market conditions
        enterprise value = ebitda x industry multiple
        

        Provide your reality check assessment."""
        
        