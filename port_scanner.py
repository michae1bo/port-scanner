import socket
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose = False):
    open_ports = []
    is_hostname = False
    error = False

    ip_parts = target.split('.')
    if len(ip_parts) == 4:
        for part in ip_parts:
            if len(part) > 3:
                break
            try:
                part_number = int(part)
            except ValueError:
                break
            if 0 > part_number or part_number > 255:
                error = True
                return 'Error: Invalid IP address'
        
    try:
        address = socket.gethostbyname(target)
    except:
        error = True
        return 'Error: Invalid hostname'

    if not error:
        for port in range(port_range[0], port_range[1] + 1):
            s = socket.socket()
            s.settimeout(1)
            if not s.connect_ex((address, port)):
                open_ports.append(port)
            s.close()

    if verbose:
        output_str = 'Open ports for '
        if address != target:
            output_str += f'{target} ({address})'
        else:
            try:
                url = socket.gethostbyaddr(address)[0]
                output_str += f'{url} ({address})'
            except:
                output_str += f'{target}'
        output_str += '\n'
        output_str += f'PORT     SERVICE\n'
        for port in open_ports:
            try:
                service = ports_and_services[port]
            except:
                service = ''
            spaces = 9 - len(str(port))
            output_str += f'{port}'+ spaces * ' ' + f'{service}\n'
        return output_str.rstrip('\n')


    return(open_ports)