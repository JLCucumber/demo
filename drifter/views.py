from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from functools import wraps
from drifter.models import *

# login_error = {'error1': "用户名不存在！", 'error2': "密码错误！"}
# register_error = {'error1': "用户名长度不符合要求", "error2": "该用户名已存在", "error3": "密码不符合要求！", "error4": "输入密码不一致！"}


# a = drifter_user.objects.create(username=768073747,password=3.1415926,sex=0)
def check_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        ret = request.session.get("login")

        if ret == "success":
            return func(request, *args, **kwargs)
        else:
            next_url = request.path_info
            print(next_url)
            return redirect("/drifter/login/?next={}".format(next_url))

    return inner


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        login_username = request.POST.get('username')
        login_password = request.POST.get('password')
        a = drifter_user.objects.filter(username=login_username)
        b = drifter_user.objects.filter(username=login_username, password=login_password)
        next_url = request.GET.get("next")

        if a.exists():
            if b.exists():
                if next_url:
                    rep = redirect(next_url)
                else:
                    rep = redirect("/drifter/gateway/")

                request.session['login'] = 'success'
                request.session["username"] = login_username
                request.session.set_expiry(100)
                return rep

                # return render(request,'gateway.html')
            else:
                error1 = {'error': '密码错误'}
                return render(request, 'login.html', error1)
        else:
            error1 = {'error': '用户名不存在！'}
            return render(request, 'login.html', error1)
    ret = request.session.get('login')
    if ret == 'success':
        return redirect("/drifter/gateway")
    else:
        return render(request, "login.html")


@check_login
def gateway(request):
    username = request.session.get("username")
    return render(request, "gateway.html", {'username': username})


def logout(request):
    request.session.flush()
    request.session.delete()
    return render(request, "login.html")


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        reg_nicheng = request.POST.get('nicheng')
        reg_username = request.POST.get('username')
        reg_password = request.POST.get('password')
        reg_password1 = request.POST.get('password1')
        reg_sex = request.POST.get('sex')
        reg_birth = request.POST.get('date_of_birth')
        reg_hobby = request.POST.get('hobby')
        reg_email = request.POST.get('email')
        a = drifter_user.objects.filter(username=reg_username)
        if len(reg_username) in range(4, 20):
            for i in range(len(reg_username)):
                if 1 <= i <= 9 or ord('A') <= i <= ord('Z') or ord('a') <= i <= ord('z'):
                    if len(reg_password) in range(4, 20):
                        for s in range(len(reg_password)):
                            if 0 <= s <= 9 or ord('A') <= s <= ord('Z') or ord('a') <= s <= ord('z'):
                                if reg_password1 == reg_password:
                                    if not a.exists():
                                        drifter_user.objects.create(nicheng=reg_nicheng, username=reg_username,
                                                                    password=reg_password, sex=reg_sex, date=reg_birth,
                                                                    hobby=reg_hobby, email=reg_email)
                                        return HttpResponse("注册成功")

                                    else:
                                        error5 = {'error': "用户名已存在！"}
                                        return render(request, "register.html", error5)

                                else:
                                    error4 = {'error': '两次输入密码不一致！'}
                                    return render(request, 'register.html', error4)
                            else:
                                error3 = {"error": '密码由4-20位字母或数字组成！'}
                                return render(request, 'register.html', error3)
                    else:
                        error2 = {"error": '请输入4-20位密码！'}
                        return render(request, 'register.html', error2)
                else:
                    error15 = {'error': "用户名由4-20位字母或数字组成！"}
        else:
            error1 = {"error": "请输入4-20位用户名！"}
            return render(request, 'register.html', error1)


# Create your views here.

def refloat(request):
    import random
    if request.method == 'POST':
        print(request.POST)
        bottle0 = request.POST.get('refloat')
        # sea = request.POST.get('sea')
        # bag = request.POST.get('bag')
        print(bottle0)

        if bottle0:
            bottle = drifter_ocean.objects.filter(state=0)
            if bottle.exists():
                bottle_list = list((bottle).values_list('id', flat=True))
                r = random.choice(bottle_list)

                random_bottle = drifter_ocean.objects.get(id=r)

                bottle_content = random_bottle.content
                bottle_owner = random_bottle.owner
                bottle_all = str(bottle_owner) + ':       ' + str(bottle_content) + "瓶子已进入您的包包，请在您的包包中查看"

                drifter_ocean.objects.filter(id=r).update(state=1)
                drifter_ocean.objects.filter(id=r).update(finder="xzxgg")

                return render(request, 'refloat.html', {'res': bottle_all})
            elif not bottle.exists():
                # r = 0
                return render(request, 'refloat.html', {'res': 'no bottle refloatable ! '})
            # else:
            #     return render(request, 'refloat.html', {'res': '请先处理您捞到的瓶子! '})

        # elif sea:
        #         if  r != 0 :
        #             drifter_ocean.objects.filter(id=r).update(state=0)
        #             r = 0
        #             return render(request, 'refloat.html', {'res1': '瓶子重返了大海'})
        #         elif r == 0 :
        #             return render(request, 'refloat.html', {'res1': '请先打捞一个瓶子'})

        # elif bag:
        #         if r != 0:
        #             bag.objects.create(owner=drifter_ocean.objects.get(id=r).owner, content=drifter_ocean.objects.get(id=r).content)
        #             r = 0
        #             return render(request, 'refloat.html', {'res2':'成功将瓶子放进包包'})
        #         elif r == 0:
        #             return render(request, 'refloat.html', {'res2':'请先打捞一个瓶子'})
        # else:
        #     print(bag)
        #     print(bottle0)
        #     print(sea)
        #     return HttpResponse("出错了！请重新试试！")


    else:
        return render(request, 'refloat.html')


