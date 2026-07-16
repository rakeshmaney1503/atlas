"""
Backward compatibility module.

Older code imports:

    from atlas.schemas.screener import CompanyScore
    from atlas.schemas.screener import ScreeningResult

New code should import from:

    atlas.schemas.company_score
    atlas.schemas.screening_result
"""

from atlas.schemas.company_score import CompanyScore
from atlas.schemas.screening_result import ScreeningResult

__all__ = [
    "CompanyScore",
    "ScreeningResult",
]
