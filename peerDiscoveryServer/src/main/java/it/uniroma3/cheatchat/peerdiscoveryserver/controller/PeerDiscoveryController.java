package it.uniroma3.cheatchat.peerdiscoveryserver.controller;

import it.uniroma3.cheatchat.peerdiscoveryserver.controller.dto.PeerDto;
import it.uniroma3.cheatchat.peerdiscoveryserver.controller.dto.PeerResponse;
import it.uniroma3.cheatchat.peerdiscoveryserver.domain.Peer;
import it.uniroma3.cheatchat.peerdiscoveryserver.service.AddressBookService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class PeerDiscoveryController {

    @Autowired
    private AddressBookService bookService;

    @PostMapping("/hello")
    public ResponseEntity<?> hello(@RequestBody PeerDto peerDto) {
        Peer peer = bookService.addPeer(peerDto.getUsername(), peerDto.getIp());
        return ResponseEntity.ok(new PeerResponse(peer.getUsername(),peer.getIp(),peer.getLastSeen().toString()));
    }

    @GetMapping("/peers")
    public String peers() {
        return "peers";
    }

}
