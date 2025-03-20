from wakeonlan import send_magic_packet

mac = "94:de:80:21:2f:11" # actual
mac = "94:de:80:21:2f:10" # not correct

send_magic_packet(mac,ip_address="192.168.20.255")