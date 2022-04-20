;
; BIND data file for local loopback interface
;
$TTL    604800
@       IN      SOA     ns.weedrecognition.com. root.weedrecognition.com. (
                              1         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      ns.weedrecognition.com.
ns      IN      A       192.168.1.101
@       IN      A       192.168.1.101
