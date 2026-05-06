class Trading212Broker:
    name = "trading212"

    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            "Trading212Broker is not implemented yet. "
            "Set execution.broker = 'mock' in config/bot.json (the default in demo mode), "
            "or implement this provider before pointing the config at it."
        )
