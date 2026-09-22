import random, csv, datetime
from itertools import islice
import sys
import os

day = sys.argv[1]
data = []

with open(f"./transactions_{day}.csv", "r") as f:
    reader_r = csv.reader(f)
    header = next(reader_r)
    for row in reader_r:
        if row:
            data.append({'txn_id': row[0], 'amount': row[2]})
    
random_txn_list = random.sample(data, 10)
refund_reason=['fraud', 'customer_request', 'duplicate']
created_at = lambda: (datetime.datetime.fromisoformat(day) + datetime.timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))).isoformat()

def make_row():
    refund_row = []
    for i, item in enumerate(random_txn_list, start=1):
        row = {
            'refund_id': i,
            'txn_id': item['txn_id'],
            'refund_amount': item['amount'],
            'refund_reason': random.choice(refund_reason),
            'created_at': created_at()
        }
        refund_row.append(row)
    return refund_row

def main():
    if not os.path.exists(f"refunds_{day}.csv"):
        with open(f"refunds_{day}.csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['refund_id', 'txn_id', 'refund_amount', 'refund_reason', 'created_at'])
            for row in make_row():
                writer.writerow([row['refund_id'], row['txn_id'], row['refund_amount'], row['refund_reason'], row['created_at']])
        print(f"file refunds_{day}.csv created successfully!")
    else:
        print("File already exists")
   
main()