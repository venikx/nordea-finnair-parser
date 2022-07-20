import pdfplumber
import re

from datetime import datetime

billing_year = ""
parsed_total_amount = 0
calculated_total_amount = 0

pdf = pdfplumber.open("finnair.pdf")

for page in pdf.pages:
    text = page.extract_text()
    lines = text.split("\n")

    for line in lines:
        # print(line)
        if m := re.search(
            "\ALASKUTUSKAUSI\s*\d{2}.\d{2}.\d{2}\W*(\d{2}.\d{2}.\d{2})", line
        ):
            billing_year = m.group(1).split(".")[2]

        if t := re.search(
            "(\d{2}.\d{2}.)\s+\d{2}.\d{2}.\s+\d{12}\s+(.+)\s+(\d+.\d+)\Z", line
        ):
            transaction_date = t.group(1) + billing_year
            transaction_description = t.group(2).strip()
            transaction_amount = t.group(3)
            # calculated_total_amount += float(transaction_amount)
            print(transaction_date, transaction_description, transaction_amount)

print(calculated_total_amount)
