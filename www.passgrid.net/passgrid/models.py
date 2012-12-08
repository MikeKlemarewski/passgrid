from django.db import models


class Token(models.Model):
    user = models.ForeignKey('auth.User')
    token = models.CharField(max_length=255)



#
# [
# [0,4210752,8421504,12632256],
# [0,4194304,8388608,12582912],
# [0,16384,32768,49152],
# [0,64,128,192]]