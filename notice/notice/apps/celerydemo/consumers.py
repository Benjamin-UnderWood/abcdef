import json
import threading
from asyncio import sleep

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class ChatConsumer(AsyncWebsocketConsumer):
    groups = ['broadcast']

    async def connect(self):
        await self.channel_layer.group_add('celery', self.channel_name)
        await self.accept()
        print("进入连接")
        import redis
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        r = redis.Redis(connection_pool=pool)
        await sleep(5)
        dic = r.hget("notice", "wx1047894")
        if dic:
            await self.send(json.dumps(json.loads(dic)))

        # def func():
        #     while True:
        #         await sleep(5)
        #         dic = r.hget("notice", "wx1047894")
        #         if dic:
        #             await self.send(json.dumps(json.loads(dic)))
        # t = threading.Thread(target=)

    async def disconnect(self, code):
        print("断开连接")
        await self.channel_layer.group_discard('celery', self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("打印输出: ", message)

        import redis
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        r = redis.Redis(connection_pool=pool)
        if text_data_json['cmd'] == 'delete': # 命令模式
            l = r.hget("notice", "wx1047894")
            l = json.loads(l)
            l.pop(text_data_json['index'])
            r.hset("notice", "wx1047894", json.dumps(l))
            print("删除完毕")
            l = r.hget("notice", "wx1047894")
            l = json.loads(l)
            await self.send(json.dumps(l))
        elif text_data_json['cmd'] == 'getall': # 命令模式
            l = r.hget("notice", "wx1047894")
            l = json.loads(l)
            await self.send(json.dumps(l))
# socket.send(JSON.stringify({message:"bbb", cmd: "delete", index: 0}));
# socket.send(JSON.stringify({message:"bbb", cmd: "getall"}));

    async def send_new_data(self, event):
        print(event['text'])

# https://stackoverflow.com/questions/39322241/sending-a-message-to-a-single-user-using-django-channels