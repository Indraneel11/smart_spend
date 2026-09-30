from dataclasses import dataclass, asdict


@dataclass
class Transaction:
    amount: float
    currency: str
    merchant: str | None
    transaction_type: str
    payment_mode: str | None
    category: str
    raw_text: str

    def to_dict(self):
        return asdict(self)