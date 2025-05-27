"""
Risk Analytics Module

This module provides comprehensive risk assessment and monitoring capabilities
for CBDC operations, including systemic risk, operational risk, and market risk analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

class RiskMetrics(BaseModel):
    """Risk metrics for CBDC operations"""
    var_95: float = Field(..., description="95% Value at Risk")
    var_99: float = Field(..., description="99% Value at Risk")
    expected_shortfall: float = Field(..., description="Expected Shortfall")
    liquidity_risk: float = Field(..., description="Liquidity Risk Score")
    operational_risk: float = Field(..., description="Operational Risk Score")
    systemic_risk: float = Field(..., description="Systemic Risk Score")

class RiskAnalytics:
    """Risk analytics engine for CBDC operations"""
    
    def __init__(self):
        self.risk_metrics = {}
        self.historical_data = pd.DataFrame()
        
    def calculate_var(self, 
                     returns: np.ndarray,
                     confidence_level: float = 0.95) -> float:
        """
        Calculate Value at Risk
        
        Args:
            returns: Array of historical returns
            confidence_level: Confidence level for VaR calculation
            
        Returns:
            Value at Risk
        """
        return np.percentile(returns, (1 - confidence_level) * 100)
    
    def calculate_expected_shortfall(self,
                                   returns: np.ndarray,
                                   var: float) -> float:
        """
        Calculate Expected Shortfall (Conditional VaR)
        
        Args:
            returns: Array of historical returns
            var: Value at Risk threshold
            
        Returns:
            Expected Shortfall
        """
        return np.mean(returns[returns <= var])
    
    def assess_liquidity_risk(self,
                            trading_volume: float,
                            market_cap: float,
                            bid_ask_spread: float) -> float:
        """
        Assess liquidity risk
        
        Args:
            trading_volume: Daily trading volume
            market_cap: Market capitalization
            bid_ask_spread: Bid-ask spread
            
        Returns:
            Liquidity risk score (0-1)
        """
        # Calculate liquidity metrics
        turnover_ratio = trading_volume / market_cap
        spread_impact = bid_ask_spread / (1 + bid_ask_spread)
        
        # Combine metrics into risk score
        risk_score = 0.7 * (1 - turnover_ratio) + 0.3 * spread_impact
        return min(max(risk_score, 0), 1)
    
    def assess_operational_risk(self,
                              system_uptime: float,
                              transaction_volume: float,
                              error_rate: float) -> float:
        """
        Assess operational risk
        
        Args:
            system_uptime: System uptime percentage
            transaction_volume: Daily transaction volume
            error_rate: Transaction error rate
            
        Returns:
            Operational risk score (0-1)
        """
        # Calculate operational metrics
        availability_risk = 1 - system_uptime
        volume_risk = min(transaction_volume / 1000000, 1)  # Normalize to 1M transactions
        error_risk = error_rate
        
        # Combine metrics into risk score
        risk_score = 0.4 * availability_risk + 0.3 * volume_risk + 0.3 * error_risk
        return min(max(risk_score, 0), 1)
    
    def assess_systemic_risk(self,
                           network_size: int,
                           concentration_ratio: float,
                           interdependency_score: float) -> float:
        """
        Assess systemic risk
        
        Args:
            network_size: Number of participants in the network
            concentration_ratio: Market concentration ratio
            interdependency_score: Network interdependency score
            
        Returns:
            Systemic risk score (0-1)
        """
        # Calculate systemic risk metrics
        size_risk = 1 - (1 / (1 + np.exp(-network_size/1000)))  # Sigmoid function
        concentration_risk = concentration_ratio
        interdependency_risk = interdependency_score
        
        # Combine metrics into risk score
        risk_score = 0.3 * size_risk + 0.4 * concentration_risk + 0.3 * interdependency_risk
        return min(max(risk_score, 0), 1)
    
    def generate_risk_report(self,
                           returns: np.ndarray,
                           trading_metrics: Dict,
                           operational_metrics: Dict,
                           systemic_metrics: Dict) -> RiskMetrics:
        """
        Generate comprehensive risk report
        
        Args:
            returns: Historical returns
            trading_metrics: Trading-related metrics
            operational_metrics: Operational metrics
            systemic_metrics: Systemic risk metrics
            
        Returns:
            RiskMetrics object with comprehensive risk assessment
        """
        # Calculate VaR metrics
        var_95 = self.calculate_var(returns, 0.95)
        var_99 = self.calculate_var(returns, 0.99)
        expected_shortfall = self.calculate_expected_shortfall(returns, var_95)
        
        # Calculate risk scores
        liquidity_risk = self.assess_liquidity_risk(
            trading_metrics['volume'],
            trading_metrics['market_cap'],
            trading_metrics['spread']
        )
        
        operational_risk = self.assess_operational_risk(
            operational_metrics['uptime'],
            operational_metrics['volume'],
            operational_metrics['error_rate']
        )
        
        systemic_risk = self.assess_systemic_risk(
            systemic_metrics['network_size'],
            systemic_metrics['concentration'],
            systemic_metrics['interdependency']
        )
        
        return RiskMetrics(
            var_95=var_95,
            var_99=var_99,
            expected_shortfall=expected_shortfall,
            liquidity_risk=liquidity_risk,
            operational_risk=operational_risk,
            systemic_risk=systemic_risk
        )

# Example usage
if __name__ == "__main__":
    # Initialize risk analytics
    risk_engine = RiskAnalytics()
    
    # Generate sample data
    returns = np.random.normal(0.0001, 0.02, 1000)  # Daily returns
    
    trading_metrics = {
        'volume': 1000000,
        'market_cap': 10000000,
        'spread': 0.001
    }
    
    operational_metrics = {
        'uptime': 0.999,
        'volume': 500000,
        'error_rate': 0.0001
    }
    
    systemic_metrics = {
        'network_size': 100,
        'concentration': 0.3,
        'interdependency': 0.4
    }
    
    # Generate risk report
    risk_report = risk_engine.generate_risk_report(
        returns,
        trading_metrics,
        operational_metrics,
        systemic_metrics
    ) 