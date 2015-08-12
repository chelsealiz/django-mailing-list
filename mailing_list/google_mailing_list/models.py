from django.db import models
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField
from django.http import HttpRequest
import urllib
import urllib2
import os
import logging
import httplib2
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
# from oauth2client.django_orm import Storage
from oauth2client.file import Storage
from django.conf import settings
from django.contrib.auth.models import User
import random
from django.shortcuts import redirect
from googleapiclient.discovery import build


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()

class SendData(models.Model):
    name = models.CharField(max_length=200, blank=False)
    email = models.CharField(max_length=200, blank=False)
    store_id=models.PositiveSmallIntegerField(blank=True)

    def auth(self, scope_url):
        scope = scope_url
        if(self.store_id==False):
            self.store_id = random.seed()
        session=self.store_id
        client_id=''
        client_secret=''
        flow = OAuth2WebServerFlow(client_id=client_id,
                                   client_secret=client_secret,
                           scope=scope,
                           redirect_uri='http://localhost:8000/admin/google_mailing_list/mailinglist/add/')
        storage = Storage("storage.dat")
        credential = storage.get()
        if credential is None or credential.invalid == True:
            flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                           session)
            auth_uri = flow.step1_get_authorize_url()
            redirect(auth_uri)
            storage = Storage("storage.dat")
            credential = flow.step2_exchange(credential)
            storage.put(credential)
        return credential

    def make_mailing_list(self):
        name = self.name
        email = self.email
        # final = "https://www.googleapis.com/admin/directory/v1/groups"
        scope = "https://www.googleapis.com/auth/admin.directory.group"
        post_data = {
            "email": email,
            "name": name
        }
        credential = self.auth(scope)
        http_auth = credential.authorize(httplib2.Http())
        service = build("admin", "directory_v1", http=http_auth)
        create = service.groups().insert(body=post_data)
        # create = create.execute()
        create = HttpResponseRedirect(create.execute())
        return create


class MailingList(models.Model):
    name = models.CharField(max_length=200, blank=False)
    email = models.CharField(max_length=200, blank=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        sending = SendData()
        sending.name=self.name
        sending.email = self.email
        sending.make_mailing_list()
        return super(MailingList, self).save(*args, **kwargs)


class Staff(models.Model):
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    email = models.CharField(max_length=200, blank=False, default='')
    position = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    picture = models.ImageField(blank=True)
    mailing_lists = models.ManyToManyField(MailingList)