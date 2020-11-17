from flask import Flask, render_template

from utils import vms_list, vm_info

app = Flask(__name__
            , static_url_path='',
            static_folder='static',
            template_folder='templates'
            )


@app.route('/dashboard', methods=['GET'])
def get_main_page():
    vms = vms_list()
    vms_info = [vm_info(vm) for vm in vms]
    return render_template('main.html', vms_info=vms_info)


#     return redirect("<url>" , code=302)

if __name__ == '__main__':
    app.config.from_object(__name__)
    app.run()
