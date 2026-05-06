from py_common.brokers.alpaca import AlpacaBroker
from py_common.brokers.backtest import BacktestBroker
from py_common.brokers.ibkr import IBKRBroker
from py_common.brokers.mock import MockBrokerProvider
from py_common.brokers.trading212 import Trading212Broker


def get_broker(name: str):
    registry = {
        "mock": MockBrokerProvider,
        "trading212": Trading212Broker,
        "backtest": BacktestBroker,
        "alpaca": AlpacaBroker,
        "ibkr": IBKRBroker,
    }
    if name not in registry:
        raise ValueError(f"Unsupported broker provider: {name}")
    return registry[name]()
