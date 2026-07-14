# Atlas Roadmap

## Completed Features

- Preserve ICICI running balances through import and display
  - ICICI `Balance(INR)` now imports into `Transaction.running_balance`
  - Dashboard uses latest running balance as current cash balance
  - Net Worth uses latest cash balance plus portfolio value
  - Transactions page displays `Running Balance` per row

## Migration Strategy

Atlas currently uses SQLite without Alembic. For schema changes:

1. Add a migration script under `scripts/`.
2. Run the migration script against `atlas.db`.
3. Keep `atlas.db` intact; do not delete existing database.

This avoids destructive schema updates and preserves existing data.
