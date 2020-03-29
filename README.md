Install:
1 - clone this repository
git clone https://github.com/TzahiM/NeuroNet.git

dev server
windows:
2 - exttact NeuroNet\Backend\install.7z into another directory (not in the cloneed root)
3 - install python
install into dir: c:\Python37
4 - install windows virtual anv wrapper https://pypi.org/project/virtualenvwrapper-win/
5 - create virtual env for ths project and activate it
6 - install python packages from 
pip install -r  NeuroNet\Backend\NeuroNet\requirements.txt
7 - merge the changes from of your *.py env in the following files to the files in NeuroNet\Backend\NeuroNet\EnvDjango2_2_7
C:\inetpub\wwwroot\NeuroNet\Backend\NeuroNet\EnvDjango2_2_7\Lib\site-packages\django\forms\boundfield.py
C:\inetpub\wwwroot\NeuroNet\Backend\NeuroNet\EnvDjango2_2_7\Lib\site-packages\floppyforms\__init__.py
8 - Init db
cd NeuroNet\Backend\NeuroNet
python manage.py makemigrations
python manage.py migrate
add admin user
9 - add a default initial debug db configuration
from public_fulfillment.services import create_segment
segment = create_segment( 'tmp1', '123', 't1')



