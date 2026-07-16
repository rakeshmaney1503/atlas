from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class MarketDataProvider(ABC):
    @abstractmethod
    def search_symbol(self, query: str) -> List[Dict[str, Any]]:
        """Search for one or more symbols matching the query."""
        raise NotImplementedError

    @abstractmethod
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """Return company profile metadata for a single symbol."""
        raise NotImplementedError

    @abstractmethod
    def get_historical_prices(self, symbol: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Return historical price series for a symbol."""
        raise NotImplementedError

    @abstractmethod
    def get_financial_statements(self, symbol: str) -> Dict[str, Any]:
        """Return financial statements for a symbol."""
        raise NotImplementedError

    @abstractmethod
    def get_ratios(self, symbol: str) -> Dict[str, Any]:
        """Return financial ratios for a symbol."""
        raise NotImplementedError
