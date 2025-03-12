"""
Tests for the main module.
"""
import pytest
from src.main import main


def test_main_runs_without_error():
    """
    Test that the main function runs without raising an exception.
    """
    # This test simply ensures the main function doesn't raise an exception
    main()


def test_example():
    """
    An example test case.
    """
    assert True, "This test should always pass" 