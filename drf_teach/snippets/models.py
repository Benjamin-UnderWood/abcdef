from django.db import models
# Create your models here.
from pygments import highlight
from pygments.formatters.html import HtmlFormatter

from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')  # 标题
    code = models.TextField()  # 代码
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    linenos = models.BooleanField(default=False)  # 是否显示行号
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)  # 代码片段使用的语言
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    class Meta:
        ordering = ('created',)  # 根据创建时间排序

    def save(self, *args, **kwargs):  # 保存每个snippet对象到数据时候额外的提前做一些事情
        # 添加html 样式

        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False  # 行号为真
        options = {'title': self.title} if self.title else {}  # title 存在那么设置为字典
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)  # 执行保存



