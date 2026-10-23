#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

total = 0.0
count = 0
# empty dict representing the latest event seen so far
latest = {}

#Opening the json file and reading through it
with open("payments.jsonl") as f:
    for line in f:
        # Using the try and except for exception cases
        try:
            event = json.loads(line)
        # Avoiding Bad lines
        except json.JSONDecodeError:
            continue
        # Ignoring Lines that can't be read
        if not isinstance(event, dict):
            continue
        # Ignoring Events without a txn_id
        if not event.get("txn_id"):
            continue
        #Logic: Comparing and Setting up the latest attempt for each txn_id
        # Setting a Variable to hold the txn_id number
        txn_id = event["txn_id"]
        # Checks if the event has been captured
        if txn_id not in latest:
        # Then stores it in the dictionary
            latest[txn_id] = event
        # Runs a Comparison for a txn_id that has a later entry, to see which is the latest based on the timestamp
        elif event["ts"] > latest[txn_id]["ts"]:
        # Relaces the previous entry for that particular txn_id
            latest[txn_id] = event

#Loops through the values of the Updated Latest Dictionary
for event in latest.values():
    # Checks for the condition if and only if the status is a "success"
    if event["status"] == "success":
        # Check whether the amount is stored as text rather than a number
        if isinstance(event["amount"], str):
            # Converts amounts that are not in the right format (e.g "55,707.77")
            clean = event["amount"].replace(",", "")
            # Converts the cleaned string to a floating number
            total += float(clean)
            # Add this to the number of financial record
            count += 1
        # Then, if it is stored originally as a number, the code jumps to the else block
        else:
            # makes sure to converts the string to a floating number
            total += float(event["amount"])
            # Add this to the number of financial record
            count += 1

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")


