Tests directory

Place unit tests under `tests/unit/` and integration tests under `tests/integration/`.

Example:

- `tests/unit/test_i2c_driver.py` : unit tests for the I2C driver using monkeypatch to fake `smbus2`.

Run tests with:

```bash
pytest
```
