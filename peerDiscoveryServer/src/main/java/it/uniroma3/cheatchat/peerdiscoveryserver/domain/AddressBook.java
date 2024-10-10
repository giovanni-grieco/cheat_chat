package it.uniroma3.cheatchat.peerdiscoveryserver.domain;

import jakarta.persistence.*;

import java.util.Set;

@Entity
public class AddressBook {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    @OneToMany
    private Set<Peer> peers;



}
