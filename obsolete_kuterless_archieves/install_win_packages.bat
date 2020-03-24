win64-setup.cmd
easy_install paramiko==1.10.2
easy_install Fabric==1.14.0
easy_install certifi==2017.11.5
easy_install chardet==3.0.4
easy_install django-uni-form==0.9.0
easy_install gunicorn==19.7.1
easy_install idna==2.6
easy_install pycrypto==2.6
easy_install python-dateutil==2.6.1
easy_install requests==2.18.4
easy_install vobject==0.9.5
easy_install psycopg2==2.5.2
pip install -r windows_current_requirement.txt
cd kuterless
python manage.py runserver

