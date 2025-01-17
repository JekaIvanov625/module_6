from collections import UserDict
import re
# Стандартний клас
class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
# Клас зберігання імені
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)
# Клас зберігання телефону
class Phone(Field):
    def __init__(self, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)
# Клас зберігання запису
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
    def edit_phone(self, old_phone, new_phone):
        if not self.find_phone(old_phone):
            raise ValueError("Old phone number not found.")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
# Клас адресної книги
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    def find(self, name):
        return self.data.get(name)
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Record for {name} not found.")
    def __str__(self):
        if not self.data:
            return "Address Book is empty."
        return "\n".join(str(record) for record in self.data.values())
# Приклади використання
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()
    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    # Додавання запису John до адресної книги
    book.add_record(john_record)
    # Створення запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    # Виведення всіх записів у книзі
    print(book)
    # Зміна номера для John
    john = book.find("John")
    try:
        john.edit_phone("1234567890", "123")  # Невалідний номер, очікується ValueError
    except ValueError as e:
        print(e)  # Виведе: Phone number must be 10 digits.
    # Замінити номер на валідний
    john.edit_phone("1234567890", "1112223333")
    print(john)  # Виведе оновлену інформацію для John
    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name.value}: {found_phone}")  # Виведе: John: 5555555555
    # Видалення запису Jane
    book.delete("Jane")
    print(book)  # Виведе лише запис John
