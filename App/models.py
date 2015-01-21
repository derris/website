from django.db import models
from django.db.models import DO_NOTHING
import datetime
# Create your models here.

BoolCharacter=(('Y','是'),('N','否'))

class BaseModel(models.Model):
    ''''''
    rec_name = models.IntegerField('创建人员')
    remark = models.CharField('备注',blank=True,max_length=50,null=True)
    def __getitem__(self,k):
        return self.__getattribute__(k)
    def __setitem__(self, key, value):
        if value == None:
            self.__setattr__(key,None)
        elif issubclass(type(self._meta.get_field_by_name(key)[0]),models.fields.DateTimeField):
            if isinstance(value,str):
                if str == '':
                    self.__setattr__(key,None)
                else:
                    self.__setattr__(key,datetime.datetime.strptime(value,'%Y-%m-%d %H:%M:%S'))
            else:
                raise Exception("日期时间型参数错误")
        elif issubclass(type(self._meta.get_field_by_name(key)[0]),models.fields.DateField):
            if isinstance(value,str):
                if str == '':
                    self.__setattr__(key,None)
                else:
                    self.__setattr__(key,datetime.datetime.strptime(value,'%Y-%m-%d').date())
            else:
                raise Exception("日期型参数错误")
        else:
            self.__setattr__(key,value)
    def clientToServerDataTrans(self):
        '''字段值转换'''
        for colModel in self._meta.local_fields:
            if issubclass(type(colModel),models.fields.related.ForeignKey):
                if colModel.null == True:
                    if self[colModel.name + '_id'] == '':
                        self[colModel.name] = colModel.get_default()
                else:
                    if self[colModel.name + '_id'] == '':
                        raise Exception(colModel.verbose_name + '，存在非法值')
            else:
                if colModel.null == True:
                    if self[colModel.name] == '':
                        self[colModel.name] = colModel.get_default()
                else:
                    if self[colModel.name] == '':
                        raise Exception(colModel.verbose_name + '，存在非法值')
    class Meta:
        abstract = True
class User(BaseModel):
    id = models.CharField('pk',primary_key=True,max_length=36)
    username = models.CharField('用户',max_length=10)
    pw = models.CharField('密码',max_length=40)
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'user'
class ArticleType(BaseModel):
    id = models.CharField('pk',primary_key=True,max_length=36)
    name = models.CharField('类型名称',max_length=50)
    description = models.CharField('描述',max_length=100,blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'ArticleType'
class Article(BaseModel):
    id = models.CharField('pk',primary_key=True,max_length=36)
    articletype = models.ForeignKey('ArticleType', \
        verbose_name='文章类型',related_name='article',db_column='articletype_id', \
        on_delete=DO_NOTHING)
    title = models.CharField('标题',max_length=100)
    content = models.TextField('内容')
    titleimage = models.CharField('标题图片文件名',max_length=50)
    publishdate = models.DateTimeField('发布时间')
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'Article'