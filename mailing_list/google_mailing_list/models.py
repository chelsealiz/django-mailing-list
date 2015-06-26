from django.db import models
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField
from django.http import HttpRequest
import os
import logging
import httplib2
from apiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
from django.conf import settings
from django.contrib.auth.models import User

class FlowModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  flow = FlowField()

class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()

class SendData(models.Model):
    name = models.CharField(max_length=200, blank=False)
    email = models.CharField(max_length=200, blank=False)

    def send_data(self, request):
        name = self.name
        email = self.email
        user = request.user
        final = "https://www.googleapis.com/admin/directory/v1/groups"
        scope = "https://www.googleapis.com/auth/admin.directory.group"
        
        flow = OAuth2WebServerFlow(client_id=client_id,
                           client_secret=client_secret,
                           scope=scope,
                           redirect_uri='localhost')
        storage = Storage(CredentialsModel, 'id', user, 'credential')
        credential = storage.get()
        post_data = {
            "email": email,
            "name": name
        }
        #
        # if credential is None or credential.invalid == True:
        #     flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
        #                                            request.user)
        #     authorize_url = flow.step1_get_authorize_url()
        #     http = HttpResponseRedirect(authorize_url)
        #     credential = flow.step2_exchange(http)
        #     storage = Storage(CredentialsModel, 'id', request.user, 'credential')
        #     storage.put(credential)
        #     http2 = httplib2.Http()
        #     http2 = credential.authorize(http2.request(final, "POST", body=post_data))
        #     return http2
        # else:
        #     credential = flow.step2_exchange(credential)
        #     storage = Storage(CredentialsModel, 'id', request.user, 'credential')
        #     storage.put(credential)
        #     http2 = httplib2.Http()
        #     http2 = credential.authorize(http2.request(final, "POST", body=post_data))
        #     return http2
        if credential is None or credential.invalid == True:
            flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                           user)
            authorize_url = flow.step1_get_authorize_url()
            authorize_url = HttpResponseRedirect(authorize_url)
            credential = flow.step2_exchange(authorize_url)
            storage = Storage(CredentialsModel, 'id', user, 'credential')
            storage.put(credential)
        credential = flow.step2_exchange(credential)
        result = credential.authorize(request.POST(final, params=post_data))
        return result


class MailingList(models.Model):
    name = models.CharField(max_length=200, blank=False)
    email = models.CharField(max_length=200, blank=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        sending = SendData()
        sending.name=self.name
        sending.email = self.email
        sending.send_data(HttpRequest)
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