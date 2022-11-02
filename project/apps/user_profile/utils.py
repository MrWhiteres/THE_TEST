from re import compile
import xml.etree.ElementTree as ET
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import UserProfile


def check_save_data_csv(file):
    for i in file:
        if not compile('[()}{]').search(i['username']) and len(i['username']) > 1:
            try:
                User.objects.create_user(username=i['username'], password=i['password'])
            except IntegrityError:
                pass


def check_save_data_xml(file):
    root = ET.parse(file).getroot()
    all_user = User.objects.all()
    full_data = dict()
    for user in root.iter('user'):
        if len(user.items()) == 0:
            continue
        if user[0].text and not compile('[()}{]').search(user[0].text):
            full_data['first_name'] = user[0].text
        if user[1].text and not compile('[()}{]').search(user[1].text):
            full_data['last_name'] = user[1].text
        if user[2].text and not compile('[()}{]').search(user[2].text):
            full_data['avatar_url'] = user[2].text
        worker(all_user, full_data)


def worker(list_user, full_data):
    for users in list_user:
        if compile('.').search(users.username):
            if len(full_data) == 3 and users.username[0] == full_data['first_name'][0] and users.username[2:] == full_data['last_name']:
                users.first_name = full_data['first_name']
                users.last_name = full_data['last_name']
                users.save()
                profile = UserProfile.objects.get(user=users.id)
                profile.avatar_urls = full_data['avatar_url']
                profile.save()
                return

