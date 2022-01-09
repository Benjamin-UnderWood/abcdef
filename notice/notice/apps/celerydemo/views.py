import json
import time

import redis
from asgiref.sync import async_to_sync
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

class TestView(APIView):
    def get(self, request):
        # 必须先创建连接,才能发送消息
        # 组发送消息
        # async_to_sync(channel_layer.group_send)('celery', {'type': 'send_new_data',
        #                                                   'text': "coins"})
        # 期望向某个consumer发送消息
        # async_to_sync(channel_layer.send('chat-consumer', {'type': 'send_new_data',
        #                                                   'text': "coins"}))

        pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        r = redis.Redis(connection_pool=pool)
        if r.hexists("notice", "wx1047894"):
            l = r.hget("notice", "wx1047894")
            l = json.loads(l)
            l.append({"timestamp": time.time(), "msg": "A任务执行完毕", "url": "localhost:8000"})
            l = json.dumps(l)
        else:
            l = json.dumps([{"timestamp": time.time(), "msg": "A任务执行完毕", "url": "localhost:8000"}])
        r.hset("notice", "wx1047894", l)
        print("111")
        return Response({'A': 1}, status=status.HTTP_200_OK)
