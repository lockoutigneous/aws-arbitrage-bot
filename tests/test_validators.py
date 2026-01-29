"""
Unit tests for validators module.
"""
import pytest
from utils.validators import (
    validate_mode,
    validate_exchange,
    validate_positive_number,
    validate_positive_integer,
    validate_symbol,
    validate_exchanges_unique
)


class TestValidateMode:
    """Test validate_mode function."""
    
    def test_valid_modes(self):
        """Test that valid modes are accepted."""
        assert validate_mode("fake-money") is True
        assert validate_mode("classic") is True
        assert validate_mode("delta-neutral") is True
    
    def test_invalid_modes(self):
        """Test that invalid modes are rejected."""
        assert validate_mode("invalid") is False
        assert validate_mode("") is False
        assert validate_mode("FAKE-MONEY") is False  # Case sensitive


class TestValidateExchange:
    """Test validate_exchange function."""
    
    def test_valid_exchanges(self):
        """Test that valid exchanges are accepted."""
        assert validate_exchange("binance") is True
        assert validate_exchange("kucoin") is True
        assert validate_exchange("okx") is True
        assert validate_exchange("bybit") is True
    
    def test_case_insensitive(self):
        """Test that exchange validation is case insensitive."""
        assert validate_exchange("BINANCE") is True
        assert validate_exchange("Binance") is True
    
    def test_invalid_exchanges(self):
        """Test that invalid exchanges are rejected."""
        assert validate_exchange("invalid") is False
        assert validate_exchange("") is False


class TestValidatePositiveNumber:
    """Test validate_positive_number function."""
    
    def test_valid_positive_numbers(self):
        """Test that valid positive numbers are accepted."""
        is_valid, error = validate_positive_number(10.5)
        assert is_valid is True
        assert error is None
        
        is_valid, error = validate_positive_number("100")
        assert is_valid is True
        assert error is None
    
    def test_invalid_numbers(self):
        """Test that invalid numbers are rejected."""
        is_valid, error = validate_positive_number(0)
        assert is_valid is False
        assert "phải là số dương" in error
        
        is_valid, error = validate_positive_number(-10)
        assert is_valid is False
        
        is_valid, error = validate_positive_number("abc")
        assert is_valid is False
        assert "số hợp lệ" in error


class TestValidatePositiveInteger:
    """Test validate_positive_integer function."""
    
    def test_valid_positive_integers(self):
        """Test that valid positive integers are accepted."""
        is_valid, error = validate_positive_integer(10)
        assert is_valid is True
        assert error is None
        
        is_valid, error = validate_positive_integer("100")
        assert is_valid is True
        assert error is None
    
    def test_invalid_integers(self):
        """Test that invalid integers are rejected."""
        is_valid, error = validate_positive_integer(0)
        assert is_valid is False
        assert "số nguyên dương" in error
        
        is_valid, error = validate_positive_integer(-10)
        assert is_valid is False
        
        is_valid, error = validate_positive_integer("10.5")
        assert is_valid is False  # Float strings should be rejected for integer validation
        
        is_valid, error = validate_positive_integer("abc")
        assert is_valid is False


class TestValidateSymbol:
    """Test validate_symbol function."""
    
    def test_valid_symbols(self):
        """Test that valid symbols are accepted."""
        is_valid, error = validate_symbol("BTC/USDT")
        assert is_valid is True
        assert error is None
        
        is_valid, error = validate_symbol("ETH:USDT")
        assert is_valid is True
        assert error is None
    
    def test_empty_symbol(self):
        """Test that empty symbol is accepted (auto-find)."""
        is_valid, error = validate_symbol("")
        assert is_valid is True
        assert error is None
        
        is_valid, error = validate_symbol(None)
        assert is_valid is True
        assert error is None
    
    def test_invalid_symbols(self):
        """Test that invalid symbols are rejected."""
        is_valid, error = validate_symbol("BTC")
        assert is_valid is False
        assert "BASE/QUOTE" in error
        
        is_valid, error = validate_symbol("BTC/ETH")
        assert is_valid is False
        assert "USDT" in error


class TestValidateExchangesUnique:
    """Test validate_exchanges_unique function."""
    
    def test_unique_exchanges(self):
        """Test that unique exchanges are accepted."""
        is_valid, error = validate_exchanges_unique(["binance", "kucoin", "okx"])
        assert is_valid is True
        assert error is None
    
    def test_duplicate_exchanges(self):
        """Test that duplicate exchanges are rejected."""
        is_valid, error = validate_exchanges_unique(["binance", "binance", "okx"])
        assert is_valid is False
        assert "khác nhau" in error
        
        is_valid, error = validate_exchanges_unique(["binance", "kucoin", "binance"])
        assert is_valid is False
