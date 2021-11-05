from django.db import models

# Create your models here.




#lga model
class Lga(models.Model):
    uniqueid = models.IntegerField(max_length=50,primary_key=True)
    lga_id = models.IntegerField(max_length=50)
    lga_name = models.CharField(max_length=50)
    state_id = models.IntegerField(max_length=50)
    lga_description = models.CharField(max_length=50)
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.CharField(max_length=50)
    user_ip_address = models.CharField(max_length=50)





# ward model
class Ward(models.Model):
    uniqueid = models.IntegerField(max_length=50,primary_key=True)
    ward_id = models.IntegerField(max_length=50)
    ward_name = models.CharField(max_length=50)
    lga_id = models.IntegerField(max_length=50)
    ward_description = models.CharField(max_length=50)
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.CharField(max_length=50)
    user_ip_address = models.CharField(max_length=50)




# polling unit model
class PollingUnit(models.Model):
    uniqueid = models.IntegerField(max_length=50, primary_key=True)
    polling_unit_id = models.IntegerField(max_length=50)
    ward_id = models.IntegerField(max_length=50)
    lga_id = models.IntegerField(max_length=50)
    uniquewardid = models.IntegerField(max_length=50)
    polling_unit_number = models.CharField(max_length=50)
    polling_unit_name = models.CharField(max_length=50)
    polling_unit_description = models.CharField(max_length=50, null=True)
    lat = models.FloatField(max_length=50, null=True)
    long = models.FloatField(max_length=50, null=True)
    entered_by_user = models.CharField(max_length=50, null=True)
    date_entered = models.CharField(max_length=50, null=True)
    user_ip_address = models.CharField(max_length=50, null=True)


# party model
class Party(models.Model):
    id = models.IntegerField(max_length=50, primary_key=True)
    party_name = models.CharField(max_length=50)



#announced polling unit result model
class PollingUnitResult(models.Model):
    result_id = models.IntegerField(max_length=50, primary_key=True)
    polling_unit_uniqueid = models.IntegerField(max_length=50)
    party_abbreviation = models.CharField(max_length=50)
    party_score = models.IntegerField(max_length=50)
    entered_by_user = models.CharField(max_length=50, null=True)
    date_entered = models.CharField(max_length=50, null=True)
    user_ip_address = models.CharField(max_length=50, null=True)