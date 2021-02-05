from flask import Flask, request

from utils import vm_stop

app = Flask(__name__
            , static_url_path='',
            static_folder='static',
            template_folder='templates'
            )


# @app.route('/start/<vm_name>', methods=['GET'])
# def start_vm(vm_name):
#     return vm_start(vm_name)
#
#
# @app.route('/stop/<vm_name>', methods=['GET'])
# def stop_vm(vm_name):
#     return vm_stop(vm_name)

@app.route('/stats/<vm_name>', methods=['POST'])
def stats_vm(vm_name):
    print(request.form['data'])
    return "ok"


if __name__ == '__main__':
    app.config.from_object(__name__)
    app.run(host='0.0.0.0')