def gateway(request):
    if request.method == 'GET':
        return render(request, 'gateway.html')




def baobao(request):
    if request.method == 'GET':

        bottle1 = list(drifter_ocean.objects.filter(owner='xzxgg'))
        print(bottle1)
        BOTTLE1 = []
        for i in range(len(bottle1)):
            o = str(bottle1[i].id)

            a = bottle1[i].owner

            b = bottle1[i].content

            c = bottle1[i].finder
            if not c:
                c = "None"
            else:
                pass
            d = bottle1[i].reply
            if not d:
                d = "None"
            else:
                pass
            BOTTLE1.append(str(o + '  ' + a + "  " + b + '  ' + c + '  ' + d))
        BOTTLE1_str = "\\`<br>".join(BOTTLE1)
        

        bottle2 = list(drifter_ocean.objects.filter(finder="xzxgg"))
        BOTTLE2 = []
        for t in range(len(bottle2)):
            o = str(bottle2[t].id)
            a = bottle2[t].owner
            b = bottle2[t].content
            c = bottle2[t].finder
            d = bottle2[t].reply
            BOTTLE2.append(str(o + '  ' + a + "  " + b + '  ' + c + '  ' + d))
        BOTTLE2_str = "\\<br>".join(BOTTLE2)

        # BOTTLE = BOTTLE1 + BOTTLE2
        # bottle = {'bottle': '             '.join(BOTTLE)}

        # bottle = {'bottle':list(bottle1) + list(bottle2)}
        # print(list(bottle1))
        # print(list(bottle2))

        return render(request, 'baobao.html', {"bottle2":BOTTLE2_str,"bottle1":BOTTLE1_str})

    if request.method == "POST":

        sea_id = request.POST.get("back to the sea")
        print(sea_id)
        reply_if = request.POST.get("reply")
        if sea_id:
            drifter_ocean.objects.filter(id=sea_id).update(finder=None)
            drifter_ocean.objects.filter(id=sea_id).update(state=0)
            return render(request,'baobao.html',{"success":"漂流瓶回到了大海"})
        elif reply_if:
            return render(request,'reply.html')

def reply(request):
    if request.method == "GET":
        return  render(request,'reply.html')
    elif request.method == "POST":
        reply_id = request.POST.get("id")
        reply_content = request.POST.get("content")
        reply_origin = drifter_ocean.objects.filter(id=reply_id)[0].reply


        print(reply_origin)

        new_content = str(reply_origin+reply_content)
        drifter_ocean.objects.filter(id=reply_id).update(reply=new_content)

        return render(request,'reply.html',{'success':'回复成功！'})

def cast(request):
    if request.method == "GET":
        return render(request,'cast.html')
    elif request.method == "POST":
        cast_owner = request.POST.get("username")
        cast_content = request.POST.get("content")
        cast = drifter_ocean.objects.create(owner=cast_owner,content=cast_content,state=0)
        cast.save()

        return render(request,"cast.html",{'success':"你的瓶子成功扔进了大海"})

def infor_change(request):
    if request.method =="GET":
        return render(request,"infor_change.html")
    elif request.method == "POST":
        nicheng = request.POST.get('nicheng')
        if nicheng:
            drifter_user.objects.filter(username='xzxgg').update(nicheng=nicheng)
        else:
            pass

        sex = request.POST.get('sex')
        if sex==0 or sex==1:
            drifter_user.objects.filter(username='xzxgg').update(sex=sex)
        else:
            pass

        hobby = request.POST.get('hobby')
        if hobby:
            drifter_user.objects.filter(username='xzxgg').update(hobby=hobby)
        else:
            pass

        email = request.POST.get('email')
        if email:
            drifter_user.objects.filter(username='xzxgg').update(email=email)
        else:
            pass

        return render(request,'infor_change.html',{'success':"您的信息已成功修改！"})

def user_center(request):
    if request.method == "GET":
        nicheng = drifter_user.objects.filter(username='xzxgg')[0].nicheng
        username = drifter_user.objects.filter(username='xzxgg')[0].username
        sex = str(drifter_user.objects.filter(username='xzxgg')[0].sex)
        date = str(drifter_user.objects.filter(username='xzxgg')[0].date)



        if not date:
            date = "None"
        else:
            pass
        hobby = drifter_user.objects.filter(username='xzxgg')[0].hobby
        if not hobby:
            hobby = "None"
        else:
            pass
        email = drifter_user.objects.filter(username='xzxgg')[0].email
        if not email:
            email = "None"
        else:
            pass
        return render(request,"user_center.html",{'user':nicheng+"\n"+username+"\n"+sex+"\n"+date+"\n"+hobby+"\n"+email})
    if request.method == "POST":
        pass


