from django.shortcuts import render,redirect
from django.contrib import messages #メッセージの送信完了をおしらせ
from .models import CustomUser
from .forms import CustomUserCreationForm

# Create your views here.
def userpage(request):
    if request.user.is_authenticated: # ユーザーが認証されている場合の処理
        print(f"***ユーザーページアクセス*****UserID：{request.user.id}******")
        params={
        "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
        }
        return render(request, 'accounts/userpage.html', params)
    else:                             # ユーザーが未認証の場合の処理
        print("*****未ログイン*****")
        messages.warning(request, "ログインして下さい")
        return redirect(to="/") #リダイレクトで飛ばす際には「/」がないとトップからの絶対パスとして認識されてしまう

def edituser(request, user_id):
    pass

def createuser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')  # 登録成功時のリダイレクト先
    else:
        form = CustomUserCreationForm()
        return render(request, 'accounts/createuser.html', {'form': form})