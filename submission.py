import bisect
import pandas as pd
import math


class Firewall:
    def __init__(self, path_to_csv):
        self.rules = initialize_rules()
        for direction, protocol, ports, addresses in rules_generator(path_to_csv):
            parsed_addresses = tuple(parse_ip_address(adr) for adr in addresses)
            for i in range(int(ports[0]), int(ports[1]) + 1):
                # We're assuming there are no duplicated / overlapping rules.
                bisect.insort(self.rules[(direction, protocol)][i], parsed_addresses)

    def accept_packet(self, direction, protocol, port, ip_address):
        accepted_ip_addresses = self.rules[(direction, protocol)][port]
        parsed_address = parse_ip_address(ip_address)
        return binary_search_ip(accepted_ip_addresses, parsed_address)


def initialize_rules():
    """
    Creates the the empty data structure for storing rules.
    """
    rules = {}
    for direction in ["inbound", "outbound"]:
        for protocol in ["tcp", "udp"]:
            rules[(direction, protocol)] = [[] for _ in range(65536)]
    return rules


def rules_generator(path_to_csv):
    """
    Parses the rules in the CSV file, one by one, and yields them in a list
    representation.
    """
    df = pd.read_csv(path_to_csv)
    for row in df.itertuples():
        current = []
        current.append(row.direction)
        current.append(row.protocol)
        for field in ["port", "address"]:
            temp = getattr(row, field).split("-")
            # If the port / address provided is a number instead of an interval,
            # convert it to an interval.
            # i.e. 300 becomes [300,300]
            if len(temp) == 1:
                temp.append(temp[0])
            current.append(temp)
        yield current
    return


def parse_ip_address(ip_address):
    """
    Converts string representation of an ip address into a tuple, so that it becomes
    comparable.
    """
    return tuple(int(num) for num in ip_address.split("."))


def binary_search_ip(accepted_addresses, address):
    """
    Determines whether the given ip address is within one of the accepted intervals.
    """
    left = 0
    right = len(accepted_addresses)
    while left < right:
        mid = (left + right) // 2
        current_address = accepted_addresses[mid]
        if current_address[0] > address:
            right = mid
        elif current_address[1] < address:
            left = mid + 1
        else:
            return True
    return False


if __name__ == "__main__":
    fw = Firewall("./rules.csv")

    assert binary_search_ip(((123, 123), (124, 126)), 123)
    assert binary_search_ip(((123, 123), (124, 126)), 126)
    assert not binary_search_ip(((123, 123), (126, 126)), 125)

    assert parse_ip_address("1.234.444.0") == (1, 234, 444, 0)
    assert parse_ip_address("0.234.444.0") == (0, 234, 444, 0)

    assert not fw.accept_packet("inbound", "tcp", 81, "192.168.1.2")
    assert not fw.accept_packet("inbound", "udp", 24, "52.12.48.92")

    assert fw.accept_packet("inbound", "tcp", 80, "192.168.1.2")
    assert fw.accept_packet("inbound", "udp", 53, "192.168.2.1")
    assert fw.accept_packet("outbound", "tcp", 10234, "192.168.10.11")

    assert fw.accept_packet("inbound", "udp", 53, "192.168.2.5")
    assert fw.accept_packet("outbound", "udp", 2000, "52.12.48.92")
    assert fw.accept_packet("outbound", "udp", 1000, "52.12.48.92")
