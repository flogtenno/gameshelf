from django.shortcuts import render,redirect
from django.contrib import messages #メッセージの送信完了をおしらせ
from .models import CustomUser
from .forms import CustomUserCreationForm,LoginForm,CustomUserEditForm
from django.contrib.auth import authenticate, login, logout as auth_logout, update_session_auth_hash
from django.core.paginator import Paginator
from diary.models import Diary,DiaryComment
from game.models import Game,GameComment

# ユーザーページ～～～～～～～～～～～～～～～～～～～
def userpage(request):
    if request.user.is_authenticated: # ユーザーが認証されている場合の処理
        print(f"***ユーザーページアクセス*****User：{request.user}******")
        # ユーザー作成記事の格納
        user_diary_all = Diary.objects.filter(diary_user=request.user) #ユーザー作成記事の情報を送付
        paginator = Paginator(user_diary_all, 3) #3つで区切る
        page_number = request.GET.get("page") #指定のページ数を格納
        user_diary = paginator.get_page(page_number) #指定ページの記事を格納
        # EXPの管理
        user_diary_count = Diary.objects.filter(diary_user_id=request.user.id).count() #ユーザーの記事執筆数
        print(f"***user_diary_count:{user_diary_count}***")
        user_diary_comment_count = DiaryComment.objects.filter(diary_comment_user_id=request.user.id).count() #ユーザーの日記へのコメント数
        print(f"***user_diary_comment_count:{user_diary_comment_count}***")
        user_game_comment_count = GameComment.objects.filter(game_comment_user_id=request.user.id).count() #ユーザーのゲームへのコメント数
        print(f"***user_game_comment_count:{user_game_comment_count}***")
        latest_exp=(user_diary_count)*100 + (user_diary_comment_count + user_game_comment_count)*10 #記事執筆は10倍
        print(f"***latest_exp:{latest_exp}***")
        request.user.exp = latest_exp #経験値情報をユーザーテーブルに記録
        # ランクの管理
        latest_rank_data = calculate_rank(latest_exp) #return {'rank': rank, 'remaining_exp': remaining_exp}
        latest_rank = latest_rank_data['rank']  # 'rank' キーを使ってランクを取得
        remaining_exp = latest_rank_data['remaining_exp']  # 'remaining_exp' キーを使って残り経験値を取得
        print(f"***latest_rank:{latest_rank}***")
        print(f"***remaining_exp:{remaining_exp}***")
        request.user.rank = latest_rank #ランク情報をユーザーテーブルに記録
        request.user.save() # EXP&Rank情報をセーブ

        params={
        "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
        "userdiary"     :   user_diary,
        "remaining_exp" :   remaining_exp,
        }
        return render(request, 'accounts/userpage.html', params)
    else:                             # ユーザーが未認証の場合の処理
        print("*****未ログイン*****")
        messages.warning(request, "ログインして下さい")
        return redirect(to="/") #リダイレクトで飛ばす際には「/」がないとトップからの絶対パスとして認識されてしまう

# ユーザー情報変更～～～～～～～～～～～～～～～～～～～
def edituser(request):
    userprofile = CustomUser.objects.get(id=request.user.id)
    params={
        "login_user"    : request.user, #現在のログインユーザー情報（request.user）
        "editform"      : CustomUserEditForm(instance=userprofile),
    }
    print(f"***ユーザー情報編集*****User：{request.user}******")
    return render(request, 'accounts/edituser.html', params)

def save_edituser(request):
    userprofile = CustomUser.objects.get(id=request.user.id)
    edit_profile = CustomUserEditForm(request.POST, request.FILES, instance=userprofile)
    if edit_profile.is_valid():
        user = edit_profile.save(commit=False)
        password = edit_profile.cleaned_data.get("password")
        confirm_password = edit_profile.cleaned_data.get("confirm_password")
        if password != confirm_password: # パスワードが一致しない場合はリダイレクトして処理終了
            messages.warning(request, "パスワードが一致しませんでした。")
            return redirect(to="userpage/")
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)# パスワードを変更した後、セッションの認証ハッシュを更新する？
        user.save()
        messages.success(request, "ユーザー情報を編集しました")
        return redirect(to="userpage/")
    else:
        messages.warning(request, "ユーザー情報編集失敗")
        return redirect(to="userpage/")

# 新規ユーザー登録～～～～～～～～～～～～～～～～～～～
def createuser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("***Create_OK***")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("***Login_OK***")
                messages.success(request, "登録成功")
                return redirect('/')  # 登録成功時のリダイレクト先
            else:
                print("***Login_NG***")
        else:
            print("***Create_NG***")
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

# ランク計算用関数～～～～～～～～～～～～～～～～～～～～～～～～～～～～
def calculate_rank(exp):
    base_exp = 100 # ランクアップに必要な経験値の基準値
    rank = 0 #ランク初期値
    exp_increase_rate = 1.2 #ランクアップに必要な経験値の増加率
    required_exp = 0
    # 経験値がランクアップに必要な経験値を超えるまでランクを上げる
    while exp >= required_exp:
        rank += 1
        required_exp = base_exp * (exp_increase_rate ** rank)
        remaining_exp = int(required_exp - exp)
        # print(f"rank:{rank} required_exp:{required_exp}")
    return {'rank': rank, 'remaining_exp': remaining_exp}
