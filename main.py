from flask import Flask, jsonify, request
from services.modbus import ModbusClass as Modbus
from configs.modbusConfig import CONNECTINFO
from services.verify import verification
from configs.commandConfig import COMMAND
from configs.profile import PROFILE
app = Flask(__name__)

modbus = Modbus(CONNECTINFO['host'], CONNECTINFO['port'])
print(CONNECTINFO['host'], CONNECTINFO['port'])
# @app.route('/getGoodsFromAGV', methods=['POST'])
# @verification
# def getGoodsFromAGV():
#     try:
#         modbus.getGoodsFromAGV(request.json['orderId'])
#         return jsonify(msg="success")
#     except Exception as e:
#         return jsonify(msg=str(e))

# @app.route('/takeGoodsToAGV', methods=['POST'])
# @verification
# def takeGoodsToAGV():
#     try:
#         modbus.takeGoodsToAGV(request.json['orderId'])
#         return jsonify(msg="success")
#     except Exception as e:
#         return jsonify(msg=str(e))
@app.route('/')
def index():
    return jsonify(msg="alive")

@app.route('/profile')
def profile():
    return jsonify(PROFILE)
    
@app.route('/registers')
@verification
def getRegi():
    return jsonify(modbus.getRegisters())

@app.route('/reconnect')
def reconnect():
    modbus.reconnect()
    return True

@app.route('/command/<command>', methods=['POST'])
def command(command=None):
    if command in COMMAND:
        try:
            if modbus.writeToSlave(modbus.addSerialNum(request.json['orderId'], COMMAND[command])):
                return jsonify(msg="success")
        except Exception as e:
            return jsonify(msg=str(e))

    return jsonify(msg="failed")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)