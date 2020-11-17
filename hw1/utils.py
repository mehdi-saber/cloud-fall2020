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
    result['state'] = next(re.finditer(r"State:\s+(.+)", cmd_response, re.MULTILINE))[1]
    result['memory'] = next(re.finditer(r"Memory size\s+(.+)", cmd_response, re.MULTILINE))[1]
    return result


if __name__ == '__main__':
    print(vm_info('vm1'))
