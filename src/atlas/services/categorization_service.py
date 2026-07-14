class CategorizationService:
    RULES = [
        # Investments
        (["PPF", "PPFAS", "SBI MUTUAL", "UTI MF", "ZERODHA"], "Investment"),

        # Insurance
        (["LIC"], "Insurance"),

        # Credit Cards
        (["BillPay", "CC BillPay"], "Credit Card"),

        # Food & Dining
        (
            [
                "coffee",
                "pizza",
                "bakery",
                "icecream",
                "panipuri",
                "bonda",
                "khara",
                "milk",
            ],
            "Food & Dining",
        ),

        # Groceries
        (
            [
                "onion",
                "vegetable",
                "provision",
                "fresh",
            ],
            "Groceries",
        ),

        # Fuel
        (
            [
                "petrol",
                "fuel",
            ],
            "Fuel",
        ),

        # Healthcare
        (
            [
                "hospital",
                "medicine",
            ],
            "Healthcare",
        ),

        # Transport
        (
            [
                "cab",
                "auto",
                "carwash",
                "car",
                "battery",
            ],
            "Transport",
        ),

        # Personal Care
        (
            [
                "haircut",
            ],
            "Personal Care",
        ),

        # Shopping
        (
            [
                "stationary",
                "apparel",
                "xyxx",
            ],
            "Shopping",
        ),

        # Bills & Utilities
        (
            [
                "ACT",
                "broadband",
                "Netflix",
                "Google Pla",
            ],
            "Bills & Utilities",
        ),

        # Family
        (
            [
                "wife",
                "amma",
                "kaka",
            ],
            "Family",
        ),

        # Income
        (
            [
                "Salary",
                "DIV",
                "REV CCW",
            ],
            "Income",
        ),
    ]

    MERCHANT_CATEGORIES = [
        (['Domino\'s'], 'Food'),
        (['Netflix'], 'Subscription'),
        (['ACT'], 'Internet'),
        (['LIC'], 'Insurance'),
        (['PPFAS'], 'Investment'),
        (['Zerodha'], 'Investment'),
        (['Google Play'], 'Digital Services'),
    ]

    @classmethod
    def categorize(
        cls,
        description: str,
        merchant: str | None = None,
    ) -> str:
        if merchant:
            for keywords, category in cls.MERCHANT_CATEGORIES:
                for keyword in keywords:
                    if keyword.lower() == merchant.lower():
                        return category

        description = description.lower()

        for keywords, category in cls.RULES:
            for keyword in keywords:
                if keyword.lower() in description:
                    return category

        return "Others"
