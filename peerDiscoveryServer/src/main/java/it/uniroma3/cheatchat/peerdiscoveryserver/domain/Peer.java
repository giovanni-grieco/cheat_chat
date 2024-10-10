package it.uniroma3.cheatchat.peerdiscoveryserver.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@Entity
public class Peer {

    @Id
    private String username;
    private String ip;
    private LocalDateTime lastSeen;

    public int hashCode() {
        return this.username.hashCode();
    }

    public boolean equals(Object obj) {
        if (obj == null) {
            return false;
        }
        if (obj instanceof Peer) {
            Peer peer = (Peer) obj;
            return this.username.equals(peer.username);
        }
        return false;
    }
}
