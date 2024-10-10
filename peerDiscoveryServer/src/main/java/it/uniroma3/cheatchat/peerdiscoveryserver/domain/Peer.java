package it.uniroma3.cheatchat.peerdiscoveryserver.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
public class Peer {

    @Id
    private String username;
    private String ip;
}
