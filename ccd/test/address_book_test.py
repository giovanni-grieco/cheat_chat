from ccd.address_book import AddressBook
from ccd.peer import Peer


def address_book_add():
    ab = AddressBook()
    p = Peer("Henderson", "1.2.3.4", "30s")
    ab.add_peer(p)
    print(ab.to_string())

if __name__ == '__main__':
    address_book_add()
