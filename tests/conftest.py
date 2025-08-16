"""
Pytest configuration and fixtures for cognitive framework tests
"""

import pytest
import sys
import os
from pathlib import Path


@pytest.fixture(scope="session")
def project_root():
    """Fixture providing the project root directory"""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session") 
def framework_config():
    """Fixture providing framework configuration for tests"""
    return {
        'consciousness_threshold': 0.7,
        'temporal_stability_min': 0.8,
        'information_integration_min': 3.0,
        'complexity_tolerance': 0.2,
        'performance_timeout': 1.0
    }


@pytest.fixture(scope="function")
def mock_consciousness_data():
    """Fixture providing mock consciousness assessment data"""
    return {
        'awareness_score': 0.87,
        'temporal_stability': 0.94,
        'information_integration': 4.2,
        'self_awareness': 0.73,
        'coherence': 0.82,
        'stability': 0.78,
        'emergence': 0.85
    }


@pytest.fixture(scope="function")
def mock_mecn_parameters():
    """Fixture providing mock MECN framework parameters"""
    return {
        'alpha_t': 0.7,
        'lambda_1': 0.3,
        'lambda_2': 0.4,
        'beta': 0.5
    }


@pytest.fixture(scope="function")
def mock_autopoietic_system():
    """Fixture providing mock autopoietic system data"""
    return {
        'components': ['processor', 'memory', 'feedback_loop'],
        'connections': [
            ('processor', 'memory'),
            ('memory', 'feedback_loop'),
            ('feedback_loop', 'processor')
        ],
        'maintenance_active': True,
        'boundary_stability': 0.8
    }


@pytest.fixture(scope="function")
def complexity_test_data():
    """Fixture providing complexity analysis test data"""
    return {
        'sizes': [100, 500, 1000, 2000, 5000],
        'expected_complexity': 'O(n log n)',
        'tolerance': 0.2,
        'reference_data': {
            100: {'theoretical': 664, 'empirical': 664},
            1000: {'theoretical': 9966, 'empirical': 9966},
            10000: {'theoretical': 132877, 'empirical': 132877}
        }
    }


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
            
        # Mark performance tests as slow
        if "performance" in str(item.fspath) or "complexity" in item.name.lower():
            item.add_marker(pytest.mark.slow)
