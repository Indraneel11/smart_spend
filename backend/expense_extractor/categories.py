MERCHANT_CATEGORY_RULES = {
    "zomato": "Food",
    "swiggy": "Food",
    "dominos": "Food",
    "uber": "Travel",
    "ola": "Travel",
    "rapido": "Travel",
    "amazon": "Shopping",
    "flipkart": "Shopping",
    "myntra": "Shopping",
    "netflix": "Entertainment",
    "spotify": "Subscription",
    "airtel": "Bills",
    "jio": "Bills",
}


def categorize_merchant(merchant):
    if not merchant:
        return "Uncategorized"

    merchant_lower = merchant.lower()

    for known_merchant, category in MERCHANT_CATEGORY_RULES.items():
        if known_merchant in merchant_lower:
            return category

    return "Uncategorized"