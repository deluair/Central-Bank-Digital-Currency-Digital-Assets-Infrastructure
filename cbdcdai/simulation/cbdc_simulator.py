"""
CBDC Simulator Module

This module provides the core simulation capabilities for CBDC operations,
including monetary policy transmission, cross-border payments, and financial stability analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

class CBDCParameters(BaseModel):
    """Parameters for CBDC simulation"""
    interest_rate: float = Field(..., description="CBDC interest rate")
    reserve_requirement: float = Field(..., description="Reserve requirement ratio")
    transaction_limit: float = Field(..., description="Per transaction limit")
    holding_limit: float = Field(..., description="Maximum holding limit")
    privacy_level: float = Field(..., description="Privacy level (0-1)")
    cross_border_enabled: bool = Field(..., description="Cross-border functionality enabled")

class EconomicIndicators(BaseModel):
    """Economic indicators for simulation"""
    gdp_growth: float
    inflation_rate: float
    unemployment_rate: float
    exchange_rate: float
    money_supply: float
    bank_deposits: float

class CBDCSimulator:
    """Core CBDC simulation engine"""
    
    def __init__(self, parameters: CBDCParameters):
        self.parameters = parameters
        self.simulation_data = {}
        self.economic_indicators = None
        
    def initialize_economic_indicators(self, indicators: EconomicIndicators):
        """Initialize economic indicators for simulation"""
        self.economic_indicators = indicators
        
    def simulate_monetary_transmission(self, 
                                     policy_rate_change: float,
                                     simulation_periods: int = 12) -> pd.DataFrame:
        """
        Simulate monetary policy transmission through CBDC
        
        Args:
            policy_rate_change: Change in policy rate
            simulation_periods: Number of periods to simulate
            
        Returns:
            DataFrame with simulation results
        """
        # Initialize results
        results = []
        current_rate = self.parameters.interest_rate
        
        for period in range(simulation_periods):
            # Calculate transmission effects
            cbdc_rate = current_rate + policy_rate_change * (1 - np.exp(-period/3))
            deposit_rate = cbdc_rate * 0.8  # Commercial bank deposit rate adjustment
            lending_rate = deposit_rate + 2.0  # Commercial bank lending rate
            
            # Calculate economic impacts
            money_velocity = 1.5 * (1 + 0.1 * (cbdc_rate - current_rate))
            inflation_impact = -0.2 * policy_rate_change * (1 - np.exp(-period/6))
            
            results.append({
                'period': period,
                'cbdc_rate': cbdc_rate,
                'deposit_rate': deposit_rate,
                'lending_rate': lending_rate,
                'money_velocity': money_velocity,
                'inflation_impact': inflation_impact
            })
            
        return pd.DataFrame(results)
    
    def simulate_cross_border_payment(self,
                                    amount: float,
                                    source_currency: str,
                                    target_currency: str,
                                    exchange_rate: float) -> Dict:
        """
        Simulate cross-border CBDC payment
        
        Args:
            amount: Payment amount
            source_currency: Source currency code
            target_currency: Target currency code
            exchange_rate: Exchange rate between currencies
            
        Returns:
            Dictionary with payment simulation results
        """
        # Validate transaction limits
        if amount > self.parameters.transaction_limit:
            raise ValueError("Transaction amount exceeds limit")
            
        # Calculate settlement time (simplified model)
        base_settlement_time = 2  # minutes
        network_load_factor = 1 + 0.1 * np.random.random()
        settlement_time = base_settlement_time * network_load_factor
        
        # Calculate fees
        base_fee = 0.001  # 0.1%
        cross_border_fee = 0.002  # 0.2%
        total_fee = amount * (base_fee + cross_border_fee)
        
        return {
            'amount': amount,
            'source_currency': source_currency,
            'target_currency': target_currency,
            'exchange_rate': exchange_rate,
            'settlement_time': settlement_time,
            'fees': total_fee,
            'final_amount': (amount - total_fee) * exchange_rate
        }
    
    def simulate_financial_stability(self,
                                   simulation_periods: int = 12) -> pd.DataFrame:
        """
        Simulate financial stability impacts of CBDC
        
        Args:
            simulation_periods: Number of periods to simulate
            
        Returns:
            DataFrame with stability metrics
        """
        results = []
        
        for period in range(simulation_periods):
            # Simulate bank deposit migration
            deposit_migration = 0.1 * (1 - np.exp(-period/4))  # Gradual migration to CBDC
            
            # Calculate stability metrics
            bank_funding_cost = 0.02 + 0.01 * deposit_migration
            interbank_liquidity = 1.0 - 0.2 * deposit_migration
            payment_system_resilience = 0.95 + 0.05 * (1 - deposit_migration)
            
            results.append({
                'period': period,
                'deposit_migration': deposit_migration,
                'bank_funding_cost': bank_funding_cost,
                'interbank_liquidity': interbank_liquidity,
                'payment_system_resilience': payment_system_resilience
            })
            
        return pd.DataFrame(results)
    
    def simulate_crisis_scenario(self,
                               scenario_type: str,
                               severity: float = 0.5) -> Dict:
        """
        Simulate crisis scenarios
        
        Args:
            scenario_type: Type of crisis scenario
            severity: Severity of the crisis (0-1)
            
        Returns:
            Dictionary with crisis simulation results
        """
        scenarios = {
            'bank_run': {
                'deposit_withdrawal_rate': 0.3 * severity,
                'liquidity_impact': 0.4 * severity,
                'system_stress': 0.5 * severity
            },
            'cyber_attack': {
                'system_availability': 1 - 0.3 * severity,
                'transaction_delay': 5 * severity,
                'recovery_time': 24 * severity
            },
            'regulatory_change': {
                'compliance_cost': 1000000 * severity,
                'implementation_time': 30 * severity,
                'market_impact': 0.2 * severity
            }
        }
        
        if scenario_type not in scenarios:
            raise ValueError(f"Unknown scenario type: {scenario_type}")
            
        return scenarios[scenario_type]

# Example usage
if __name__ == "__main__":
    # Initialize simulator with parameters
    params = CBDCParameters(
        interest_rate=0.02,
        reserve_requirement=0.1,
        transaction_limit=1000000,
        holding_limit=10000000,
        privacy_level=0.7,
        cross_border_enabled=True
    )
    
    simulator = CBDCSimulator(params)
    
    # Initialize economic indicators
    indicators = EconomicIndicators(
        gdp_growth=0.03,
        inflation_rate=0.02,
        unemployment_rate=0.05,
        exchange_rate=1.0,
        money_supply=1000000000,
        bank_deposits=800000000
    )
    
    simulator.initialize_economic_indicators(indicators)
    
    # Run simulations
    monetary_transmission = simulator.simulate_monetary_transmission(0.01)
    cross_border = simulator.simulate_cross_border_payment(
        100000, 'USD', 'EUR', 0.85
    )
    stability = simulator.simulate_financial_stability()
    crisis = simulator.simulate_crisis_scenario('bank_run', 0.7) 