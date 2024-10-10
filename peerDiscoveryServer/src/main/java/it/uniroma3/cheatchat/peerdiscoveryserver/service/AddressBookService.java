package it.uniroma3.cheatchat.peerdiscoveryserver.service;

import it.uniroma3.cheatchat.peerdiscoveryserver.domain.AddressBook;
import it.uniroma3.cheatchat.peerdiscoveryserver.domain.Peer;
import it.uniroma3.cheatchat.peerdiscoveryserver.repository.AddressBookRepository;
import it.uniroma3.cheatchat.peerdiscoveryserver.repository.PeerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class AddressBookService {

    @Autowired
    private AddressBookRepository addressBookRepository;

    @Autowired
    private PeerRepository peerRepository;

    public AddressBookService() {
        AddressBook ab = new AddressBook();
        addressBookRepository.save(ab);
    }

    public AddressBook getAddressBook() {
        return addressBookRepository.findById(1L).orElse(null);
    }

    public Peer addPeer(String username, String ip) {
        AddressBook ab = addressBookRepository.findById(1L).orElse(null);
        Peer peer = peerRepository.findByUsername(username).orElse(null);
        if (peer == null) {
            peer = new Peer();
            peer.setUsername(username);
            peer.setIp(ip);
            peer.setLastSeen(LocalDateTime.now());
            peer = peerRepository.save(peer);
        } else if (peer.getIp().equals(ip)) {
            peer.setLastSeen(LocalDateTime.now());
            peer = peerRepository.save(peer);
        }
        ab.addPeer(peer);
        addressBookRepository.save(ab);
        return peer;
    }


}
