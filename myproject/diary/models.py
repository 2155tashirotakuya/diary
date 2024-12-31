# UUIDを使う　UUIDとは他の識別子とはかぶらない識別子を生成する
from django.db import models
# delete機能追加時に追加
from pathlib import Path
import uuid

#日記のページクラス
class Page(models.Model):
    #変数にフィールドを代入する
    # フィールドによって、どのような種類のデータか定める
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    # プライマリーキーは、日記のページを一意に識別するためのカラム
    # default=uuid.uuid4：
    # editable=False:変更不可
    title = models.CharField(max_length=100, verbose_name="タイトル")
    # 文字列の長さ:100
    #本文
    body = models.TextField(max_length=2000, verbose_name="本文")
    # 作成日時
    page_date = models.DateField(verbose_name="日付")

    # 画像の保存先サブフォルダ_画像なしでも日記作成可能にする
    picture = models.ImageField(
        upload_to="diary/picture/",blank=True,null=True,verbose_name="写真")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    # auto_now_add=True:データが初めて作成された日時を保存
    # 更新日時
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    # auto_now=True:データが保存・更新されるたびに日時を保存

    def __str__(self):
        return self.title

    # オーバーライドする
    #　オーバーライド：基底クラスのメソッドを上書きすること
    def delete(self, *args, **kwargs):
        picture = self.picture
        super().delete(*args, **kwargs)
        if picture:
            Path(picture.path).unlink(missing_ok = True)



