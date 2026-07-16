from __future__ import annotations

from atlas.services.providers.market_data_provider import MarketDataProvider


class FMPProvider(MarketDataProvider):
    def search_symbol(self, query: str) -> list[dict]:
        raise NotImplementedError

    def get_company_profile(self, symbol: str) -> dict:
        raise NotImplementedError

    def get_historical_prices(self, symbol: str, start_date: str, end_date: str) -> list[dict]:
        raise NotImplementedError

    def get_financial_statements(self, symbol: str) -> dict:
        raise NotImplementedError

    def get_ratios(self, symbol: str) -> dict:
        raise NotImplementedError
