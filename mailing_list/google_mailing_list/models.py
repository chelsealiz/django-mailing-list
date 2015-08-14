import httplib2

from django.db import models
from googleapiclient.discovery import build
from django.contrib.auth.models import User
from oauth2client.django_orm import CredentialsField

import utils


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()


class MailingList(models.Model):
    name = models.CharField(max_length=200, blank=False)
    email = models.CharField(max_length=200, blank=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            pass
            self._make_mailing_list()
        else:
            self.update()
        return super(MailingList, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        scope = '/admin/directory/v1/groups/{}'.format(self.email)
        request = utils.make_request('DELETE', 'www.googleapis.com', scope)
        return super(MailingList, self).delete(*args, **kwargs)

    def update(self):
        scope = '/admin/directory/v1/groups/{}'.format(self.email)
        request = utils.make_request('PUT', 'www.googleapis.com', scope)
        return request

    def _make_mailing_list(self):
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

    class Meta:
        ordering = ('name',)
        verbose_name_plural = u'Edit COS Mailing lists'
        verbose_name = u'Mailing Lists'


class Staff(models.Model):
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    email = models.CharField(max_length=200, blank=False, default='')
    position = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    picture = models.ImageField(blank=True)
    mailing_lists = models.ManyToManyField(MailingList, blank=True)

    def add_to_group(self, email):
        mail = email
        scope = 'https://www.googleapis.com/auth/admin.directory.members'
        post_data = {
            'email': self.email,
            'role': 'MEMBER'
        }
        credentials = utils.auth(scope)
        http_auth = credentials.authorize(httplib2.Http())
        service = build('admin', 'directory_v1', http=http_auth)
        create = service.members().insert(groupKey=mail, body=post_data)
        return create.execute()

    def remove_from_group(self, email):
        mail = email
        scope = 'https://www.googleapis.com/auth/admin.directory.members'
        credentials = utils.auth(scope)
        http_auth = credentials.authorize(httplib2.Http())
        service = build('admin', 'directory_v1', http=http_auth)
        create = service.members().delete(groupKey=mail, memberKey=self.email)
        return create.execute()

    def delete(self, using=None):
        for group in self.mailing_lists.all():
            self.remove_from_group(group)
        return super(Staff, self).delete()


    def save(self, *args, **kwargs):
        super(Staff, self).save(*args, **kwargs)
        all_emails = self.mailing_lists.all()
        for email in all_emails:
            self.add_to_group(email)
        return None