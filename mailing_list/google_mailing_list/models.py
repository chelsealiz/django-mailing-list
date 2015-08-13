import httplib2

from django.db import models
from googleapiclient.discovery import build
from django.contrib.auth.models import User
from oauth2client.django_orm import CredentialsField

from google_mailing_list import utils


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()


class MailingList(models.Model):
    name = models.CharField(max_length=200, blank=False)
    email = models.CharField(max_length=200, blank=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.make_mailing_list()
        return super(MailingList, self).save(*args, **kwargs)

    def make_mailing_list(self):
        scope = 'https://www.googleapis.com/auth/admin.directory.group'
        post_data = {
            'email': self.email,
            'name': self.name
        }
        credentials = utils.auth(scope)
        http_auth = credentials.authorize(httplib2.Http())
        service = build('admin', 'directory_v1', http=http_auth)
        create = service.groups().insert(body=post_data)
        return create.exexute()


class Staff(models.Model):
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    email = models.CharField(max_length=200, blank=False, default='')
    position = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    picture = models.ImageField(blank=True)
    mailing_lists = models.ManyToManyField(MailingList)
