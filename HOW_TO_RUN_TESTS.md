# How to Run Tests - AWS Arbitrage Bot

This guide explains how to run the comprehensive test suite for the AWS Arbitrage Bot.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ -v --cov=. --cov-report=html
```

## Test Categories

### 1. Unit Tests
Tests individual functions and utilities in isolation.

**Run validators tests:**
```bash
python -m pytest tests/test_validators.py -v
```

**Run helpers tests:**
```bash
python -m pytest tests/test_helpers.py -v
```

### 2. Integration Tests
Tests the interaction between components and system-level functionality.

**Run integration tests:**
```bash
python -m pytest tests/test_integration.py -v
```

## Test Options

### Verbose Output
```bash
python -m pytest tests/ -v
```

### Show Test Durations
```bash
python -m pytest tests/ --durations=10
```

### Run Specific Test Class
```bash
python -m pytest tests/test_validators.py::TestValidateMode -v
```

### Run Specific Test Method
```bash
python -m pytest tests/test_validators.py::TestValidateMode::test_valid_modes -v
```

### Stop on First Failure
```bash
python -m pytest tests/ -x
```

### Show Local Variables on Failure
```bash
python -m pytest tests/ -l
```

## Manual Testing

### Test Bot Initialization
```bash
# Test with fake-money mode (safe, no real trades)
python main.py fake-money 15 1000 binance kucoin okx BTC/USDT --no-banner --dry-run

# Test argument validation (should fail with error)
python main.py invalid-mode 15 1000 binance kucoin okx
```

### Test Configuration Validation
```bash
# Valid configuration
python main.py fake-money 15 1000 binance kucoin okx BTC/USDT --dry-run

# Invalid: duplicate exchanges
python main.py fake-money 15 1000 binance binance okx BTC/USDT

# Invalid: insufficient USDT amount
python main.py fake-money 15 5 binance kucoin okx BTC/USDT

# Invalid: wrong symbol format
python main.py fake-money 15 1000 binance kucoin okx BTC
```

## Expected Test Results

### All Tests Should Pass
```
========================= test session starts ==========================
platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/runner/work/aws-arbitrage-bot/aws-arbitrage-bot
collected 48 items

tests/test_helpers.py ............                               [ 25%]
tests/test_integration.py .....................                  [ 68%]
tests/test_validators.py ...............                         [100%]

========================== 48 passed in 0.64s ==========================
```

### Success Indicators
- ✅ All 48 tests pass
- ✅ No errors or warnings
- ✅ Test execution time < 1 second
- ✅ No security vulnerabilities

## Troubleshooting

### Issue: aiohttp Installation Fails
**Solution:** Ensure you're using Python 3.12+
```bash
python --version  # Should be 3.12 or higher
pip install aiohttp>=3.13.0
```

### Issue: Import Errors
**Solution:** Install all dependencies
```bash
pip install -r requirements.txt
```

### Issue: Tests Run but Some Fail
**Solution:** Check the error messages and verify:
1. All dependencies are installed
2. Python version is 3.12+
3. No modifications to test files

## Continuous Integration

For CI/CD pipelines, use:
```bash
# Install dependencies quietly
pip install -q -r requirements.txt

# Run tests with JUnit XML output
python -m pytest tests/ -v --junit-xml=test-results.xml

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ All tests passed"
else
    echo "❌ Tests failed"
    exit 1
fi
```

## Test Coverage

To generate a coverage report:
```bash
# Install pytest-cov
pip install pytest-cov

# Generate HTML coverage report
python -m pytest tests/ --cov=. --cov-report=html

# View report
# Open htmlcov/index.html in a browser
```

## Adding New Tests

### Unit Test Template
```python
class TestNewFeature:
    """Test new feature functionality."""
    
    def test_basic_functionality(self):
        """Test basic functionality works."""
        result = new_feature()
        assert result is not None
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            new_feature(invalid_input)
```

### Integration Test Template
```python
class TestNewIntegration:
    """Test integration with other components."""
    
    def test_component_interaction(self):
        """Test components work together."""
        component_a = ComponentA()
        component_b = ComponentB()
        
        result = component_a.interact_with(component_b)
        assert result.is_successful()
```

## Security Testing

Run CodeQL security analysis (requires GitHub Actions or CodeQL CLI):
```bash
# This is done automatically in CI/CD
# Manual check through code review and static analysis
```

## Performance Testing

For performance benchmarks:
```bash
# Install pytest-benchmark
pip install pytest-benchmark

# Run with timing information
python -m pytest tests/ --durations=0
```

## Test Reports

After running tests, review the comprehensive reports:
- `TEST_REPORT.md` - English test report
- `BAO_CAO_KIEM_TRA.md` - Vietnamese test report (Báo cáo tiếng Việt)

## Support

If you encounter any issues:
1. Check the test reports for details
2. Review the logs in the `logs/` directory
3. Ensure all dependencies are installed correctly
4. Verify Python version compatibility

---

**Last Updated:** 2026-01-29  
**Test Framework:** pytest 9.0.2  
**Python Version:** 3.12.3+  
**Total Tests:** 48  
**Success Rate:** 100%
