import json
from pathlib import Path

from expense_extractor import parse_notification


sample_notifications = [
    "Rs. 249 paid to Zomato using PhonePe UPI.",
    "HDFC Bank: Rs. 1,500 debited from your account for AMAZON PAY.",
    "You paid ₹320 to Uber via UPI.",
    "Rs. 5000 credited to your HDFC Bank account.",
    "Your order has been packed and will arrive today.",
]


transactions = []
ignored_notifications = []

for notification in sample_notifications:
    transaction = parse_notification(notification)

    if transaction is None:
        ignored_notifications.append({
            "ignored": True,
            "raw_text": notification
        })
    else:
        transactions.append(transaction.to_dict())


output_dir = Path("backend/output")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "transactions.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(transactions, file, indent=2)

print(f"Extracted {len(transactions)} transactions")
print(f"Ignored {len(ignored_notifications)} notifications")
print(f"Saved output to {output_file}")