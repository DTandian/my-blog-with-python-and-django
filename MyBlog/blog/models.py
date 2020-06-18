from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class PostCategory(models.Model):
    name = models.CharField(max_length=50,
                            blank=False)

    #  instance function which allows to slug category name
    #  ie switch from capital letter to minuscule letter in category name
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, )
    category = models.ForeignKey("PostCategory",
                                 # null attribute related to BDD
                                 null=True,
                                 blank=True,
                                 on_delete=models.DO_NOTHING)
    published = models.BooleanField(default=False)
    text = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    STATUS_VISIBLE = 'visible'
    STATUS_HIDDEN = 'hidden'
    STATUS_MODERATE = 'moderated'

    CHOICES_STATUS = [
        (STATUS_VISIBLE, 'visible'),
        (STATUS_HIDDEN, 'hidden'),
        (STATUS_MODERATE, 'moderated'),
    ]

    post = models.ForeignKey('Post',
                             on_delete=models.CASCADE,
                             related_name='comments')
    #  related_name='comments' allows to access comments linked with post by foreign key
    author_name = models.CharField(max_length=100)
    text = models.TextField()
    status = models.CharField(max_length=20,
                              default=STATUS_VISIBLE,
                              choices=CHOICES_STATUS)
    moderation_text = models.CharField(max_length=200,
                                       blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} - {} status={}'.format(self.author_name, self.text[:20], self.status)
