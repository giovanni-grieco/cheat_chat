package it.uniroma3.cheatchat.peerdiscoveryserver.repository;

import it.uniroma3.cheatchat.peerdiscoveryserver.domain.Peer;
import org.springframework.data.repository.CrudRepository;

public interface PeerRepository extends CrudRepository<Peer, String> {
    Peer findByUsername(String username);
}
