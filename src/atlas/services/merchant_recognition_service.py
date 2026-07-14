import re


class MerchantRecognitionService:
    RULES = [
        (['DOMINOS'], "Domino's"),
        (['NETFLIX'], 'Netflix'),
        (['ACT'], 'ACT'),
        (['LIC'], 'LIC'),
        (['PPFAS'], 'PPFAS'),
        (['ZERODHA'], 'Zerodha'),
        (['GOOGLE PLA', 'GOOGLE PLAY', 'PLAYSTORE'], 'Google Play'),
    ]

    @classmethod
    def recognize(cls, description: str | None) -> str | None:
        if description is None:
            return None

        text = str(description).strip()
        if not text:
            return None

        normalized = text.lower()

        for keywords, merchant in cls.RULES:
            for keyword in keywords:
                if re.search(rf"\b{re.escape(keyword.lower())}\b", normalized):
                    return merchant

        return None
