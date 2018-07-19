from django.db import models

# Create your models here.

class JobMsg(models.Model):
    job_time = models.CharField(max_length=100, blank=True, null=True)
    job_name = models.CharField(max_length=100, blank=True, null=True)
    job_money = models.CharField(max_length=100, blank=True, null=True)
    job_meanmoney = models.CharField(db_column='job_meanMoney', max_length=100, blank=True, null=True)  # Field namemade lowercase.
    job_address = models.CharField(max_length=100, blank=True, null=True)
    job_jy = models.CharField(max_length=100, blank=True, null=True)
    job_xl = models.CharField(max_length=100, blank=True, null=True)
    job_hrname = models.CharField(db_column='job_hrName', max_length=100, blank=True, null=True)  # Field name madelowercase.
    job_hrleader = models.CharField(max_length=100, blank=True, null=True)
    job_zwtext = models.TextField(blank=True, null=True)
    job_tdtext = models.TextField(blank=True, null=True)
    job_gstext = models.TextField(blank=True, null=True)
    job_comname = models.CharField(db_column='job_comName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    company_username = models.CharField(db_column='company_userName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    company_money = models.CharField(max_length=100, blank=True, null=True)
    company_time = models.CharField(max_length=100, blank=True, null=True)
    company_type = models.CharField(max_length=100, blank=True, null=True)
    company_status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_msg'
