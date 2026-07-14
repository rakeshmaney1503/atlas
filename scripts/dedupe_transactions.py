"""
Safe dedupe script for transactions table.
Keeps the earliest `created_at` row for each normalized key:
(account_id, transaction_date.isoformat(), amount.quantized(0.01), description.strip())

Usage:
    python3 scripts/dedupe_transactions.py

This will print a summary and prompt before deleting.
"""
from decimal import Decimal
import sqlite3
from datetime import datetime

DB = "atlas.db"

def normalize_key(account_id, tx_date, amount, description):
    try:
        date_key = tx_date
    except Exception:
        date_key = str(tx_date)
    try:
        amt = Decimal(str(amount)).quantize(Decimal("0.01"))
    except Exception:
        amt = Decimal("0.00")
    amount_key = format(amt, 'f')
    desc_key = (description or "").strip()
    return (str(account_id), date_key, amount_key, desc_key)

def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    rows = c.execute('SELECT id, account_id, transaction_date, amount, description, created_at FROM "transaction"').fetchall()

    groups = {}
    for r in rows:
        _id, account_id, tx_date, amount, description, created_at = r
        key = normalize_key(account_id, tx_date, amount, description)
        groups.setdefault(key, []).append((_id, created_at))

    dup_groups = {k:v for k,v in groups.items() if len(v)>1}
    total_dups = sum(len(v)-1 for v in dup_groups.values())
    print(f"Found {len(dup_groups)} duplicate groups, {total_dups} rows to delete.")
    if total_dups==0:
        return

    confirm = input("Proceed to delete duplicates, keeping the earliest created_at in each group? [y/N]: ")
    if confirm.lower()!='y':
        print('Aborting.')
        return

    to_delete = []
    for key, items in dup_groups.items():
        # keep the one with earliest created_at (lexicographic compare of string)
        items_sorted = sorted(items, key=lambda x: x[1] or '')
        keep = items_sorted[0][0]
        for _id, _ in items_sorted[1:]:
            to_delete.append(_id)

    print(f"Deleting {len(to_delete)} rows...")
    c.executemany('DELETE FROM "transaction" WHERE id=?', [(i,) for i in to_delete])
    conn.commit()
    print('Done.')

if __name__=='__main__':
    main()
