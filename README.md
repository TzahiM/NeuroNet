Dev setup:

    git clone
    cd NeuroNet

On windows:
    win32-setup.cmd
    or
    win64-setup.cmd

    pip install -r requirements-base.txt

On linux:

    pip install -r requirements-dev.txt


Setup db:

    cd kuterless
    python manage.py sqlcreate --router=default | psql -U  postgres
    python manage.py syncdb --migrate --noinput

    python manage.py createsuperuser



