package it.uniroma3.cheatchat.peerdiscoveryserver.repository;

import it.uniroma3.cheatchat.peerdiscoveryserver.domain.Peer;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;

public interface PeerRepository extends CrudRepository<Peer, String> {
    Optional<Peer> findByUsername(String username);
}
