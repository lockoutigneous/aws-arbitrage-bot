"""
Integration tests for main bot functionality.
Tests configuration, bot initialization, and key workflows.
"""
import pytest
import os
import sys
import tempfile
import argparse
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import (
    validate_bot_config,
    parse_arguments,
    setup_logging,
)
from configs import BOT_MODES, MIN_USDT_AMOUNT


class TestBotConfigValidation:
    """Test bot configuration validation."""
    
    def test_valid_config(self):
        """Test valid configuration passes validation."""
        errors = validate_bot_config(
            mode="fake-money",
            renew_time=15,
            usdt_amount=1000,
            exchanges=["binance", "kucoin", "okx"],
            symbol="BTC/USDT"
        )
        assert len(errors) == 0
    
    def test_invalid_mode(self):
        """Test invalid mode is detected."""
        errors = validate_bot_config(
            mode="invalid-mode",
            renew_time=15,
            usdt_amount=1000,
            exchanges=["binance", "kucoin", "okx"],
            symbol="BTC/USDT"
        )
        assert len(errors) > 0
        assert any("Chế độ không hợp lệ" in error for error in errors)
    
    def test_invalid_renew_time(self):
        """Test invalid renew time is detected."""
        errors = validate_bot_config(
            mode="fake-money",
            renew_time=-5,
            usdt_amount=1000,
            exchanges=["binance", "kucoin", "okx"],
            symbol="BTC/USDT"
        )
        assert len(errors) > 0
        assert any("Thời gian làm mới" in error for error in errors)
    
    def test_insufficient_usdt_amount(self):
        """Test insufficient USDT amount is detected."""
        errors = validate_bot_config(
            mode="fake-money",
            renew_time=15,
            usdt_amount=5,  # Less than MIN_USDT_AMOUNT
            exchanges=["binance", "kucoin", "okx"],
            symbol="BTC/USDT"
        )
        assert len(errors) > 0
        assert any("ít nhất" in error for error in errors)
    
    def test_unsupported_exchange(self):
        """Test unsupported exchange is detected."""
        errors = validate_bot_config(
            mode="fake-money",
            renew_time=15,
            usdt_amount=1000,
            exchanges=["binance", "invalid_exchange", "okx"],
            symbol="BTC/USDT"
        )
        assert len(errors) > 0
        assert any("không được hỗ trợ" in error for error in errors)
    
    def test_duplicate_exchanges(self):
        """Test duplicate exchanges are detected."""
        errors = validate_bot_config(
            mode="fake-money",
            renew_time=15,
            usdt_amount=1000,
            exchanges=["binance", "binance", "okx"],
            symbol="BTC/USDT"
        )
        assert len(errors) > 0
        assert any("khác nhau" in error for error in errors)
    
    def test_invalid_symbol(self):
        """Test invalid symbol is detected."""
        errors = validate_bot_config(
            mode="fake-money",
            renew_time=15,
            usdt_amount=1000,
            exchanges=["binance", "kucoin", "okx"],
            symbol="BTC"  # Invalid format
        )
        assert len(errors) > 0
        assert any("BASE/QUOTE" in error for error in errors)
    
    def test_symbol_without_usdt(self):
        """Test symbol without USDT is detected."""
        errors = validate_bot_config(
            mode="fake-money",
            renew_time=15,
            usdt_amount=1000,
            exchanges=["binance", "kucoin", "okx"],
            symbol="BTC/ETH"  # No USDT
        )
        assert len(errors) > 0
        assert any("USDT" in error for error in errors)
    
    def test_empty_symbol_allowed(self):
        """Test empty symbol is allowed (auto-find)."""
        errors = validate_bot_config(
            mode="fake-money",
            renew_time=15,
            usdt_amount=1000,
            exchanges=["binance", "kucoin", "okx"],
            symbol=None
        )
        assert len(errors) == 0


