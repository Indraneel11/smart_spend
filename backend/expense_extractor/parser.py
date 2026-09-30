import re

from .categories import categorize_merchant
from .models import Transaction


AMOUNT_PATTERN = re.compile(
    r"(?:rs\.?|inr|₹)\s*([0-9]+(?:,[0-9]{2,3})*(?:\.[0-9]{1,2})?)",
    re.IGNORECASE,
)

EXPENSE_KEYWORDS = [
    "paid",
    "debited",
    "spent",
    "sent",
    "payment successful",
]

INCOME_KEYWORDS = [
    "credited",
    "received",
    "refund",
]

MERCHANT_PATTERNS = [
    re.compile(r"paid to\s+([A-Za-z0-9 &._-]+?)(?:\s+using|\s+via|\.|$)", re.IGNORECASE),
    re.compile(r"to\s+([A-Za-z0-9 &._-]+?)(?:\s+using|\s+via|\.|$)", re.IGNORECASE),
    re.compile(r"for\s+([A-Za-z0-9 &._-]+?)(?:\.|$)", re.IGNORECASE),
]


def parse_notification(text):
    cleaned_text = clean_text(text)

    if not is_transaction(cleaned_text):
        return None

    amount = extract_amount(cleaned_text)

    if amount is None:
        return None

    merchant = extract_merchant(cleaned_text)
    transaction_type = extract_transaction_type(cleaned_text)
    payment_mode = extract_payment_mode(cleaned_text)
    category = categorize_merchant(merchant)

    return Transaction(
        amount=amount,
        currency="INR",
        merchant=merchant,
        transaction_type=transaction_type,
        payment_mode=payment_mode,
        category=category,
        raw_text=text,
    )


def clean_text(text):
    return " ".join(text.strip().split())


def is_transaction(text):
    text_lower = text.lower()

    has_amount = bool(AMOUNT_PATTERN.search(text))
    has_transaction_keyword = any(
        keyword in text_lower
        for keyword in EXPENSE_KEYWORDS + INCOME_KEYWORDS
    )

    return has_amount and has_transaction_keyword


def extract_amount(text):
    match = AMOUNT_PATTERN.search(text)

    if not match:
        return None

    amount_text = match.group(1).replace(",", "")
    return float(amount_text)


def extract_merchant(text):
    for pattern in MERCHANT_PATTERNS:
        match = pattern.search(text)

        if match:
            merchant = match.group(1).strip(" .,-")
            return merchant.title()

    return None


def extract_transaction_type(text):
    text_lower = text.lower()

    if any(keyword in text_lower for keyword in INCOME_KEYWORDS):
        return "income"

    return "expense"


def extract_payment_mode(text):
    text_lower = text.lower()

    if "upi" in text_lower:
        return "UPI"

    if "card" in text_lower:
        return "Card"

    if "wallet" in text_lower:
        return "Wallet"

    if "net banking" in text_lower or "netbanking" in text_lower:
        return "Net Banking"

    return None