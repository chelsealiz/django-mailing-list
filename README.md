# django-mailing-list*
*work in progress

#Information
This is a Django plugin that allows users to add members of a staff module to a Google Mailing list. You can create mailing lists and staff members, associate them with each other, and create corresponding information in Google from the Django admin site.

#Features
- Sortable by first and last name in admin
- Optional position, department, phone number, and photo
- Create Mailing Lists in Google Groups* as well as adding people to the lists**

*Only works if you have an Enterprise Google Account

** Work in Progress

#Future Features
- Better photo uploading options
- HTML templates for use in your staff pages

#Use
Clone and add the Plugin to your project

Make sure google_mailing_list is in installed apps

Go to the Google Developer console and create a new project, allowing the Admin SDK API

  Make sure you choose Web application!
  
Add the Client secret and Client ID to the corresponding sections in the utils.py file

Create and run migrations
