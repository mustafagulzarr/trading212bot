class MusaffaProvider:
    name = "musaffa"
    methodology = "AAOIFI"

    async def get_report(self, symbol: str):
        raise NotImplementedError("Musaffa provider is not implemented yet.")

    async def bulk_get_reports(self, symbols: list[str]):
        raise NotImplementedError("Musaffa provider is not implemented yet.")
