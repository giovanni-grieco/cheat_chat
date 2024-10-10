package it.uniroma3.cheatchat.peerdiscoveryserver.controller.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class PeerResponse {
    private String username;
    private String ip;
    private String lastSeen;
}
