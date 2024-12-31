from django.shortcuts import render, redirect, get_object_or_404
# ログイン必須にするMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import PageForm
from .models import Page
from datetime import datetime
from zoneinfo import ZoneInfo

# LoginRequiredMixinは、一番前に書いて継承させる必要がある
class IndexView(LoginRequiredMixin,View):
    def get(self, request):
        datetime_now = datetime.now(
            ZoneInfo("Asia/Tokyo")
        ).strftime("%Y年%m月%d日 %H:%M:%S")
        return render(
            request, "diary/index.html", {"datetime_now": datetime_now})
            #HTML側の変数(キー):Python側の変数(バリュー)
            #HTMLファイルの変数にpython側の変数を渡す

class PageCreateView(LoginRequiredMixin,View):
    def get(self, request):
        form = PageForm()
        return render(request, "diary/page_form.html", {"form": form})
        # PageFormで定義した入力項目をHTML側へ渡す

    def post(self, request):
        form = PageForm(request.POST, request.FILES)
        #　ユーザーが入力したデータを持つformクラスのオブジェクトができる
        #　入力項目のバリデーション(値のチェック)
        if form.is_valid():
            # Trueならデータベースに保存する
            form.save()
            # 保存されたらトップページに戻る
            # redirect(アプリ名:パスの名前)
            # diary/urls.py のurlpatternsの name="index"　に紐づいている
            return redirect("diary:index")
        #if文がfalseなら入力画面に戻る
        return render(request, "diary/page_form.html", {"form": form})

# プロジェクト内のオブジェクトを操作することでデータベースのデータを操作する技術をORM(オーアールマッパー)という

class PageListView(LoginRequiredMixin,View):
    def get(self, request):
        # .allメソッドじゃなくて.order_byメソッドを使うことで最新日付順に並べる
        # page_list = Page.objects.order_by("-page_date")
        # 改造ポイント
        # 作成日時順に並べる
        page_list = Page.objects.order_by("-created_at")

        return render(request, "diary/page_list.html", {"page_list": page_list})

class PageDetailView(LoginRequiredMixin,View):
    #id : パラメータとして送られてくる日記ページのID
    def get(self, request, id):
        # id にid を指定することでDBからIDが一致するPageのデータを取得
        # 一致するIDがなければ404ページへ
        page = get_object_or_404(Page, id=id)
        return render(request, "diary/page_detail.html", {"page":page})

# 編集機能用のクラス
class PageUpdateView(LoginRequiredMixin,View):
    def get(self, request, id):
        page = get_object_or_404(Page, id=id)
        form = PageForm(instance=page)
        return render(request, "diary/page_update.html", {"form": form})

    def post(self, request, id):
        page = get_object_or_404(Page, id=id)
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect("diary:page_detail", id=id)
        return render(request,"diary/page_update.html",{"form": form})

# 削除用のクラス
class PageDeleteView(LoginRequiredMixin,View):
    def get(self, request, id):
        page = get_object_or_404(Page, id=id)
        return render(request, "diary/page_confirm_delete.html",{"page":page})

    def post(self, request, id):
        page = get_object_or_404(Page, id=id)
        page.delete()
        return redirect('diary:page_list')

index = IndexView.as_view()
page_create = PageCreateView.as_view()
page_list = PageListView.as_view()
page_detail = PageDetailView.as_view()
page_update = PageUpdateView.as_view()
page_delete = PageDeleteView.as_view()

