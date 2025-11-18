from django.db import models
import uuid

choices_place = {
   '受付': '受付',
   '直前待機場所': '直前待機場所',
   'ステージ・客席（設備）': 'ステージ・客席（設備）',
   'ステージ・客席（演奏）': 'ステージ・客席（演奏）',
   'スタッフエリア': 'スタッフエリア',
   '会場周辺': '会場周辺',
   '全域': '全域',
   'その他': 'その他',
}

pub_pri_permissions = [
   ("public", "全体に表示"),
   ("only_staff", "スタッフのみに表示"),
   ("private", "非表示"),
]

class Report(models.Model):
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
   created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
   repo_cont = models.TextField(max_length=2000, verbose_name='報告内容')
   repo_plac = models.CharField(max_length=15, choices=choices_place, verbose_name='発生場所', blank=True, null=True)
   repo_pter = models.CharField(max_length=15, verbose_name='報告者')
   repo_publicity = models.CharField(max_length=15, choices=pub_pri_permissions, verbose_name='表示設定', default='only_staff')
   repo_tweet = models.BooleanField(verbose_name='つぶやきモード', default=False)

   def __str__(self):
      return self.repo_cont
   
   class Meta:
      permissions = [
         ("make_report", "報告権限"),
         ("view_reports", "報告閲覧権限"),
      ]