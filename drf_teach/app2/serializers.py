from rest_framework import serializers

# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=128)
#
#     def create(self, validated_data):
#         pass
#
#     def update(self, instance, validated_data): # PUT\PATCH
#         pass
from app2.models import User, Topic, Post

#
# class UserSerializer(serializers.ModelSerializer):
#     # 重写username
#     username = serializers.CharField(max_length=64)
#     password = serializers.CharField(write_only=True) #密码只写,不可以读
#     # 设置辅助性字段, 不用于保存


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name')



class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # 一个序列化的实例, 本身也是一种字段, 可以作为一种字段类型放在这里使用
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'topics')

    def create(self, validated_data):
        topic_data = []
        if validated_data['topics']:
            topic_data = validated_data.pop('topics')

        user_data = validated_data.pop('user')
        # 返回对象 和 创建获取,状态指示器
        user, flag = User.objects.get_or_create(username=user_data['username'])

        post = Post.objects.create(user=user, **validated_data)
        if topic_data:
            post.topics.add(*topic_data)
        return post

    def update(self, instance, validated_data):
        # 获取 topics内容
        request_topics = validated_data.pop('topics')
        # user 内容
        request_user = validated_data.pop('user')
        # validata_data内容
        # 逐一拿取各条数据, instance.title = validated_data.get('title',instance.title)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('title', instance.content)
        instance.save()
        user = instance.user
        user.username = request_user.get('username', user.username)
        user.save()
        instance.topics.set(request_topics, clear=True)
        instance.save()
        return instance

class PostBSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'topics')
        depth = 1 # 正向序列化 depth 指定嵌套深度


class PostHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.CharField(source='user.username')
    class Meta:
        model = Post
        fields = ('goto', 'id', 'title', 'content', 'created', 'user', 'topics')
        depth = 1 # 正向序列化 depth 指定嵌套深度