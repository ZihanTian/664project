from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings
from multiselectfield import MultiSelectField

POSITION_CHOICE = (
    ('North Campus', ('North Campus')),
    ('Central Campus', ('Central Campus')),
    ('Other Area',('Other Area')),
)
class Ad(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.TextField()
    position = MultiSelectField(choices=POSITION_CHOICE,max_choices=1,null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='comments_owned')
    # Picture #add one more picture and content_type
    picture1 = models.BinaryField(null=True, editable=True)
    picture2 = models.BinaryField(null=True, editable=True)
    content_type1 = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    content_type2 = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    # Shows up in the admin list
    def __str__(self):
        return self.title
class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'
