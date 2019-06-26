from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from PIL import Image
# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=20)
    def __str__(self):
        return self.category
class newManuscript(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    fileImg = models.FileField(default='Cover.jpg', upload_to='Manuscript_Files')
    file = models.FileField(default='default.jpg', upload_to='Manuscript_Files')
    text = models.TextField(default='No text')
    ispaperoriginal = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    undercosideration = models.BooleanField(default=False)
    containcopyright = models.BooleanField(default=False)
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "{} - Posted at {}".format(self.title,self.post_date.strftime("%b %d %Y %H:%M:%S"))
    def save(self):
        super().save()
class Comment(models.Model):
    name = models.CharField(max_length=50)
    body = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    post = models.ForeignKey(newManuscript,on_delete=models.CASCADE,related_name='comments')
    def __str__(self):
        return 'علق {} على {}'.format(self.name,self.post)
    class Meta:
        ordering = ('comment_date',)
class Profile(models.Model):
    image = models.ImageField(default='default.jpg',upload_to='profiles')
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return "{}".format(self.user.username)
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)
        if img.width>300 or img.height > 300:
            img.thumbnail((300,300))
            img.save(self.image.path)
def creat_profile(sender,**kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
post_save.connect(creat_profile,sender=User)
class PDF_Files(models.Model):
    file = models.FileField(default='default.jpg',upload_to='Manuscript_Files')
    manuscript = models.ForeignKey(newManuscript,on_delete=models.CASCADE)
    def __str__(self):
        return "{}".format(self.manuscript)
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
def creat_pdf(sender,**kwargs):
    if kwargs['created']:
        PDF_Files.objects.create(manuscript=kwargs['instance'])
post_save.connect(creat_pdf,sender=newManuscript)