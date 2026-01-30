/**
 * MicroBiz Reality Check Agent - Frontend Application
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('reality-check-form');
    const submitBtn = document.getElementById('submit-btn');
    const buttonText = submitBtn.querySelector('.button-text');
    const spinner = submitBtn.querySelector('.spinner');
    
    // Input elements
    const inputs = {
        business_type: document.getElementById('business_type'),
        location: document.getElementById('location'),
        startup_budget: document.getElementById('startup_budget'),
        monthly_sales_volume: document.getElementById('monthly_sales_volume')
    };
    
    // Error elements
    const errors = {
        business_type: document.getElementById('business_type_error'),
        location: document.getElementById('location_error'),
        startup_budget: document.getElementById('startup_budget_error'),
        monthly_sales_volume: document.getElementById('monthly_sales_volume_error')
    };
    
    // Results elements
    const resultsSection = document.getElementById('results');
    const explanationContent = document.getElementById('explanation-content');
    const questionsSection = document.getElementById('questions-section');
    const questionsList = document.getElementById('questions-list');
    const disclaimerText = document.getElementById('disclaimer-text');
    
    // Error section
    const errorSection = document.getElementById('error-section');
    const errorList = document.getElementById('error-list');
    
    // Validation state
    const validationState = {
        business_type: false,
        location: false,
        startup_budget: false,
        monthly_sales_volume: false
    };
    
    /**
     * Validate a single field
     */
    function validateField(fieldName) {
        const input = inputs[fieldName];
        const errorEl = errors[fieldName];
        const value = input.value.trim();
        
        let isValid = false;
        let errorMessage = '';
        
        switch (fieldName) {
            case 'business_type':
                isValid = value.length > 0;
                errorMessage = isValid ? '' : 'Business type is required.';
                break;
            case 'location':
                isValid = value.length > 0;
                errorMessage = isValid ? '' : 'Location is required.';
                break;
            case 'startup_budget':
                const budget = parseFloat(value);
                isValid = !isNaN(budget) && budget > 0;
                errorMessage = isValid ? '' : 'Startup budget must be greater than zero.';
                break;
            case 'monthly_sales_volume':
                const sales = parseFloat(value);
                isValid = !isNaN(sales) && sales > 0;
                errorMessage = isValid ? '' : 'Expected monthly sales must be greater than zero.';
                break;
        }
        
        validationState[fieldName] = isValid;
        
        // Update UI
        if (value.length > 0 || input === document.activeElement) {
            input.classList.toggle('invalid', !isValid);
            errorEl.textContent = errorMessage;
        } else {
            input.classList.remove('invalid');
            errorEl.textContent = '';
        }
        
        updateSubmitButton();
        return isValid;
    }
    
    /**
     * Validate all fields
     */
    function validateAll() {
        let allValid = true;
        for (const fieldName in inputs) {
            if (!validateField(fieldName)) {
                allValid = false;
            }
        }
        return allValid;
    }
    
    /**
     * Update submit button state
     */
    function updateSubmitButton() {
        const allValid = Object.values(validationState).every(v => v === true);
        submitBtn.disabled = !allValid;
    }
    
    /**
     * Show loading state
     */
    function setLoading(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            buttonText.textContent = 'Analyzing...';
            spinner.classList.remove('hidden');
        } else {
            updateSubmitButton();
            buttonText.textContent = 'Run Reality Check';
            spinner.classList.add('hidden');
        }
    }
    
    /**
     * Display results
     */
    function showResults(data) {
        // Hide error section
        errorSection.classList.add('hidden');
        
        // Show explanation
        explanationContent.textContent = data.explanation;
        
        // Show questions if any
        if (data.questions && data.questions.length > 0) {
            questionsList.innerHTML = '';
            data.questions.forEach(question => {
                const li = document.createElement('li');
                li.textContent = question;
                questionsList.appendChild(li);
            });
            questionsSection.classList.remove('hidden');
        } else {
            questionsSection.classList.add('hidden');
        }
        
        // Show disclaimer
        disclaimerText.textContent = data.disclaimer;
        
        // Show results section
        resultsSection.classList.remove('hidden');
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    /**
     * Display errors
     */
    function showErrors(errorMessages) {
        // Hide results section
        resultsSection.classList.add('hidden');
        
        // Populate error list
        errorList.innerHTML = '';
        errorMessages.forEach(error => {
            const li = document.createElement('li');
            li.textContent = error;
            errorList.appendChild(li);
        });
        
        // Show error section
        errorSection.classList.remove('hidden');
        
        // Scroll to error section
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    /**
     * Handle form submission
     */
    async function handleSubmit(e) {
        e.preventDefault();
        
        // Validate all fields first
        if (!validateAll()) {
            return;
        }
        
        setLoading(true);
        
        // Prepare data
        const data = {
            business_type: inputs.business_type.value.trim(),
            location: inputs.location.value.trim(),
            startup_budget: parseFloat(inputs.startup_budget.value),
            monthly_sales_volume: parseFloat(inputs.monthly_sales_volume.value)
        };
        
        try {
            const response = await fetch('/api/analyze/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showResults(result);
            } else {
                showErrors(result.errors || ['An unexpected error occurred.']);
            }
        } catch (error) {
            showErrors(['Failed to connect to the server. Please try again.']);
        } finally {
            setLoading(false);
        }
    }
    
    // Attach event listeners
    for (const fieldName in inputs) {
        inputs[fieldName].addEventListener('input', () => validateField(fieldName));
        inputs[fieldName].addEventListener('blur', () => validateField(fieldName));
    }
    
    form.addEventListener('submit', handleSubmit);
    
    // Initial validation check
    updateSubmitButton();
});
