from . import server

def train(taskstatus, model):
    ret = {}
    try:
        print("run thread")

        if taskstatus.canceled:
            return {'result': 'canceled'}

        return {'result': 'ok'}

    except Exception as e:
        traceback.print_exc()
        return {'error_msg': str(e)}
