from django.shortcuts import render
from django.http import HttpResponse
from decimal import Decimal
from datetime import date,datetime
import json
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
    l_rtn = [{
        "id":0,
        "title":"title0",
        "description":"description0",
        "price":3.95
    },
             {
        "id":1,
        "title":"title1",
        "description":"description1",
        "price":9.99
    }]
    return HttpResponse(json.dumps(l_rtn,ensure_ascii=False,cls=ServerToClientJsonEncoder))
