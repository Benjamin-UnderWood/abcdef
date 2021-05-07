from rest_framework import serializers

from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # read_only 只读不允许写
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)  #
    code = serializers.CharField(style={'base template': 'textarea.html'})  # style 默认样式 渲染成什么样式的主体
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        创建
        :param validated_data: 经过验证的数据 字典格式
        :return:
        """

        return Snippet.objects.create(**validated_data)  # 创建模型

    def update(self, instance, validated_data):
        """
        更新
        :param instance: 要更新的实例
        :param validated_data: 经过验证的数据 字典格式
        :return:
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)

        instance.save()  # 保存

        return instance  # restful 要求返回更新的模型


###########################################
############ModelSerializer使用#############
###########################################


class SnippetModelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        # 针对哪个model 进行序列化
        model = Snippet
        # 针对哪个字段进行序列化
        fields = ('id',
                  'title',
                  'code',
                  'linenos',
                  'language',
                  'style',
                  'owner')

        # modelSerializer 为我们提供了 create, update 方法


from django.contrib.auth.models import User


class UserModelSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')


###########################################
############HyperlinkSerializer使用#############
###########################################

class SnippetHyperlinkSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'title', 'code', 'linenos', 'language', 'style', 'owner', 'highlight')


class UserHyperlinkSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets',)



