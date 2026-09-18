import csv, random, datetime
import sys

day = sys.argv[1]

columns = ['txn_id', 'customer_id', 'amount', 'currency', 'status', 'created_at']
status = ['approved', 'declined', 'pending']
amount = lambda: round(random.uniform(1.00, 500.00), 2)

base = datetime.datetime.fromisoformat(day)
created_at = lambda: datetime.datetime.combine(base, datetime.time(random.randint(0,23), random.randint(0,59))).isoformat()

def make_row(i):
    return [
        i,
        f"CS-{i:03d}",
        amount(),
        "USD",
        random.choice(status),
        created_at()
    ]

def main():
    # TODO: write to transactions_2026-09-16.csv\
    with open(f"transactions_{day}.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(columns)

        for i in range(1, 101):
            row=writer.writerow(make_row(i))

main()