import datetime
from django.db import models
from django.utils import timezone
# import for security fix:
# from passlib.hash import bcrypt

class Users(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def set_password(self, pss):
        # Does not use a cryptographic and safe hash function,
        # thus succumbing to a cryptographic failure.
        # SHOULD BE:
        # self.password = bcrypt.hash(pss)
        # INSTEAD OF
        self.password = hash(pss)
        # end

    def check_password(self, pss):
        # Previous cryptographic failure continues:
        # SHULD BE: 
        # if bcrypt.verify(pss, self.password):
        # INSTEAD OF
        print(self.password)
        print(hash(pss))
        if int(self.password) == hash(pss):
        # end
            return True
        return False

    def __str__(self) -> str:
        return self.username
    
class Question(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self) -> str:
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.choice_text
