import os
import re
import socket
from contextlib import closing


def vms_list():
    cmd_response = os.popen('vboxmanage list vms').read()
    matches = re.finditer(r"\"(.+)\" {.+}", cmd_response, re.MULTILINE)
    matches = [match[1] for match in matches]
    return matches


def vm_info(vm_name):
    cmd_response = os.popen(f'vboxmanage showvminfo {vm_name}').read()
    result = dict()
    result['name'] = vm_name
    result['cpu'] = next(re.finditer(r"Number of CPUs:\s+(\d+)", cmd_response, re.MULTILINE))[1]
    state = next(re.finditer(r"State:\s+(.+) \((.+)\)", cmd_response, re.MULTILINE))
    result['state'], result['state_since'] = state[1], state[2]
    result['memory'] = next(re.finditer(r"Memory size\s+(.+)", cmd_response, re.MULTILINE))[1]
    ssh_rgx = r"name = guestssh, protocol = tcp, host ip = , host port = (\d+), guest ip = , guest port = 22"
    result['ssh_port'] = next(re.finditer(ssh_rgx, cmd_response, re.MULTILINE))[1]
    return result


def vm_start(vm_name):
    return os.popen(f'vboxmanage startvm {vm_name} --type headless').read()


def vm_stop(vm_name):
    return os.popen(f'vboxmanage controlvm {vm_name} poweroff soft').read()


def vm_change_cpu(vm_name, cores):
    return os.popen(f'vboxmanage modifyvm {vm_name} --cpus {cores}').read()


def vm_change_memory(vm_name, memory):
    return os.popen(f'vboxmanage modifyvm {vm_name} --memory {memory}').read()


def vm_delete(vm_name):
    return os.popen(f'vboxmanage unregistervm {vm_name} --delete').read()


def vm_clone(vm_source, vm_new):
    os.popen(f'vboxmanage clonevm {vm_source} --name={vm_new} --register').read()
    free_port = get_free_port()
    os.popen(f"VBoxManage modifyvm \"{vm_new}\" --natpf1 delete \"guestssh\"").read()
    return os.popen(f"VBoxManage modifyvm \"{vm_new}\" --natpf1 \"guestssh,tcp,,{free_port},,22\"").read()


def vm_ssh(vm_name, command):
    info = vm_info(vm_name)
    return os.popen(f'ssh -p{info["ssh_port"]} vm1@127.0.0.1 -o "StrictHostKeyChecking=no" "{command}"').read()


def get_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


if __name__ == '__main__':
    print(vm_ssh('vm1', 'echo "hello" > ~/1.txt'))
    print(vm_ssh('vm1', "cat ~/1.txt"))
