# -*- coding:utf-8 -*-
from app import creat_app
app = creat_app()






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=90, debug=app.config['DEBUG'], threaded=True)