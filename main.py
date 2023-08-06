import csv
import re
from pprint import pprint

# Читаем адресную книгу в формате CSV в список contacts_list
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


    phone = re.sub(r'[^0-9]', '', contact[5])
    if len(phone) == 10:
        contact[5] = f"+7({phone[:3]}){phone[3:6]}-{phone[6:8]}-{phone[8:10]}"
    elif len(phone) == 11:
        contact[5] = f"+7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]}"


uni_contacts = {}
for contact in contacts_list:
    key = (contact[0], contact[1], contact[2])
    if key not in uni_contacts:
        uni_contacts[key] = contact
    else:
        uni_contacts[key][5] += f" доб.{re.sub(r'[^0-9]', '', contact[5])}"


contacts_list = list(uni_contacts.values())

# Сохранение данных в новый файл CSV
with open("phonebook.csv", "w", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

# Вывод обработанных данных
pprint(contacts_list)



# Ваша задача: починить адресную книгу, используя регулярные выражения.
# Структура данных будет всегда:
# lastname,firstname,surname,organization,position,phone,email
# Предполагается, что телефон и e-mail у человека может быть только один.
#
# Необходимо:
#
# Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно. В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О.
# Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999.
# Объединить все дублирующиеся записи о человеке в одну.