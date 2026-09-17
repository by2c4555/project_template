# Bounded Local Repair

A Task defaults to two local repairs and may declare `max_repairs` from 0 through 5. Each authorized repair creates a fresh Repair Ticket and fresh Builder Attempt bound to the failed parent Attempt. Exhausted budgets or structural authority failures route to Diagnosis rather than permitting open-ended Builder retry loops.
