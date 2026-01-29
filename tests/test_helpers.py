"""
Unit tests for helpers module.
"""
import pytest
import os
import tempfile
from utils.helpers import (
    show_time,
    format_message,
    calculate_average,
    extract_base_asset,
    read_file_content,
    update_balance_file
)


class TestShowTime:
    """Test show_time function."""
    
    def test_returns_time_format(self):
        """Test that show_time returns properly formatted time."""
        time_str = show_time()
        assert isinstance(time_str, str)
        # Should be in HH:MM:SS format
        parts = time_str.split(':')
        assert len(parts) == 3
        for part in parts:
            assert part.isdigit()
            assert len(part) == 2


class TestFormatMessage:
    """Test format_message function."""
    
    def test_removes_color_codes(self):
        """Test that format_message removes colorama codes."""
        message = "[2mTest message[0m"
        result = format_message(message)
        assert "[2m" not in result
        assert "[0m" not in result
        assert "Test message" in result


class TestCalculateAverage:
    """Test calculate_average function."""
    
    def test_calculates_average(self):
        """Test that calculate_average correctly computes average."""
        values = [10, 20, 30]
        assert calculate_average(values) == 20.0
        
        values = [5.5, 10.5]
        assert calculate_average(values) == 8.0
    
    def test_empty_list(self):
        """Test that empty list returns 0."""
        assert calculate_average([]) == 0
    
    def test_single_value(self):
        """Test that single value returns itself."""
        assert calculate_average([42]) == 42


class TestExtractBaseAsset:
    """Test extract_base_asset function."""
    
    def test_extracts_from_slash_format(self):
        """Test extraction from symbol with slash."""
        assert extract_base_asset("BTC/USDT") == "BTC"
        assert extract_base_asset("ETH/USDT") == "ETH"
    
    def test_extracts_from_colon_format(self):
        """Test extraction from symbol with colon."""
        assert extract_base_asset("BTC:USDT") == "BTC"
        assert extract_base_asset("ETH:USDT") == "ETH"
    
    def test_no_separator(self):
        """Test that symbol without separator is returned as-is."""
        assert extract_base_asset("BTC") == "BTC"


class TestFileOperations:
    """Test file operation functions."""
    
    def test_read_file_content(self):
        """Test reading file content."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("test content")
            temp_file = f.name
        
        try:
            content = read_file_content(temp_file)
            assert content == "test content"
        finally:
            os.unlink(temp_file)
    
    def test_read_nonexistent_file(self):
        """Test reading nonexistent file raises exception."""
        with pytest.raises(FileNotFoundError):
            read_file_content("/nonexistent/file.txt")
    
    def test_update_balance_file(self):
        """Test updating balance file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file = f.name
        
        try:
            # Test update with 10% profit on 100 USDT
            new_balance = update_balance_file(temp_file, 10, 100)
            assert new_balance == 110.0
            
            # Verify file content
            content = read_file_content(temp_file)
            assert content == "110.0"
        finally:
            os.unlink(temp_file)
    
    def test_update_balance_with_loss(self):
        """Test updating balance with negative profit."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file = f.name
        
        try:
            # Test update with -5% loss on 100 USDT
            new_balance = update_balance_file(temp_file, -5, 100)
            assert new_balance == 95.0
        finally:
            os.unlink(temp_file)
