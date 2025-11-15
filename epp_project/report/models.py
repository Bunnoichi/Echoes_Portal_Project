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

class Report(models.Model):
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
   created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
   repo_cont = models.TextField(max_length=2000, verbose_name='報告内容')
   repo_plac = models.CharField(max_length=15, choices=choices_place, verbose_name='発生場所')
   repo_pter = models.CharField(max_length=15, verbose_name='報告者')

   def __str__(self):
      return choices_place[self.repo_plac]
   
   class Meta:
    permissions = [
        ("make_report", "報告権限"),
        ("view_reports", "報告閲覧権限"),
    ]

