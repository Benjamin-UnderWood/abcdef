# websocket 学习文档

[rfc websocket](https://www.rfc-editor.org/rfc/rfc6455.html)

[rfc websocket 中文翻译](https://juejin.cn/post/6844903779192569869)

[iana websocket 协议注册表](https://www.iana.org/assignments/websocket/websocket.xhtml)

[官方 websocket api](https://html.spec.whatwg.org/multipage/web-sockets.html#the-websocket-interface)

[websocket api](https://developer.mozilla.org/zh-CN/docs/Web/API/WebSocket) 



### [http1.1 如何协议升级](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Protocol_upgrade_mechanism)

**http机制**

允许将一个已建立的连接升级成新的、不相容的协议。这篇指南涵盖了其工作原理和使用场景。



**传输层安全协议 TLS** 支持由服务器端发起



## 流程



**客户端请求**

![image-20211223111529791](assets/image-20211223111529791.png)

```
Connection: Upgrade  升级请求
Upgrade: WebSocket  指定一项或多项协议名 按优先级排序，以逗号分隔
```

**Sec-WebSocket-Extensions**

* 指定一个或多个请求服务器使用的协议级WebSocket扩展
* 值来自[IANA WebSocket 扩展名注册表](https://www.iana.org/assignments/websocket/websocket.xml#extension-name)

**Sec-WebSocket-Key**

* 向服务器提供所需的信息，以确认客户端有权请求升级到 WebSocket
* 不提供安全性
* 有助于防止非 WebSocket 客户端无意中或误用请求 WebSocket 连接。



**Sec-WebSocket-Version**
请求头
指定客户端希望使用的 WebSocket 协议版本



**Sec-WebSocket-Accept**
当服务器愿意发起 WebSocket 连接时，在打开握手过程中包含在来自服务器的响应消息中。它不会在响应标题中出现不止一次。





服务器同意, 返回

```
HTTP/1.1 101 Switching Protocols
Upgrade
```

服务器不同意

```
返回一个常规的响应：例如一个200 OK
```



升级完成了，连接就变成了双向管道。并且可以通过新协议完成启动升级的请求。





## 场景

用 [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) 建立WebSocket连接时，不用操心升级的过程, API已经实现了这一步

```
webSocket = new WebSocket("ws://destination.server.ext", "optionalProtocol");
```

* 用 `"wss://"` 地址格式来打开安全的WebSocket连接。







**属性**

```
Socket.readyState	
只读属性 readyState 表示连接状态，可以是以下值：

0 - 表示连接尚未建立。

1 - 表示连接已建立，可以进行通信。

2 - 表示连接正在进行关闭。

3 - 表示连接已经关闭或者连接不能打开。

Socket.bufferedAmount	
只读属性 bufferedAmount 已被 send() 放入正在队列中等待传输，但是还没有发出的 UTF-8 文本字节数。


WebSocket.binaryType
使用二进制的数据类型连接。

WebSocket.bufferedAmount 只读
未发送至服务器的字节数。

WebSocket.extensions 只读
服务器选择的扩展。

WebSocket.onclose
用于指定连接关闭后的回调函数。

WebSocket.onerror
用于指定连接失败后的回调函数。

WebSocket.onmessage
用于指定当从服务器接受到信息时的回调函数。

WebSocket.onopen
用于指定连接成功后的回调函数。

WebSocket.protocol 只读
服务器选择的下属协议。

WebSocket.readyState 只读
当前的链接状态。

WebSocket.url 只读
WebSocket 的绝对路径。
```



**事件**

| 事件    | 事件处理程序     | 描述                       |
| :------ | :--------------- | :------------------------- |
| open    | Socket.onopen    | 连接建立时触发             |
| message | Socket.onmessage | 客户端接收服务端数据时触发 |
| error   | Socket.onerror   | 通信发生错误时触发         |
| close   | Socket.onclose   | 连接关闭时触发             |



**方法**

| 方法           | 描述             |
| :------------- | :--------------- |
| Socket.send()  | 使用连接发送数据 |
| Socket.close() | 关闭连接         |

















# django channels

## 示例

### 配置

**添加 channel 应用**

**asgi模块配置**

```
ASGI_APPLICATION = 'realtime_graph.asgi.application'
```



**配置CHANNEL_LAYERS**

```
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)]
        }
    }
}
```

* **layer 是什么?** 帮助我们多个consumer之间通信.

* 在 **consumer类** 外面进行消息推送, 推送消息给多个客户端需要利用 **channel layer**

  



### asgi.py

**配置asgi**

```
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from coins.routing import ws_urlpatterns

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})
```

* 描述了http 如何路由
  *   `get_asgi_application()`
* 描述了websocket 如何路由
  * `URLRouter()`
  * `AuthMiddlewareStack()`



### routing.py

````
ws_urlpatterns = [
    path('ws/coins/', CoinsConsumer.as_asgi()),
]
````

* 指定了消费者是谁.



### consumers.py

```
from channels.generic.websocket import AsyncWebsocketConsumer

class GraphConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        for i in range(5):
            await self.send(json.dumps({'value': randint(10, 20)}))
            await sleep(1)
```

* `AsyncWebsocketConsumer`

* 连接时触发
* 关闭连接时触发
* 收到消息后触发
* 如何将channel 分组





### tasks.py

```
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()


async_to_sync(channel_layer.group_send)('coins', 
{
  'type': 'send_new_data',
  'text': coins
})
```

* **get_channel_layer() 获取的是哪个layer**

  



## 概念

在 **consumer类** 外面进行消息推送, 推送消息给多个客户端需要利用 **channel layer**

### channel layer

允许多个consumer实例之间互相通信, 以及与**外部django程序** 实现互通.

#### channel

表示一个发送消息的通道, 

每个channel都有一个名称, 

每个拥有这个名称的人都可以往这个channel里面发送消息

```
async_to_sync(channel_layer.send)(
'coins', 
{
  'type': 'send_new_data',
  'text': coins
})
```

* **layer中的所有方法都是异步的.** 从同步环境发送事件需要async_to_sync 包装
* **type含义**
  * 将消息转发到对应消费者类中的对应方法进行处理.
* **如何确定的当前channel_layer是谁?**
  * 一个请求确定一个layer吗?
* **一个consumer 只有一个group吗?**
* 当存在两个consumer, 并且consumer 都存在相同方法时, 会把消息转发到哪个consumer的方法上?





#### group

多个 **channel name**, 可以组成一个group , 一个group 对应一个名称.

每个拥有这个 **group name**的人都可以往这个group 添加 删除 channel

**group 中 channel 的增删方法**

```
增加
self.channel_layer.group_add('coins', self.channel_name)

删除
self.channel_layer.group_discard('coins', self.channel_name)
```



并且可以向group 发送消息.

```
async_to_sync(channel_layer.group_send)('coins', 
{
  'type': 'send_new_data',
  'text': coins
})
```





# 实验

### 实验1

1. 向指定的channel 发送消息
2. 向一个layer group 中的所有channel 发送消息
3. 一个consumer 对应了一个请求链接, 多个consumer 之间相互通信
   1. 利用channel 名称, 发送信息.







# 如何调试websocket

### chrome调试

https://stackoverflow.com/questions/5751495/debugging-websocket-in-google-chrome

```
二进制帧将显示长度和时间戳，并指示它们是否被屏蔽。文本框将显示还包括负载内容。
```



###  wirshark调试连接





# 问题

1. 如何向websocket 发送数据, django channels 在哪里接收数据?

2. http 提交ip list以及相应参数 给后端,后端组装成ping 语句. 返回响应地址,然后客户端开启ws
   1. 用户点击执行.后端触发执行相应consumer.
   2. 并 向consumer 发送数据触发执行.
3. consumer 要区分开.



````
self.scope[url_route] 路径参数
query_string 查询字符串
type websocket
````



1. 不同的请求consumer  channel name 默认是不通的.





**开启一个ws后 view 访问异常慢**









# 需求

**单用户**

* 一个用户使用ping功能 开通一个websocket

* 一个websocket 对应整个ping功能

* ping功能 可以添加多个组, 一个组在前端表示一个PING列表视图card,  每个组前端生成一个uuid 号码

* 一个组有一组IP, 每个IP需要在后端开启一个进程去ping.并把结果返回. 

* 多个组都是PING功能所以是相同的channel, 对应一个websocket 链接, 把数据返回给前端

**添加IP**

* 生成UUID 
* 通过 http 请求,携带用户ID和表示前端某个ping视图的UUID
*  添加一组IP



```
{
user: 工号,    # group
ping组 号				#  
}
```





**多用户**

* 如果一个用户想将自己ping 展示给其他人
* 公共 ping group  ping结果展示给所有人.
* 每个人一个 ping group  ping结果可以展示给某个人.





**删除不通IP**

* 所有返回的IP都放入一个list
* 有错误返回的ip写入全局list
* 过滤  有错误IP 差集即可

**停止 有错误IP的ping**  

也就是说返回值要有进程号







**创建组**  

* 通过 时间戳
* 当有IP需要执行时, 创建组请求. 记录**IP组表**内.  
* **方法一** 发送ping请求的同时向后端发送组ID





**查看成功率**  

提交信息

```
组id
floor_time 时间
time_range 时间跨度 120秒
```

```
from datetime import datetime, timedelta

date_filter = dict(created__gte=datetime.now() - timedelta(30), created__lte=datetime.now()) 

you can filter more customize 
start_date = '2021-05-21'
end_date = '2021-05-24'
date_filter = dict(created__gte=start_date), created__lte=end_date)

objs  = Klash.objects.filter(**date_filter) # Klash = your model name 
```

```
Payload.objects.filter(user=user_id, timestamp__range=[start_date,end_date]
```

* ```
  https://docs.djangoproject.com/en/3.2/ref/models/querysets/#date  吧
  ```

* 



**删除组**

* **方法一** 前端自己过滤组ID



* **方法二**  



### 发送给其他人

**组涉及权限吗**





### 消息系统(通知)

发送给某人一个消息

发送的是一个链接, 用户点开链接跳转到响应页面, 并且添加了

每秒去请求通知链接携带用户参数













