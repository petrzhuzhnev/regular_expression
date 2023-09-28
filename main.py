import csv
import re
from pprint import pprint

def normalize_phone(phone):
    # Приводим номер телефона к нужному формату
    phone = re.sub(r'[^0-9]', '', phone)
    if len(phone) == 10:
        return f"+7({phone[:3]}){phone[3:6]}-{phone[6:8]}-{phone[8:10]}"
    elif len(phone) == 11:
        return f"+7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]}"
    else:
        return ""

def merge_contacts(contacts_list):
    uni_contacts = {}
    for contact in contacts_list:
        key = (contact[0], contact[1], contact[2])
        if key not in uni_contacts:
            uni_contacts[key] = contact
        else:
            # Объединяем телефоны и e-mail при дублировании записей
            uni_contacts[key][5] += f" доб.{re.sub(r'[^0-9]', '', contact[5])}"
            if contact[6]:
                uni_contacts[key][6] = contact[6]
    
    return list(uni_contacts.values())

def main():
    
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    for contact in contacts_list:
        name_parts = re.split(r'\s+', contact[0])
        if len(name_parts) == 3:
            contact[0] = name_parts[0]
            contact[1] = name_parts[1]
            contact[2] = name_parts[2]
        elif len(name_parts) == 2:
            contact[0] = name_parts[0]
            contact[1] = name_parts[1]
            contact[2] = ""

        # Нормализуем номер телефона
        contact[5] = normalize_phone(contact[5])

    contacts_list = merge_contacts(contacts_list)

    # Сохранение данных в новый файл CSV
    with open("phonebook.csv", "w", newline="") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

    # Вывод обработанных данных
    pprint(contacts_list)

if __name__ == "__main__":
    main()