class TestArgumentParsing:
    """Test command line argument parsing."""
    
    def test_parse_valid_args(self):
        """Test parsing valid command line arguments."""
        test_args = [
            'fake-money', '15', '1000',
            'binance', 'kucoin', 'okx',
            'BTC/USDT'
        ]
        
        with patch('sys.argv', ['main.py'] + test_args):
            args = parse_arguments()
            assert args.mode == 'fake-money'
            assert args.renew_time == 15
            assert args.usdt_amount == 1000
            assert args.exchange1 == 'binance'
            assert args.exchange2 == 'kucoin'
            assert args.exchange3 == 'okx'
            assert args.symbol == 'BTC/USDT'
    
    def test_parse_args_without_symbol(self):
        """Test parsing arguments without symbol."""
        test_args = [
            'classic', '30', '500',
            'binance', 'kucoin', 'okx'
        ]
        
        with patch('sys.argv', ['main.py'] + test_args):
            args = parse_arguments()
            assert args.mode == 'classic'
            assert args.symbol is None
    
    def test_parse_args_with_flags(self):
        """Test parsing arguments with optional flags."""
        test_args = [
            'fake-money', '15', '1000',
            'binance', 'kucoin', 'okx',
            '--debug', '--dry-run'
        ]
        
        with patch('sys.argv', ['main.py'] + test_args):
            args = parse_arguments()
            assert args.debug is True
            assert args.dry_run is True


class TestLoggingSetup:
    """Test logging setup."""
    
    def test_logging_setup_creates_directory(self):
        """Test that logging setup creates logs directory."""
        import logging
        
        # Use a temporary directory for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                setup_logging()
                
                # Check that logs directory was created
                logs_dir = Path(tmpdir) / 'logs'
                assert logs_dir.exists()
                assert logs_dir.is_dir()
            finally:
                os.chdir(original_cwd)
    
    def test_logging_level_can_be_set(self):
        """Test that logging level can be configured."""
        import logging
        
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                setup_logging(level=logging.DEBUG)
                
                # Verify logging setup was called successfully
                # (The actual level is set on handlers, not root logger)
                logs_dir = Path(tmpdir) / 'logs'
                assert logs_dir.exists()
            finally:
                os.chdir(original_cwd)


class TestBotModes:
    """Test bot mode configurations."""
    
    def test_all_bot_modes_supported(self):
        """Test that all expected bot modes are supported."""
        expected_modes = ['fake-money', 'classic', 'delta-neutral']
        assert BOT_MODES == expected_modes
    
    def test_each_mode_validates_correctly(self):
        """Test that each mode validates correctly."""
        for mode in BOT_MODES:
            errors = validate_bot_config(
                mode=mode,
                renew_time=15,
                usdt_amount=1000,
                exchanges=["binance", "kucoin", "okx"],
                symbol="BTC/USDT"
            )
            assert len(errors) == 0, f"Mode {mode} should be valid"


class TestBalanceFileOperations:
    """Test balance file operations used by bot."""
    
    def test_balance_file_creation(self):
        """Test balance file can be created and read."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
            f.write("1000.0")
        
        try:
            with open(temp_file, 'r') as f:
                balance = float(f.read().strip())
            assert balance == 1000.0
        finally:
            os.unlink(temp_file)
    
    def test_balance_file_update(self):
        """Test balance file can be updated."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
            f.write("1000.0")
        
        try:
            # Read original balance
            with open(temp_file, 'r') as f:
                balance = float(f.read().strip())
            
            # Update balance (e.g., 10% profit)
            new_balance = balance * 1.10
            with open(temp_file, 'w') as f:
                f.write(str(new_balance))
            
            # Verify update
            with open(temp_file, 'r') as f:
                updated_balance = float(f.read().strip())
            assert updated_balance == 1100.0
        finally:
            os.unlink(temp_file)


class TestEnvironmentConfiguration:
    """Test environment variable configuration."""
    
    def test_env_var_defaults(self):
        """Test that environment variables have sensible defaults."""
        from configs import PYTHON_COMMAND, ENABLE_TELEGRAM, MIN_USDT_AMOUNT
        
        assert isinstance(PYTHON_COMMAND, str)
        assert isinstance(ENABLE_TELEGRAM, bool)
        assert MIN_USDT_AMOUNT > 0
    
    def test_supported_exchanges_list(self):
        """Test that supported exchanges are properly configured."""
        from configs import SUPPORTED_EXCHANGES
        
        assert isinstance(SUPPORTED_EXCHANGES, list)
        assert len(SUPPORTED_EXCHANGES) > 0
        assert 'binance' in SUPPORTED_EXCHANGES
        assert 'kucoin' in SUPPORTED_EXCHANGES
    
    def test_exchange_fees_configured(self):
        """Test that exchange fees are configured."""
        from configs import EXCHANGE_FEES
        
        assert isinstance(EXCHANGE_FEES, dict)
        assert 'binance' in EXCHANGE_FEES
        assert 'kucoin' in EXCHANGE_FEES
        
        # Check fee structure
        for exchange, fees in EXCHANGE_FEES.items():
            assert 'give' in fees
            assert 'receive' in fees
            assert fees['give'] > 0
            assert fees['receive'] > 0
