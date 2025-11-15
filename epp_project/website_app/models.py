from django.db import models
import uuid


class Team(models.Model):
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
   team_name = models.CharField(max_length=100, verbose_name="団体名")
   team_name_kana = models.CharField(verbose_name='団体名（カナ）')
   team_desc = models.CharField(max_length=100, verbose_name="団体の所属", null=True, blank=True)
   team_ninzu = models.IntegerField(verbose_name='参加人数', null=True, blank=True)
   team_equip = models.TextField(verbose_name='使用機材等',max_length=1000, null=True, blank=True)
   team_rep = models.CharField(verbose_name="代表者名（カナ）",null=True, blank=True)
   team_rep_mail = models.CharField(verbose_name="代表者メールアドレス",null=True, blank=True)
   team_rep_tel = models.CharField(verbose_name="代表者電話番号",null=True, blank=True)
   checkin_pretime_1 = models.DateTimeField(verbose_name="受付日時の予定")
   checkin_postime_1 = models.DateTimeField(verbose_name="実際の受付日時",null=True, blank=True)
   checkin_pretime_2 = models.DateTimeField(verbose_name="直前待機日時の予定", null=True, blank=True)
   checkin_postime_2 = models.DateTimeField(verbose_name="実際の直前待機日時",null=True, blank=True)
   duration_reha = models.IntegerField(verbose_name='リハ分数', default=5, null=True, blank=True)
   duration_onst = models.IntegerField(verbose_name='出演分数', default=10, null=True, blank=True)
   onstage_time = models.DateTimeField(verbose_name="出演予定時刻")
   onstage_time_acc = models.DateTimeField(verbose_name="実際の出演時刻", null = True, blank=True)
   file_form = models.FileField(upload_to='website_app/form_files/',null=True,  blank=True, verbose_name='応募ファイル')
   file_stage = models.FileField(upload_to='website_app/stage_files/',null=True, blank=True, verbose_name='ステージファイル')
   note = models.TextField(verbose_name='備考',max_length=1000, null=True, blank=True)
   created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
   updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

   def __str__(self):
      return self.team_name
   
   class Meta:
      permissions = [
         ("initial_registration", "団体初期登録権限"),
         ("checkin", "打刻権限"),
         ("view_detail", "団体詳細確認権限"),
         ("update_information", "団体情報更新権限"),
      ]
   
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