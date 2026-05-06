class ZoyaProvider:
    name = "zoya"
    methodology = "AAOIFI"

    async def get_report(self, symbol: str):
        raise NotImplementedError("Zoya provider is not implemented yet.")

    async def bulk_get_reports(self, symbols: list[str]):
        raise NotImplementedError("Zoya provider is not implemented yet.")
