from flask import Flask, render_template, redirect, request

from utils import vms_list, vm_info, vm_stop, vm_start, vm_change_memory, vm_change_cpu, vm_delete, vm_clone, vm_ssh

app = Flask(__name__
            , static_url_path='',
            static_folder='static',
            template_folder='templates'
            )


@app.route('/dashboard', methods=['GET'])
@app.route('/', methods=['GET'])
def get_dashboard():
    vms = vms_list()
    vms_info = [vm_info(vm) for vm in vms]
    return render_template('main.html', vms_info=vms_info)


@app.route('/start/<vm_name>', methods=['GET'])
def start_vm(vm_name):
    vm_start(vm_name)
    return redirect("/", code=302)


@app.route('/power-off/<vm_name>', methods=['GET'])
def stop_vm(vm_name):
    vm_stop(vm_name)
    return redirect("/", code=302)


@app.route('/change-ram/<vm_name>', methods=['GET'])
def change_vm_ram(vm_name):
    current_ram = vm_info(vm_name)['memory']
    info = vm_info(vm_name)
    current_ram = int(current_ram.replace('MB', ''))
    messages = []
    if info['state'] != 'powered off':
        messages.append("Vm is running it will be turned off for change!")
    return render_template('edit-ram.html', current_ram=current_ram, vm_name=vm_name, messages=messages)


@app.route('/change-ram/', methods=['POST'])
def change_vm_ram_post():
    vm_name = request.form['vm-name']
    info = vm_info(vm_name)
    memory = request.form['memory']
    if info['state'] != 'powered off':
        vm_stop(vm_name)
    vm_change_memory(vm_name, memory)
    return redirect("/", code=302)


@app.route('/change-cpu/<vm_name>', methods=['GET'])
def change_vm_cpu(vm_name):
    current_cpu = vm_info(vm_name)['cpu']
    info = vm_info(vm_name)
    current_cpu = int(current_cpu.replace('MB', ''))
    messages = []
    if info['state'] != 'powered off':
        messages.append("Vm is running it will be turned off for change!")
    return render_template('edit-cpu.html', current_cpu=current_cpu, vm_name=vm_name, messages=messages)


@app.route('/change-cpu/', methods=['POST'])
def change_vm_cpu_post():
    vm_name = request.form['vm-name']
    info = vm_info(vm_name)
    cores = request.form['cores']
    if info['state'] != 'powered off':
        vm_stop(vm_name)
    vm_change_cpu(vm_name, cores)
    return redirect("/", code=302)


@app.route('/delete/<vm_name>', methods=['GET'])
def change_vm_delete(vm_name):
    info = vm_info(vm_name)
    if info['state'] != 'powered off':
        vm_stop(vm_name)
    vm_delete(vm_name)
    return redirect("/", code=302)


@app.route('/clone/<vm_name>', methods=['GET'])
def change_vm_clone(vm_name):
    messages = []
    # info = vm_info(vm_name)
    # if info['state'] != 'powered off':
    #     messages.append("Vm is running it will be turned off for change!")
    return render_template('clone.html', vm_name=vm_name, messages=messages)


@app.route('/clone/', methods=['POST'])
def change_vm_clone_post():
    vm_source = request.form['vm-source']
    vm_new = request.form['vm-new']
    info = vm_info(vm_source)
    if info['state'] != 'powered off':
        vm_stop(vm_source)
    vm_clone(vm_source, vm_new)
    return redirect("/", code=302)


@app.route('/ssh/<vm_name>', methods=['GET'])
def ssh_vm(vm_name):
    messages = []
    info = vm_info(vm_name)
    if info['state'] == 'powered off':
        messages.append("Vm is powered off it will be running for executing commands!")
    return render_template('ssh.html', vm_name=vm_name, messages=messages)


@app.route('/ssh/', methods=['POST'])
def ssh_vm_post():
    vm_name = request.form['vm-name']
    command = request.form['command']
    info = vm_info(vm_name)
    if info['state'] == 'powered off':
        vm_start(vm_name)
    messages = [vm_ssh(vm_name, command)]
    return render_template('ssh.html', vm_name=vm_name, messages=messages)


if __name__ == '__main__':
    app.config.from_object(__name__)
    app.run()
