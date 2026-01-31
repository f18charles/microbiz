from django import forms


class RealityCheckForm(forms.Form):
    # Business context
    business_type = forms.CharField(
        label="Business Type",
        max_length=100
    )

    location = forms.CharField(
        label="Location",
        max_length=100
    )

    # 1. Capital and time
    C_start = forms.FloatField(
        label="Starting Capital",
        min_value=0
    )

    T = forms.IntegerField(
        label="Time Horizon (months)",
        min_value=1
    )

    # 2. Pricing and sales
    P = forms.FloatField(
        label="Unit Selling Price",
        min_value=0
    )

    Q = forms.IntegerField(
        label="Expected Sales Volume (units per month)",
        min_value=0
    )

    g = forms.FloatField(
        label="Monthly Growth Rate",
        required=False,
        min_value=0,
        help_text="Optional. Example: 0.05 for 5%"
    )

    # 3. Costs
    E_var = forms.FloatField(
        label="Variable Expenses (monthly)",
        min_value=0
    )

    E_fix = forms.FloatField(
        label="Fixed Expenses (monthly)",
        min_value=0
    )

    C_startup = forms.FloatField(
        label="One-time Startup Costs",
        min_value=0
    )

    initial_inventory_units = forms.IntegerField(
        label="Initial Inventory (units)",
        min_value=0
    )

    contingency_percent = forms.FloatField(
        label="Contingency Fund (% of capital)",
        min_value=0,
        max_value=100
    )

    # 4. Customers and marketing (optional)
    target_customers = forms.IntegerField(
        label="Target Number of Customers (monthly)",
        required=False,
        min_value=0
    )

    marketing_budget = forms.FloatField(
        label="Marketing Budget (monthly)",
        required=False,
        min_value=0
    )
