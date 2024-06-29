import csv
import re
from collections import defaultdict
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def split_fullname(contact):
    fullname = " ".join(contact[:3]).split()
    lastname, firstname, surname = (fullname + ["", ""])[:3]
    contact[:3] = [lastname, firstname, surname]
    return contact


def normalize_phone(phone):
    phone_pattern = re.compile(
        r'(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s*доб\.\s*(\d{4}))?')
    match = phone_pattern.match(phone)
    if match:
        normalized_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        if match.group(7):
            normalized_phone += f" доб.{match.group(7)}"
        return normalized_phone
    return phone


processed_contacts = defaultdict(lambda: ["", "", "", "", "", "", ""])
for contact in contacts_list[1:]:
    contact = split_fullname(contact)
    contact[5] = normalize_phone(contact[5])
    key = (contact[0], contact[1])
    existing_contact = processed_contacts[key]

    for i in range(7):
        if not existing_contact[i] and contact[i]:
            existing_contact[i] = contact[i]

final_contacts_list = [contacts_list[0]] + list(processed_contacts.values())

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts_list)

pprint(final_contacts_list)
