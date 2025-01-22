from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Phone not found.")
    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            self.add_phone(new_phone)  # Спочатку додаємо новий номер
            self.remove_phone(old_phone)  # Потім видаляємо старий
        else:
            raise ValueError("Phone not found.")
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    def find(self, name):
        return self.data.get(name, None)
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Contact not found.")
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def main():
    book = AddressBook()
    print("Welcome to the address book!")
    while True:
        user_input = input("Enter a command: ").strip().lower()
        if user_input == "add":
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            try:
                record = Record(name)
                record.add_phone(phone)
                book.add_record(record)
                print("Contact added.")
            except ValueError as e:
                print(e)
        elif user_input == "change":
            name = input("Enter name: ")
            old_phone = input("Enter old phone number: ")
            new_phone = input("Enter new phone number: ")
            try:
                record = book.find(name)
                if record:
                    record.edit_phone(old_phone, new_phone)
                    print("Contact updated.")
                else:
                    print("Contact not found.")
            except ValueError as e:
                print(e)
        elif user_input == "phone":
            name = input("Enter name: ")
            record = book.find(name)
            if record:
                print(record)
            else:
                print("Contact not found.")
        elif user_input == "all":
            print(book)
        elif user_input in ["close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command.")
if __name__ == "__main__":
    main()
