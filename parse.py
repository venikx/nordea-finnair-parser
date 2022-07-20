#!/usr/bin/env python3
import pdfplumber
import re

from datetime import datetime
import csv
import sys

header = ["Booking date", "Description", "Amount"]

parsed_total_amount = 0
calculated_total_amount = 0
transactions_count = 0


def parse_transactions(fname):
    global calculated_total_amount, parsed_total_amount, transactions_count
    billing_year = ""
    pdf = pdfplumber.open(fname)

    with open("nordea-finnair.csv", "w", encoding="UTF8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(header)

        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")

            for line in lines:
                if t := re.search("\s+OSTOT YHTEENSÄ\s+([\d\s]+.+\d{2})", line):
                    parsed_total_amount = float(t.group(1).replace(" ", ""))

                if m := re.search(
                    "\ALASKUTUSKAUSI\s*\d{2}.\d{2}.\d{2}\W*(\d{2}.\d{2}.\d{2})", line
                ):
                    billing_year = m.group(1).split(".")[2]

                if t := re.search(
                    "(\d{2}.\d{2}.)\s+\d{2}.\d{2}.\s+\d{12}\s+(.+)\s+(\d+.\d+)\Z", line
                ):
                    transaction_date = datetime.strptime(
                        t.group(1) + billing_year, "%d.%m.%y"
                    ).strftime("%Y-%m-%d")
                    transaction_description = t.group(2).strip()
                    transaction_amount = t.group(3)
                    writer.writerow(
                        [transaction_date, transaction_description, transaction_amount]
                    )
                    calculated_total_amount += float(transaction_amount)
                    transactions_count += 1
        f.close()


def main():
    pdf_path = sys.argv[1]
    parse_transactions(pdf_path)

    print("Expected Amount:     {:.2f}".format(parsed_total_amount))
    print("Calculated Amount:   {:.2f}".format(calculated_total_amount))
    print("Total Transactions:   {}".format(transactions_count))


main()
