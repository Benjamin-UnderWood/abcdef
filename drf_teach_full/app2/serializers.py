from rest_framework import serializers
from .models import User, Topic, Post


# 遵循RESTful规范，一个名词url只处理一个资源。所以，不在嵌套的关系字段中同时创建对象。
# /users/ POST  去创建User对象， 不会去/posts/，创建post对象的同时创建user
# 前后端协商接口的时候，就要将逻辑区分开，不要混在一起

class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'posts')


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id','name')


class PostSerializer(serializers.ModelSerializer):
    # user = UserSerializer()   # 以后，user的处理，使用UserSerializer
    # topics = serializers.PrimaryKeyRelatedField()
    # content = serializers.CharField(style={'base_template': 'textarea.html'})
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created', 'user', 'topics')


    # password

    # 根据model 模型的定义，自动生成默认字段
    # 自动生成相应的验证器
    # create update方法
    # 自动默认将关系字段，映射成PrimaryKeyRelatedField






    # def create(self, validated_data):
    #     topic_data = []
    #     if validated_data['topics']:
    #         topic_data = validated_data.pop('topics')
    #     user_data = validated_data.pop('user')
    #     user, flag = User.objects.get_or_create(username=user_data['username'])
    #     post = Post.objects.create(user=user, **validated_data)
    #     if topic_data:
    #         post.topics.add(*topic_data)
    #     return post
    #
    # def update(self,instace, validated_data):
    #     pass
    #     # 获取topic的内容，user的内容，validated_data
    #     # 逐一拿取各条数据，  instance.title = validated_data.get('title',instance.title)
    #     # instance.save()
    #     # user  = instance.user   user.username = user_data.get('username', user.username)
    #     # user.save()


# class PostSerializer(serializers.HyperlinkedModelSerializer):
#
#
#     class Meta:
#         model = Post
#         fields = ('url', 'title', 'content', 'created', 'user', 'topics')


    # serializer = PostSerializer(queryset, context={'request': request})
    # {'request': None}
    # {model_name}-detail   name= 'post-detail'  /posts/<int:pk>/

    # view_name和lookup_field


class PostSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created', )