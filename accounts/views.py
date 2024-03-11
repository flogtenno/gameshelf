from django.shortcuts import render,redirect
from django.contrib import messages #メッセージの送信完了をおしらせ
from .models import CustomUser
from .forms import CustomUserCreationForm,LoginForm
from django.contrib.auth import authenticate, login, logout as auth_logout

# ユーザーページ～～～～～～～～～～～～～～～～～～～
def userpage(request):
    if request.user.is_authenticated: # ユーザーが認証されている場合の処理
        print(f"***ユーザーページアクセス*****User：{request.user}******")
        params={
        "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
        }
        return render(request, 'accounts/userpage.html', params)
    else:                             # ユーザーが未認証の場合の処理
        print("*****未ログイン*****")
        messages.warning(request, "ログインして下さい")
        return redirect(to="/") #リダイレクトで飛ばす際には「/」がないとトップからの絶対パスとして認識されてしまう

# ユーザー情報変更～～～～～～～～～～～～～～～～～～～
def edituser(request, user_id):
    pass

# 新規ユーザー登録～～～～～～～～～～～～～～～～～～～
def createuser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("***CreateOK***")
            messages.warning(request, "登録成功")
            return redirect(to='/')  # 登録成功時のリダイレクト先
        else:
            print("***CreateNG***")
            messages.warning(request, "登録失敗")
            return redirect(to='/accounts/createuser')  # 登録失敗時のリダイレクト先
    else:
        form = CustomUserCreationForm()
        params={
            "createform" : form
        }
        return render(request, 'accounts/createuser.html', params)

# ログインページ～～～～～～～～～～～～～～～～～～～

def userlogin(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password) #ユーザーを認証する関数
            print(f"****user:{user}")
            if user is not None:
                print("***LoginOK***")
                login(request, user)
                messages.warning(request, "ログイン成功")
                return redirect('/accounts/userpage/')  # ログイン成功時のリダイレクト先
        else:
            print("***LoginNG***")
            messages.warning(request, "ログイン失敗")
            return redirect(to='/accounts/login')  # 登録失敗時のリダイレクト先
    else:
        params={
            "loginform" : LoginForm()
        }
    return render(request, 'accounts/login.html', params)

# ログアウト～～～～～～～～～～～～～～～～～～～～～～～～～
def userlogout(request):
    auth_logout(request) #ログアウト処理
    messages.info(request, "ログアウトしました")
    return redirect('/')