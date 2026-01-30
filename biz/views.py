"""
Views for the Reality Check app using Groq AI.
"""

import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .utils import get_groq_completion  # Your Groq API utility function
from .prompt import prompt_system, prompt_user  # Importing the system prompt


def index(request):
    """Render the main page."""
    return render(request, 'index.html')


@csrf_exempt
@require_http_methods(["POST"])
def analyze(request):
    """
    API endpoint to analyze business inputs using Groq AI.
    """
    try:
        # Parse JSON body
        data = json.loads(request.body)

        # Validate required fields
        business_type = data.get('business_type', '').strip()
        location = data.get('location', '').strip()
        startup_budget = data.get('startup_budget')
        # Accept either backend keys (fixed_costs/variable_costs) or older names (fixed_cost/variable_cost)
        _fixed = data.get('fixed_costs', data.get('fixed_cost', ''))
        if isinstance(_fixed, str):
            fixed_costs = _fixed.strip()
        else:
            fixed_costs = _fixed

        _variable = data.get('variable_costs', data.get('variable_cost', ''))
        if isinstance(_variable, str):
            variable_costs = _variable.strip()
        else:
            variable_costs = _variable
        monthly_sales_volume = data.get('monthly_sales_volume')
        # Numeric/text fields: tolerate numbers or strings
        _cpu = data.get('cost_per_unit', '')
        cost_per_unit = _cpu.strip() if isinstance(_cpu, str) else _cpu

        _tsp = data.get('target_selling_price', '')
        target_selling_price = _tsp.strip() if isinstance(_tsp, str) else _tsp

        _expected = data.get('expected_sales_volume', '')
        expected_sales_volume = _expected.strip() if isinstance(_expected, str) else _expected

        _th = data.get('time_horizon', '6 months')
        time_horizon = _th.strip() if isinstance(_th, str) else _th

        errors = []
        if not business_type:
            errors.append("Business type is required.")
        if not location:
            errors.append("Location is required.")
        if not startup_budget or float(startup_budget) <= 0:
            errors.append("Startup budget must be greater than zero.")
        if not monthly_sales_volume or float(monthly_sales_volume) <= 0:
            errors.append("Expected monthly sales volume must be greater than zero.")

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Check Groq API key
        groq_api_key = settings.GROQ_API_KEY  # reuse env variable if you like
        if not groq_api_key:
            return JsonResponse({
                'success': False,
                'errors': ['Groq API key is not configured.']
            }, status=500)

        # Prepare system and user prompts
        system_prompt = prompt_system
#         system_prompt = """You are a business reality check advisor. Your role is to:
# 1. Explain whether the business inputs appear realistic based on common business knowledge
# 2. Highlight obvious risks or weak assumptions in the business idea
# 3. Ask clarifying questions if information seems vague or incomplete
# 4. Provide practical, grounded feedback

# Important constraints:
# - Do NOT calculate revenue, profit, or make financial predictions
# - Do NOT give financial guarantees or specific numbers
# - Do NOT provide investment advice
# - Focus only on the realism and potential challenges of the inputs provided

# Format:
# - Start with a brief assessment of the overall realism
# - List any concerns or risks you identify
# - End with 2-3 clarifying questions if relevant
# """

        user_prompt = prompt_user(business_type,location,startup_budget,monthly_sales_volume,fixed_costs,variable_costs,cost_per_unit,target_selling_price,expected_sales_volume,time_horizon)

        # Call Groq API via your utility function
        ai_response_raw = get_groq_completion(
            system_prompt=system_prompt,
            prompt=user_prompt,
            api_key=groq_api_key
        )

        # Parse the AI response to separate explanation and questions
        lines = ai_response_raw.split('\n')
        explanation_lines = []
        questions = []
        in_questions = False

        for line in lines:
            line_lower = line.lower().strip()
            if 'clarifying question' in line_lower or 'questions:' in line_lower or 'consider:' in line_lower:
                in_questions = True
                continue
            if in_questions and line.strip().startswith(('-', '•', '*', '1', '2', '3', '4', '5')):
                question = line.strip().lstrip('-•*0123456789.) ').strip()
                if question:
                    questions.append(question)
            elif not in_questions:
                explanation_lines.append(line)

        explanation = '\n'.join(explanation_lines).strip()

        return JsonResponse({
            'success': True,
            'explanation': explanation,
            'questions': questions,
            'disclaimer': 'This tool provides decision support only. The analysis is based on general business knowledge and does not constitute financial advice. No guarantees are made about business outcomes.'
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'errors': ['Invalid JSON in request body.']}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'errors': [f'An error occurred: {str(e)}']}, status=500)
