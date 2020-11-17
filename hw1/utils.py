import os
import re


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
    return os.popen(f'vboxmanage clonevm {vm_source} --name={vm_new} --register').read()


if __name__ == '__main__':
    print(vm_info('vm1'))
