"""! @brief `UDPBufferSizeSetup` class right now relies on the Linux kernel command `sysctl` to setup the 
"""
from helpers.subprocess_wrappers import check_call, check_output

class KernelController:
    def __init__(self, shell=True):
        self.shell = shell
    def set_system_value(self, metric, value):
        check_call(f"sudo sysctl -w {metric}={value}", shell = self.shell) #enable shell=True to actually change your system settings



class UDPSocketReceiveController(KernelController):
    def __init__(self):
        super().__init__()
    def reset_rmem(self): #linux default
        self.set_system_value('net.core.rmem_default', 212992)
        self.set_system_value('net.core.rmem_max', 212992)
    def set_rmem(self):
        self.set_system_value('net.core.rmem_default', 16777216)
        self.set_system_value('net.core.rmem_max', 33554432) #16777216*32 = 536870912


class UDPSocketSendController(KernelController):
    def __init__(self):
        super().__init__()
    def reset_wmem(self):
        self.set_system_value('net.core.wmem_default', 212992)
        self.set_system_value('net.core.wmem_max', 212992)
    def set_wmem(self):
        self.set_system_value('net.core.wmem_default', 16777216)
        self.set_system_value('net.core.wmem_max', 536870912)

class TCPSocketReceiveController(KernelController):
    def __init__(self):
        super().__init__()
    def reset_tcp_rmem(self):
        self.set_system_value('net.ipv4.tcp_rmem', '4096 87380 6291456')
    def set_tcp_rmem(self):
        self.set_system_value('net.ipv4.tcp_rmem', '4096 16777216 536870912')

class TCPSocketSendController(KernelController):
    def __init__(self):
        super().__init__()
    def reset_tcp_wmem(self):
        self.set_system_value('net.ipv4.tcp_wmem', '4096 16384 4194304')
    def set_tcp_wmem(self):
        self.set_system_value('net.ipv4.tcp_wmem', '4096 16777216 536870912')

class IPForwardEnabler(KernelController):
    def __init__(self):
        super().__init__()
    def enable(self):
        self.set_system_value('net.ipv4.ip_forward', 1)

    
class RPFilterDisabler(KernelController):
    def __init__(self, interface, shell = True):
        self.interface = interface
        super().__init__()
    def disable_rpf_interface(self):
        rpf_interface = f'net.ipv4.conf.{self.interface}.rp_filter'
        self.set_system_value(rpf_interface, 0)
    def disable_rpf_all(self):
        self.set_system_value('net.ipv4.conf.all.rp_filter',0)


class QDiscController(KernelController):
    def __init__(self, qdisc, shell = True):
        self.qdisc = qdisc
        super().__init__()

    def set_qdisc(qdisc):
        curr_qdisc = check_output('sysctl net.core.default_qdisc', shell=True)
        curr_qdisc = curr_qdisc.split('=')[-1].strip()

        if curr_qdisc != self.qdisc:
            self.set_system_value('set.core.default_qdisc',self.qdisc)
            sys.stderr.write(f'Changed default_qdisc from {curr_qdisc} to {self.qdisc}\n')


