package it.uniroma3.cheatchat.peerdiscoveryserver.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import lombok.Getter;
import lombok.Setter;

import java.util.Set;

@Getter
@Setter
@Entity
public class AddressBook {

    @Id
    private Long id = 1L;

    @OneToMany
    private Set<Peer> peers;

    public void addPeer(Peer peer){
        this.peers.add(peer);
    }

    public void removePeer(Peer peer){
        this.peers.remove(peer);
    }

}
