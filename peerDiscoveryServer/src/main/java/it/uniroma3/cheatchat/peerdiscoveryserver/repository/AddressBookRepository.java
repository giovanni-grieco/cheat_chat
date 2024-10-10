package it.uniroma3.cheatchat.peerdiscoveryserver.repository;

import it.uniroma3.cheatchat.peerdiscoveryserver.domain.AddressBook;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;

public interface AddressBookRepository extends CrudRepository<AddressBook, Long> {
    public Optional<AddressBook> findById(Long id);
}
