"""
Advanced Risk Models

Enhanced risk assessment models for CBDC operations, including:
- Network risk analysis
- Liquidity risk modeling
- Operational risk assessment
- Systemic risk analysis
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field
from scipy import stats

class NetworkMetrics(BaseModel):
    """Network risk metrics"""
    node_count: int = Field(..., description="Number of nodes in network")
    edge_count: int = Field(..., description="Number of edges in network")
    average_degree: float = Field(..., description="Average node degree")
    clustering_coefficient: float = Field(..., description="Network clustering coefficient")
    centralization: float = Field(..., description="Network centralization")

class LiquidityMetrics(BaseModel):
    """Liquidity risk metrics"""
    trading_volume: float = Field(..., description="Daily trading volume")
    bid_ask_spread: float = Field(..., description="Average bid-ask spread")
    market_depth: float = Field(..., description="Market depth")
    turnover_ratio: float = Field(..., description="Turnover ratio")
    liquidity_ratio: float = Field(..., description="Liquidity ratio")

class AdvancedRiskModels:
    """Advanced risk assessment models"""
    
    def __init__(self):
        self.network_metrics = {}
        self.liquidity_metrics = {}
        
    def calculate_network_risk(self,
                             adjacency_matrix: np.ndarray) -> NetworkMetrics:
        """
        Calculate network risk metrics
        
        Args:
            adjacency_matrix: Network adjacency matrix
            
        Returns:
            NetworkMetrics object
        """
        # Calculate basic network metrics
        node_count = len(adjacency_matrix)
        edge_count = np.sum(adjacency_matrix) / 2
        degrees = np.sum(adjacency_matrix, axis=1)
        average_degree = np.mean(degrees)
        
        # Calculate clustering coefficient
        triangles = np.trace(np.linalg.matrix_power(adjacency_matrix, 3)) / 6
        possible_triangles = np.sum(degrees * (degrees - 1)) / 2
        clustering_coefficient = triangles / possible_triangles if possible_triangles > 0 else 0
        
        # Calculate network centralization
        max_degree = np.max(degrees)
        centralization = np.sum(max_degree - degrees) / (node_count * (node_count - 1))
        
        return NetworkMetrics(
            node_count=node_count,
            edge_count=edge_count,
            average_degree=average_degree,
            clustering_coefficient=clustering_coefficient,
            centralization=centralization
        )
    
    def calculate_liquidity_risk(self,
                               trading_data: Dict) -> LiquidityMetrics:
        """
        Calculate liquidity risk metrics
        
        Args:
            trading_data: Dictionary containing trading metrics
            
        Returns:
            LiquidityMetrics object
        """
        # Calculate turnover ratio
        turnover_ratio = trading_data['volume'] / trading_data['market_cap']
        
        # Calculate liquidity ratio
        liquidity_ratio = (trading_data['volume'] * 
                         (1 - trading_data['spread'])) / trading_data['market_cap']
        
        return LiquidityMetrics(
            trading_volume=trading_data['volume'],
            bid_ask_spread=trading_data['spread'],
            market_depth=trading_data['depth'],
            turnover_ratio=turnover_ratio,
            liquidity_ratio=liquidity_ratio
        )
    
    def assess_operational_risk(self,
                              system_metrics: Dict) -> float:
        """
        Assess operational risk
        
        Args:
            system_metrics: Dictionary containing system metrics
            
        Returns:
            Operational risk score (0-1)
        """
        # Calculate component risk scores
        availability_risk = 1 - system_metrics['uptime']
        performance_risk = 1 - (system_metrics['response_time'] / system_metrics['target_response_time'])
        security_risk = system_metrics['security_incidents'] / system_metrics['total_incidents']
        
        # Weighted combination of risk scores
        risk_score = (0.4 * availability_risk +
                     0.3 * performance_risk +
                     0.3 * security_risk)
        
        return min(max(risk_score, 0), 1)
    
    def assess_systemic_risk(self,
                           network_metrics: NetworkMetrics,
                           liquidity_metrics: LiquidityMetrics,
                           operational_risk: float) -> float:
        """
        Assess systemic risk
        
        Args:
            network_metrics: Network risk metrics
            liquidity_metrics: Liquidity risk metrics
            operational_risk: Operational risk score
            
        Returns:
            Systemic risk score (0-1)
        """
        # Calculate network risk component
        network_risk = (0.3 * network_metrics.centralization +
                       0.3 * (1 - network_metrics.clustering_coefficient) +
                       0.4 * (network_metrics.average_degree / network_metrics.node_count))
        
        # Calculate liquidity risk component
        liquidity_risk = (0.4 * (1 - liquidity_metrics.liquidity_ratio) +
                         0.3 * liquidity_metrics.bid_ask_spread +
                         0.3 * (1 - liquidity_metrics.turnover_ratio))
        
        # Combine risk components
        systemic_risk = (0.4 * network_risk +
                        0.3 * liquidity_risk +
                        0.3 * operational_risk)
        
        return min(max(systemic_risk, 0), 1)
    
    def stress_test(self,
                   initial_conditions: Dict,
                   shock_scenarios: List[Dict]) -> pd.DataFrame:
        """
        Perform stress testing
        
        Args:
            initial_conditions: Initial economic conditions
            shock_scenarios: List of shock scenarios
            
        Returns:
            DataFrame with stress test results
        """
        results = []
        
        for scenario in shock_scenarios:
            # Apply shock to initial conditions
            shocked_conditions = initial_conditions.copy()
            for key, value in scenario['shocks'].items():
                shocked_conditions[key] *= (1 + value)
            
            # Calculate risk metrics under shocked conditions
            network_risk = self.calculate_network_risk(scenario['network'])
            liquidity_risk = self.calculate_liquidity_risk(shocked_conditions)
            operational_risk = self.assess_operational_risk(shocked_conditions)
            
            # Calculate systemic risk
            systemic_risk = self.assess_systemic_risk(
                network_risk,
                liquidity_risk,
                operational_risk
            )
            
            results.append({
                'scenario': scenario['name'],
                'network_risk': network_risk.centralization,
                'liquidity_risk': liquidity_risk.liquidity_ratio,
                'operational_risk': operational_risk,
                'systemic_risk': systemic_risk
            })
            
        return pd.DataFrame(results)

# Example usage
if __name__ == "__main__":
    # Initialize risk models
    risk_models = AdvancedRiskModels()
    
    # Sample network
    adjacency_matrix = np.array([
        [0, 1, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [0, 1, 1, 0]
    ])
    
    # Calculate network risk
    network_metrics = risk_models.calculate_network_risk(adjacency_matrix)
    
    # Sample trading data
    trading_data = {
        'volume': 1000000,
        'market_cap': 10000000,
        'spread': 0.001,
        'depth': 500000
    }
    
    # Calculate liquidity risk
    liquidity_metrics = risk_models.calculate_liquidity_risk(trading_data)
    
    # Sample system metrics
    system_metrics = {
        'uptime': 0.999,
        'response_time': 0.1,
        'target_response_time': 0.2,
        'security_incidents': 2,
        'total_incidents': 100
    }
    
    # Calculate operational risk
    operational_risk = risk_models.assess_operational_risk(system_metrics)
    
    # Calculate systemic risk
    systemic_risk = risk_models.assess_systemic_risk(
        network_metrics,
        liquidity_metrics,
        operational_risk
    ) 