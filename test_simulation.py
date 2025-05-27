"""
Test script to verify CBDCDAI simulation functionality
"""

from cbdcdai.simulation.economic_models import EconomicModels, EconomicParameters
import pandas as pd
import numpy as np

def test_simulation():
    # Initialize economic models
    params = EconomicParameters(
        natural_rate=0.02,
        inflation_target=0.02,
        output_gap_weight=0.5,
        inflation_weight=1.5,
        money_velocity=1.5,
        fiscal_multiplier=1.0
    )
    
    models = EconomicModels(params)
    
    # Test Taylor Rule
    interest_rate = models.taylor_rule(
        inflation_rate=0.03,
        output_gap=0.01
    )
    print(f"Taylor Rule Interest Rate: {interest_rate:.4f}")
    
    # Test Phillips Curve
    inflation = models.phillips_curve(
        unemployment_rate=0.05,
        expected_inflation=0.02
    )
    print(f"Phillips Curve Inflation: {inflation:.4f}")
    
    # Test IS-LM Model
    output, interest = models.is_lm_model(
        interest_rate=0.02,
        government_spending=1000,
        money_supply=5000,
        cbdc_adoption=0.1
    )
    print(f"IS-LM Output: {output:.2f}")
    print(f"IS-LM Interest Rate: {interest:.4f}")
    
    # Test Money Multiplier
    multiplier = models.money_multiplier(
        reserve_ratio=0.1,
        currency_ratio=0.2,
        cbdc_ratio=0.1
    )
    print(f"Money Multiplier: {multiplier:.4f}")
    
    # Run full simulation
    initial_conditions = {
        'interest_rate': 0.02,
        'inflation': 0.02,
        'output': 1000,
        'potential_output': 1000,
        'unemployment': 0.05,
        'cbdc_adoption': 0.1,
        'reserve_ratio': 0.1,
        'currency_ratio': 0.2
    }
    
    results = models.simulate_monetary_impact(
        initial_conditions=initial_conditions,
        policy_shock=0.01,
        periods=12
    )
    
    print("\nSimulation Results:")
    print(results.to_string())
    
    return results

if __name__ == "__main__":
    test_simulation() 