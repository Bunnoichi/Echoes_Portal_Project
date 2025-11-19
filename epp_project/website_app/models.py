from django.db import models
import uuid


class Team(models.Model):
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
   team_name = models.CharField(max_length=100, verbose_name="団体名")
   team_name_kana = models.CharField(verbose_name='団体名（カナ）')
   team_belong = models.CharField(max_length=100, verbose_name="団体の所属", null=True, blank=True)
   team_desc = models.CharField(max_length=100, verbose_name="団体説明", null=True, blank=True)
   team_ninzu = models.IntegerField(verbose_name='参加人数', null=True, blank=True)

   checkin_pretime_1 = models.DateTimeField(verbose_name="受付定刻")
   checkin_koedashi = models.DateTimeField(verbose_name="声出し開始定刻",null=True, blank=True)
   duration_koed = models.IntegerField(verbose_name='声出し分数', default=17, null=True, blank=True)
   checkin_pretime_2 = models.DateTimeField(verbose_name="控室到着定刻", null=True, blank=True)
   duration_reha = models.IntegerField(verbose_name='リハ分数', default=5, null=True, blank=True)
   onstage_time = models.DateTimeField(verbose_name="出演定刻")
   duration_onst = models.IntegerField(verbose_name="出演分数", default=10, null=True, blank=True)

   checkin_postime_1 = models.DateTimeField(verbose_name="受付打刻",null=True, blank=True)
   checkin_postime_2 = models.DateTimeField(verbose_name="控室到着打刻",null=True, blank=True)
   onstage_time_acc = models.DateTimeField(verbose_name="開演打刻", null = True, blank=True)
   onstage_tien_acc = models.DateTimeField(verbose_name="終演打刻", null = True, blank=True)

   team_rep = models.CharField(verbose_name="代表者名（カナ）",null=True, blank=True)
   team_rep_mail = models.CharField(verbose_name="代表者メールアドレス",null=True, blank=True)
   team_rep_tel = models.CharField(verbose_name="代表者電話番号",null=True, blank=True)

   file_artpic = models.ImageField(upload_to='website_app/art_pictures/', null=True, blank=True, verbose_name='アーティスト写真')
   file_form = models.FileField(upload_to='website_app/form_files/',null=True,  blank=True, verbose_name='応募ファイル')
   file_stage = models.FileField(upload_to='website_app/stage_files/',null=True, blank=True, verbose_name='ステージファイル')

   team_equip = models.TextField(verbose_name='使用機材等',max_length=1000, null=True, blank=True)
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