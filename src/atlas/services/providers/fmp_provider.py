from __future__ import annotations

from typing import Any

import requests

from atlas.core.config import get_settings
from atlas.services.providers.market_data_provider import (
    CompanyProfile,
    MarketDataProvider,
)


class FMPProvider(MarketDataProvider):
    """
    Financial Modeling Prep provider.

    This class ONLY communicates with FMP.

    It never:
        • touches the database
        • performs caching
        • contains investment logic
    """

    BASE_URL = "https://financialmodelingprep.com/api/v3"

    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.fmp_api_key

    def provider_name(self) -> str:
        return "Financial Modeling Prep"

    def _request(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        if not self.api_key:
            raise RuntimeError(
                "ATLAS_FMP_API_KEY is not configured."
            )

        if params is None:
            params = {}

        params["apikey"] = self.api_key

        response = requests.get(
            f"{self.BASE_URL}{endpoint}",
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def search_symbol(
        self,
        query: str,
    ) -> list[CompanyProfile]:

        results = self._request(
            "/search",
            {
                "query": query,
                "limit": 10,
            },
        )

        companies: list[CompanyProfile] = []

        for row in results:
            companies.append(
                CompanyProfile(
                    symbol=row.get("symbol", ""),
                    company_name=row.get("name", ""),
                    exchange=row.get("exchangeShortName"),
                    provider=self.provider_name(),
                )
            )

        return companies

    def get_company_profile(
        self,
        symbol: str,
    ) -> CompanyProfile | None:

        results = self._request(f"/profile/{symbol}")

        if not results:
            return None

        profile = results[0]

        return CompanyProfile(
            symbol=profile.get("symbol", symbol),
            company_name=profile.get("companyName", ""),
            isin=profile.get("isin"),
            exchange=profile.get("exchangeShortName"),
            sector=profile.get("sector"),
            industry=profile.get("industry"),
            description=profile.get("description"),
            website=profile.get("website"),
            currency=profile.get("currency"),
            provider=self.provider_name(),
        )

    def get_financial_statements(
        self,
        symbol: str,
    ) -> dict:
        """
        Return the three core financial statements.

        This will become the foundation for the
        Atlas Screening Engine.
        """

        return {
            "income_statement": self._request(
                f"/income-statement/{symbol}",
                {"limit": 10},
            ),
            "balance_sheet": self._request(
                f"/balance-sheet-statement/{symbol}",
                {"limit": 10},
            ),
            "cash_flow": self._request(
                f"/cash-flow-statement/{symbol}",
                {"limit": 10},
            ),
        }

    def get_ratios(
        self,
        symbol: str,
    ) -> dict:

        results = self._request(
            f"/ratios/{symbol}",
            {"limit": 10},
        )

        if not results:
            return {}

        return results[0]

    def get_historical_prices(
        self,
        symbol: str,
        years: int = 10,
    ) -> dict:

        return self._request(
            f"/historical-price-full/{symbol}",
        )
