from django.db import models


class UserProfile(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    username = models.CharField(max_length=255, default='@Unknown')
    first_name = models.CharField(max_length=255, default='Unknown')
    last_name = models.CharField(max_length=255, default='Unknown')
    wallet_address = models.CharField(max_length=255, blank=True, null=True)
    xp = models.IntegerField(default=0)
    coins = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    class Boosts(models.IntegerChoices):
        lighting = 0
        fertilizer = 0
        sour = 0
    boosts_lvls = models.IntegerField(choices=Boosts)

    def str(self):
        return f'{self.first_name} {self.last_name}'


class Referral(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referred_by')
    xp = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} referred {self.referred_user.username}'