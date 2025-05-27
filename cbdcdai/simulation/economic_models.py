"""
Economic Models

Advanced economic models for CBDC simulation, including:
- IS-LM model adaptation for CBDC
- Phillips Curve analysis
- Taylor Rule implementation
- Money Multiplier effects
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

class EconomicParameters(BaseModel):
    """Parameters for economic models"""
    natural_rate: float = Field(..., description="Natural rate of interest")
    inflation_target: float = Field(..., description="Inflation target")
    output_gap_weight: float = Field(..., description="Output gap weight in Taylor rule")
    inflation_weight: float = Field(..., description="Inflation weight in Taylor rule")
    money_velocity: float = Field(..., description="Money velocity")
    fiscal_multiplier: float = Field(..., description="Fiscal multiplier")

class EconomicModels:
    """Economic models for CBDC simulation"""
    
    def __init__(self, parameters: EconomicParameters):
        self.parameters = parameters
        
    def taylor_rule(self,
                   inflation_rate: float,
                   output_gap: float,
                   natural_rate: Optional[float] = None) -> float:
        """
        Calculate interest rate using Taylor Rule
        
        Args:
            inflation_rate: Current inflation rate
            output_gap: Output gap (actual - potential)
            natural_rate: Natural rate of interest (optional)
            
        Returns:
            Recommended interest rate
        """
        natural_rate = natural_rate or self.parameters.natural_rate
        
        return (natural_rate + 
                self.parameters.inflation_weight * (inflation_rate - self.parameters.inflation_target) +
                self.parameters.output_gap_weight * output_gap)
    
    def phillips_curve(self,
                      unemployment_rate: float,
                      expected_inflation: float,
                      supply_shock: float = 0.0) -> float:
        """
        Calculate inflation using Phillips Curve
        
        Args:
            unemployment_rate: Current unemployment rate
            expected_inflation: Expected inflation rate
            supply_shock: Supply shock impact
            
        Returns:
            Inflation rate
        """
        # Simplified Phillips Curve with supply shock
        return (expected_inflation - 
                0.5 * (unemployment_rate - 0.05) +  # 5% natural rate of unemployment
                supply_shock)
    
    def is_lm_model(self,
                   interest_rate: float,
                   government_spending: float,
                   money_supply: float,
                   cbdc_adoption: float) -> Tuple[float, float]:
        """
        Calculate equilibrium using IS-LM model with CBDC
        
        Args:
            interest_rate: Current interest rate
            government_spending: Government spending
            money_supply: Money supply
            cbdc_adoption: CBDC adoption rate
            
        Returns:
            Tuple of (equilibrium output, equilibrium interest rate)
        """
        # IS curve parameters
        autonomous_spending = 1000
        marginal_propensity_consume = 0.8
        investment_sensitivity = 50
        
        # LM curve parameters
        money_demand_sensitivity = 0.5
        money_demand_autonomous = 500
        
        # CBDC impact on money demand
        cbdc_impact = 1 + 0.2 * cbdc_adoption
        
        # IS curve: Y = C + I + G
        is_output = (autonomous_spending + 
                    marginal_propensity_consume * government_spending -
                    investment_sensitivity * interest_rate)
        
        # LM curve: M/P = L(Y, r)
        lm_interest = ((money_supply / cbdc_impact - money_demand_autonomous) /
                      (money_demand_sensitivity * is_output))
        
        return is_output, lm_interest
    
    def money_multiplier(self,
                        reserve_ratio: float,
                        currency_ratio: float,
                        cbdc_ratio: float) -> float:
        """
        Calculate money multiplier with CBDC
        
        Args:
            reserve_ratio: Reserve requirement ratio
            currency_ratio: Currency to deposit ratio
            cbdc_ratio: CBDC to deposit ratio
            
        Returns:
            Money multiplier
        """
        # Traditional money multiplier: 1 / (r + c)
        # Modified for CBDC: 1 / (r + c + cbdc)
        return 1 / (reserve_ratio + currency_ratio + cbdc_ratio)
    
    def simulate_monetary_impact(self,
                               initial_conditions: Dict,
                               policy_shock: float,
                               periods: int = 12) -> pd.DataFrame:
        """
        Simulate monetary policy impact with CBDC
        
        Args:
            initial_conditions: Initial economic conditions
            policy_shock: Policy rate change
            periods: Number of periods to simulate
            
        Returns:
            DataFrame with simulation results
        """
        results = []
        
        # Initial conditions
        interest_rate = initial_conditions['interest_rate']
        inflation = initial_conditions['inflation']
        output = initial_conditions['output']
        cbdc_adoption = initial_conditions['cbdc_adoption']
        
        for period in range(periods):
            # Apply policy shock
            interest_rate += policy_shock * (1 - np.exp(-period/3))
            
            # Calculate economic impacts
            output_gap = (output - initial_conditions['potential_output']) / initial_conditions['potential_output']
            inflation = self.phillips_curve(
                initial_conditions['unemployment'],
                inflation,
                supply_shock=0.0
            )
            
            # Calculate CBDC impact
            cbdc_adoption = min(cbdc_adoption + 0.01, 1.0)  # Gradual adoption
            
            # Calculate money multiplier
            multiplier = self.money_multiplier(
                initial_conditions['reserve_ratio'],
                initial_conditions['currency_ratio'],
                cbdc_adoption
            )
            
            results.append({
                'period': period,
                'interest_rate': interest_rate,
                'inflation': inflation,
                'output_gap': output_gap,
                'cbdc_adoption': cbdc_adoption,
                'money_multiplier': multiplier
            })
            
        return pd.DataFrame(results)

# Example usage
if __name__ == "__main__":
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
    
    # Initial conditions
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
    
    # Run simulation
    results = models.simulate_monetary_impact(
        initial_conditions,
        policy_shock=0.01,
        periods=12
    ) 