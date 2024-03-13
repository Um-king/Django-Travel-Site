from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# models.py
class Post(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=1000, default='General', blank=True)
    contents = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True, null=True)
    fromDate = models.DateField(default=timezone.now, blank=True)  # 기본값으로 현재 날짜 설정
    toDate = models.DateField(default=timezone.now, blank=True)
    tags = models.ManyToManyField("Tag", blank=True)
    subContent = models.TextField(blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0, blank=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    

class Itinerary(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='itineraries')
    date = models.DateField(default=timezone.now)  # 현재 날짜를 기본값으로 설정
    detailContent = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.post.title} - {self.date}"

class Mission(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='missions')
    mission = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post.title} - {self.mission} - {'Completed' if self.is_completed else 'Not Completed'}"


class Comment(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)


    def __str__(self):
        return self.message
    

# 구독자와 채널 소유자 user간의 중계 테이블 생성(user와 user 연결하는 중간 테이블)
class Subscription(models.Model): # 중계테이블 생성(user와 user를 연결하는 중간테이블)
    # subscriber = models.ForeignKey( # 구독자 user 정보
    #     User, on_delete=models.CASCADE, related_name="subscriptions"
    # )
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscriptions', on_delete=models.CASCADE)
    # channel = models.ForeignKey( # 채널 소유자 user 정보
    #     User, on_delete=models.CASCADE, related_name="subscribers"
    # ) 
    channel = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscribers', on_delete=models.CASCADE)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("subscriber", "channel")  # 구독자와 채널은 유일해야 함

    def __str__(self):
        return f"{self.subscriber.username}이 {self.channel.username}를 구독하였습니다."
    

class Area(models.Model):
    name = models.CharField(max_length=100)




    
# 즐겨찾기 모델
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')