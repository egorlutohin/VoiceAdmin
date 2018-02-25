import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponse

from VoiceAdmin.user_access import ALLOWED_USERS

def _get_allowed_dirs(user):
	username = user.username
	try:
		allowed_dirs = ALLOWED_USERS[username]['dirs']
	except:
		allowed_dirs = []
		
	return allowed_dirs


@login_required
def index(request):
	allowed_dirs = _get_allowed_dirs(request.user)
	
	return render(request, 'dirlist/index.html', {"dirs": allowed_dirs})
	
@login_required
def dates_index(request, phone_number):
	
	phone_number = os.path.split(phone_number)[-1]
	
	allowed_dirs = _get_allowed_dirs(request.user)
	
	if phone_number not in allowed_dirs:
		raise PermissionDenied()
		
	dates_dir = os.listdir(os.path.join(settings.RECORDS_DIR, phone_number))
	
	return render(request, 'dirlist/dates_index.html', {'phone_number': phone_number,'dirs': dates_dir})
	
@login_required
def records_index(request, phone_number, date_dir):
	phone_number = os.path.split(phone_number)[-1]
	date_dir = os.path.split(date_dir)[-1]
	
	allowed_dirs = _get_allowed_dirs(request.user)

	if phone_number not in allowed_dirs:
		raise PermissionDenied()
		
	dates_dir = os.listdir(os.path.join(settings.RECORDS_DIR, phone_number))
	
	if date_dir not in dates_dir:
		raise PermissionDenied()
		
	record_dir = os.path.join(settings.RECORDS_DIR, phone_number, date_dir)
	
	record_files = [f for f in os.listdir(record_dir) if (f.endswith('.wav') or f.endswith('.mp3')) and os.path.isfile(os.path.join(record_dir, f))]
	
	record_files.sort()
	
	l = []
	for f in record_files:
		try:
			p = f.split('_')
			p2 = p[0].split('-')
			time = p2[3]+':'+p2[4] +':'+p2[5]
			from_phone = p[2]
		except:
			time="-"
			from_phone = "-"
		l.append({'file': f, 'time': time, 'from_phone': from_phone})
	
	return render(request, 'dirlist/records_index.html', {'phone_number': phone_number, 'date': date_dir, 'files': l})

@login_required	
def deliver_record(request, phone_number, date_dir, record_file):
	phone_number = os.path.split(phone_number)[-1]
	date_dir = os.path.split(date_dir)[-1]
	record_file = os.path.split(record_file)[-1]
	
	allowed_dirs = _get_allowed_dirs(request.user)
	
	if phone_number not in allowed_dirs:
		raise PermissionDenied()
	
	dates_dir = os.listdir(os.path.join(settings.RECORDS_DIR, phone_number))
	
	if date_dir not in dates_dir:
		raise PermissionDenied()
		
	full_file_path = os.path.join(settings.RECORDS_DIR, phone_number, date_dir, record_file)
	
	if not os.path.isfile(full_file_path):
		raise PermissionDenied()
			
	response = HttpResponse()
	response['X-Accel-Redirect'] = os.path.join('/accel-redirect', phone_number, date_dir, record_file)
	
	return response
		
	

	
