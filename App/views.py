from django.shortcuts import render

def test1(request):
    print('321')
    return render(request, "App/test.html")
