from asyncClientServer import AsyncClient
import json

req = {
    "requested_id":"1",
    "data":"Hub&&name&&qwe&&id&&123&&%%Device&&name&&wqe&&id&&234&&"
}
m1 = json.dumps(req)
cl1 = AsyncClient('localhost',8888,4096)
cl1.send_message(m1,time=1)
