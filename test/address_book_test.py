import time

from address_book.address_book import AddressBook
from convos.peer import Peer


def address_book_add():
    ab = AddressBook()
    p = Peer("Henderson", "1.2.3.4", time.time())
    ab.add_peer(p)
    print(ab.to_string())

if __name__ == '__main__':
    address_book_add()
