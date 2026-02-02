"""
Views for the Reality Check app using Groq AI.
"""

import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .forms import RealityCheckForm
from .utils import get_groq_completion  # Your Groq API utility function
from .prompt import prompt_system, prompt_user  # Importing the system prompt


def index(request):
    """Render the main page."""
    return render(request, 'index.html')

def dash(request):
    """Render the main page."""
    return render(request, 'dash.html')

def login(request):
    """Render the main page."""
    return render(request, 'login.html')

def signup(request):
    """Render the main page."""
    return render(request, 'signup.html')

def trials(request):
    """Render the main page."""
    form = RealityCheckForm()
    
    return render(request, 'trials.html', {'form': form})

def test(request):
    """Render the main page."""
    return render(request, 'test.html')




@csrf_exempt
@require_http_methods(["POST"])
def analyze(request):
    """
    API endpoint to analyze business inputs using Groq AI.
    """
    try:
        # Parse JSON body
        data = json.loads(request.body)

        """
        inputs
        1. Capital and time
        C_start - starting capital
        T - time horizon for analysis (months)
        
        2. Pricing and sales
        P - unit selling price
        Q - expected sales volume (units per month)
        g - growth rate(optional) per month
        
        3. Costs
        E_var - variable expenses 
        E_fix - fixed expenses
        C_startup- one-time startup costs (equipment, licenses, initial inventory)
        - initial inventory (units)
        - contingency fund (% of capital)
        
        4. customers and marketing(optional but helpful)
        - target no. of customers(monthly)
        - marketing budget (monthly)
        
        other
        business type
        location
        """

        form = RealityCheckForm(data)
        
        if form.is_valid():
            business_type = form.cleaned_data['business_type']
            location = form.cleaned_data['location']
            capital = form.cleaned_data['C_start']
            time_horizon = form.cleaned_data['T']
            target_selling_price = form.cleaned_data['P']
            monthly_sales_volume = form.cleaned_data['Q']
            expected_growth_rate = form.cleaned_data['g']
            fixed_costs = form.cleaned_data['E_fix']
            variable_costs = form.cleaned_data['E_var']
            initial_inventory_units = form.cleaned_data['initial_inventory_units']  # Assuming expected sales volume is same as monthly sales volume
            
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        
        
        # Check Groq API key
        groq_api_key = settings.GROQ_API_KEY  # reuse env variable if you like
        if not groq_api_key:
            return JsonResponse({
                'success': False,
                'errors': ['Groq API key is not configured.']
            }, status=500)

        # Prepare system and user prompts
        system_prompt = prompt_system

        user_prompt = prompt_user(
            expected_growth_rate,
            business_type,
            location,
            capital,
            time_horizon,
            target_selling_price,
            monthly_sales_volume,
            fixed_costs,
            variable_costs,
            initial_inventory_units)

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
