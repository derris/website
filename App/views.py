from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from decimal import Decimal
from datetime import date,datetime
import json
import os
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from App.utils import *
from App.ueditor_config import UEditorUploadSettings
from website.settings import UPLOAD_PATH
# Create your views here.
class ServerToClientJsonEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj,date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj,Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self,obj)

def test1(request):
    print('321')
    return render(request, "App/test.html")
def test2(request):
    print('123')
    return HttpResponse(json.dumps(UEditorUploadSettings,ensure_ascii=False,cls=ServerToClientJsonEncoder))
def _uploadfile(fileObj,):
    lrtn={}
    try:
        if fileObj:
            sourceName = fileObj.name
            fileName = datetime.now().strftime('%Y%m%d%H%M%S%f')
            fileExt = sourceName.split('.')[1]
            #检查文件扩展名
            UEditorUploadSettings['fileAllowFiles'].index('.' + fileExt.lower())
            if not os.path.exists(UPLOAD_PATH):
                return "Error:上传路径错误！"
            if fileObj._size > UEditorUploadSettings['']:
                return "Error:"
            pathfile = os.path.join(UPLOAD_PATH,fileName + '.' + fileExt)
            destination = open(pathfile,'wb+')
            for chunk in fileObj.chunks():
                destination.write(chunk)
            destination.close()
            if ("." + fileExt) in UEditorUploadSettings['imageAllowFiles']:
                if UEditorUploadSettings['imageCompressEnable']:
                    paththumbfile = os.path.join(UPLOAD_PATH,fileName + '_thum' + '.' + fileExt)
                    im = Image.open(pathfile)
                    im.thumbnail((720,720))
                    im.save(paththumbfile)
            lrtn = {
                'original':sourceName,
                'name':fileName + '.' + fileExt,
                'size':fileObj._size,
                'type':'.' + fileExt,
                'state':'SUCCESS',
                'url':'static/upload/' + fileName + '.' + fileExt
            }
    except ValueError as e:
        return "Error:文件类型错误！"
    return lrtn

@csrf_exempt
def dealPAjax(request):
    ls_err = ""
    l_rtn = {}
    try:
        #request_type = request.REQUEST['action']
        if request.method == 'GET': #请求配置
            print('get')
            request_type = request.GET['action']
            if request_type == 'config':
                return HttpResponse(json.dumps(UEditorUploadSettings,ensure_ascii=False,cls=ServerToClientJsonEncoder))
            else:
                ls_err = '配置请求参数错误！'
        elif request.method == 'POST': #具体POST提交
            print('post')
            request_type = request.REQUEST['action']
            print(request_type)
            if request_type == 'uploadimage':#上传图片
                fileObj = request.FILES.get('upfile',None)
                l_rtn = _uploadfile(fileObj)
            if request_type == 'uploadscrawl':#上传图片
                fileObj = request.FILES.get('upfile',None)
                l_rtn = _uploadfile(fileObj)

        else:
            print(request.methon)
            l_rtn = {"error": [ls_err],
                     "msg": '',
                     "stateCod": -1}
        return (HttpResponse(json.dumps(l_rtn, ensure_ascii=False)))
    except Exception as e:
        logErr("ajaxResp.dealPAjax执行错误：%s" % str(e.args))
        ls_err = str(e.args)
    finally:
        #sql日志
        for q in connection.queries:
            log(q)
    l_rtn = {
        "error": [ls_err],
        "msg": "Ueditor执行失败",
        "stateCod": -1,
    }
    return ( HttpResponse(json.dumps(l_rtn, ensure_ascii=False)))