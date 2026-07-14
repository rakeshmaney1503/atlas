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

    @classmethod
    def categorize(cls, description: str) -> str:
        description = description.lower()

        for keywords, category in cls.RULES:
            for keyword in keywords:
                if keyword.lower() in description:
                    return category

        return "Others"
