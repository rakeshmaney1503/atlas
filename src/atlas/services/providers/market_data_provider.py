from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class CompanyProfile:
    symbol: str
    company_name: str

    isin: Optional[str] = None
    exchange: Optional[str] = None

    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap_category: Optional[str] = None

    description: Optional[str] = None
    website: Optional[str] = None
    currency: Optional[str] = None

    provider: Optional[str] = None
    fetched_at: Optional[datetime] = None


class MarketDataProvider(ABC):
    """
    Base interface for every external market data provider.

    Providers are responsible ONLY for retrieving data from external
    services and converting them into Atlas domain models.

    Providers MUST NOT:
      - update the database
      - cache results
      - contain business logic
      - make investment decisions
    """

    @abstractmethod
    def provider_name(self) -> str:
        """Human readable provider name."""

    @abstractmethod
    def search_symbol(
        self,
        query: str,
    ) -> list[CompanyProfile]:
        """
        Search for companies matching a query.
        """

    @abstractmethod
    def get_company_profile(
        self,
        symbol: str,
    ) -> CompanyProfile | None:
        """
        Return the latest company profile for a symbol.
        """

    @abstractmethod
    def get_financial_statements(
        self,
        symbol: str,
    ) -> dict:
        """
        Return financial statements.
        """

    @abstractmethod
    def get_ratios(
        self,
        symbol: str,
    ) -> dict:
        """
        Return valuation and financial ratios.
        """

    @abstractmethod
    def get_historical_prices(
        self,
        symbol: str,
        years: int = 10,
    ) -> dict:
        """
        Return historical OHLC data.
        """
