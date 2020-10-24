from django.http import HttpResponse
from django.shortcuts import render

id_and_password = {"jl":"3.1415926","jl1":3.14,"jl2":"123456","Tom":"7654321"}
login_error = {'error1':"用户名不存在！",'error2':"密码错误！"}
register_error = {'error1':"用户名长度不符合要求","error2":"该用户名已存在","error3":"密码不符合要求！","error4":"输入密码不一致！"}
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username in id_and_password and password==id_and_password[username]:
            return HttpResponse("sucess!")
        elif not username in id_and_password:
            error1={'error':'用户名不存在！'}
            return render(request,'login.html',error1)
        elif password != id_and_password[username]:
            error2={'error':"密码错误！"}
            return render(request,'login.html',error2)

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if len(username) in range(6,12):
            if len(password) in range(6,12):
                for i in range(len(password)):
                    if '0'<='i'<='9' or 'A'<='i'<='Z' or 'a'<='i'<='z':
                        if password1 == password:
                            id_and_password[username]=password
                            return HttpResponse("注册成功")
                        else:
                            error4={'error':'两次输入密码不一致！'}
                            return render(request, 'register.html', error4)
                    else :
                        error3={"error":'密码由6-12位字母或数字组成！'}
                        return render(request, 'register.html', error3)
            else:
                error2={"error":'请输入6-12位密码！'}
                return render(request, 'register.html', error2)
        else:
            error1 = {"error":"请输入6-12位用户名！"}
            return render(request,'register.html',error1)







