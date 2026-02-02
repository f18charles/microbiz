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
        business_type: document.getElementById('id_business_type'),
        location: document.getElementById('id_location'),
        C_start: document.getElementById('id_C_start'),
        T: document.getElementById('id_T'),
        P: document.getElementById('id_P'),
        Q: document.getElementById('id_Q'),
        g: document.getElementById('id_g'),
        E_fix: document.getElementById('id_E_fix'),
        E_var: document.getElementById('id_E_var'),
        initial_inventory_units: document.getElementById('id_initial_inventory_units'),
    };
    
    // Error elements
    const errors = {
        business_type: document.getElementById('id_business_type_error'),
        location: document.getElementById('id_location_error'),
        C_start: document.getElementById('id_C_start_error'),
        T: document.getElementById('id_T_error'),
        P: document.getElementById('id_P_error'),
        Q: document.getElementById('id_Q_error'),
        g: document.getElementById('id_g_error'),
        E_fix: document.getElementById('id_E_fix_error'),
        E_var: document.getElementById('id_E_var_error'),
        initial_inventory_units: document.getElementById('id_initial_inventory_units_error'),
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
        C_start: false,
        T: false,
        P: false,
        Q: false,
        g: false,
        E_fix: false,
        E_var: false,
        initial_inventory_units: false
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
            case 'C_start':
                const budget = parseFloat(value);
                isValid = !isNaN(budget) && budget > 0;
                errorMessage = isValid ? '' : 'Capital must be greater than zero.';
                break;
            case 'T':
                const sales = parseFloat(value);
                isValid = !isNaN(sales) && sales > 0;
                errorMessage = isValid ? '' : 'Time horizon must be greater than zero.';
                break;
            case 'P':
                const fixed = parseFloat(value);
                isValid = !isNaN(fixed) && fixed >= 0;
                errorMessage = isValid ? '' : 'The selling price must be 0 or greater.';
                break;
            case 'Q':
                const variable = parseFloat(value);
                isValid = !isNaN(variable) && variable >= 0;
                errorMessage = isValid ? '' : 'Quantity must be 0 or greater.';
                break;
            case 'g':
                const cpu = parseFloat(value);
                isValid = !isNaN(cpu) && cpu >= 0;
                errorMessage = isValid ? '' : 'Growth rate per unit must be 0 or greater.';
                break;
            case 'E_fix':
                const tsp = parseFloat(value);
                isValid = !isNaN(tsp) && tsp >= 0;
                errorMessage = isValid ? '' : 'Target selling price must be 0 or greater.';
                break;
            case 'E_var':
                const variable_e = parseFloat(value);
                isValid = !isNaN(variable_e) && variable_e >= 0;
                errorMessage = isValid ? '' : 'Variable expenses is required.';
                break;
            case 'initial_inventory_units':
                isValid = value.length > 0;
                errorMessage = isValid ? '' : 'Time horizon is required.';
                break;
            case 'monthly_sales_volume':
                isValid = value.length > 0;
                errorMessage = isValid ? '' : 'Monnthly sales volume is required.';
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
        console.log('SUBMIT FIRED')
        e.preventDefault();
        
        // Validate all fields first
        if (!validateAll()) {
            return;
        }
        
        setLoading(true);
        
        // Prepare data (keys match backend expectations)
        const data = {
            business_type: inputs.business_type.value.trim(),
            location: inputs.location.value.trim(),
            C_start: parseFloat(inputs.C_start.value),
            T: parseFloat(inputs.T.value),
            P: parseFloat(inputs.P.value),
            Q: parseFloat(inputs.Q.value),
            g: parseFloat(inputs.g.value),
            E_fix: parseFloat(inputs.E_fix.value),
            E_var: parseFloat(inputs.E_var.value),
            initial_inventory_units: inputs.initial_inventory_units.value.trim()
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
