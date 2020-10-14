import asyncio
import json

class AsyncServer:
    def __init__(self,addr='localhost',port=6000,message_maxlen=4096):
        self.addr = addr
        self.port = port
        self.message_maxlen=message_maxlen
        self.event_loop = asyncio.get_event_loop()

    async def server(self,reader,writer):
        data = await reader.read(self.message_maxlen)
        data = data.decode()
        answer = self.parse_json(data).encode()
        writer.write(answer)
        await writer.drain()
        writer.close()

    def run(self):
        core = asyncio.start_server(self.server, self.addr, self.port, loop=self.event_loop)
        server = self.event_loop.run_until_complete(core)
        try:
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            server.close()
            loop.run_until_complete(server.wait_closed())
            loop.close()

    def parse_json(self, js_str):
        answer = {}
        py_obj = json.loads(js_str)
        sub_cathegories = {}
        try:
            answer['requested_id'] = py_obj.pop('requested_id')
            data = py_obj['data'].split('%%')
            for subdata in data:
                sub_dict = {}
                inner_sub_dict = {}
                sd = subdata.split('&&')
                main_name = sd.pop(0)
                while sd:
                    if len(sd) <= 1:
                        break
                    else:
                        key = sd.pop(0)
                        value = sd.pop(0)
                        if key == '' or value == '':
                            continue
                        else:
                            inner_sub_dict[key] = value
                sub_cathegories[main_name] = inner_sub_dict
            answer['data'] = sub_cathegories
            answer = json.dumps(answer, indent=4)
            return answer
        except KeyError:
            print('can`t get data, it`s broken')


class AsyncClient:
    def __init__(self,addr='localhost',port=6000,message_maxlen=4096):
        self.addr = addr
        self.port = port
        self.message_maxlen=message_maxlen
        self.event_loop = asyncio.get_event_loop()

    async def connect(self,message,time):
        reader, writer = await asyncio.open_connection(self.addr, self.port)
        await asyncio.sleep(time)
        writer.write(message.encode())
        data = await reader.read(self.message_maxlen)
        data = data.decode()
        print('Recieved:')
        print(data)
        writer.close()

    def send_message(self,message,time=0,):
        self.event_loop.run_until_complete(self.connect(message,time))


