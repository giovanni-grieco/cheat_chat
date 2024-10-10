package it.uniroma3.cheatchat.peerdiscoveryserver.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PeerDiscoveryController {

    @PostMapping("/hello")
    public String hello() {
        return "Hello, World!";
    }

    @GetMapping("/peers")
    public String peers() {
        return "peers";
    }

}
