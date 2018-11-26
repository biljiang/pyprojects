### Set up the website

Follow django document 2.1 tutorial. https://docs.djangoproject.com/en/2.1/

1. django-admin startproject XXXX/python manage.py runserver 0:8000/python manage.py startapp XXXX/ modify urls.py|views.py

2. setup postgresql/modify settings.py/install psy2copy/python manage.py migrate/ python manage.py createsuperuser

### Set up Nginx

1. sudo apt install nginx / nginx service will be started by systemd after the installation is done

2. to check nginx use chrome to access IP address:80 

### Set up uwsgi

1. pip install uwsgi / here we need to use "pip install" instead of "apt install" because pip will install uwsgi into anaconda3/bin, which starts python3. otherwise system default python2.7 will be started /http://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/tutorials/Django_and_nginx.html

2. unsuccessful installation error fix for uwsgi/ https://www.cnblogs.com/liuzhen1995/p/8893962.html  /apt install gcc4.7 / "ls /usr/bin/gcc* -l" / modify the link to gcc4.7 version
https://blog.csdn.net/jacke121/article/details/54565281

    ln -s /usr/local/lib/libpcre.so.1 /lib64

3. successful installation error fix for uwsgi/ https://blog.csdn.net/king_way/article/details/80821139

    conda install -c conda-forge uwsgi

    conda install -c conda-forge libiconv   

    to check uwsgi, in demoweb directory run:

    uwsgi --http :8000 --module demoweb.wsgi      or
    uwsgi --http :8000 --wsgi-file test.py

### Configure uwsgi and nginx to work together

1. start on boot for uwsgi with emperor https://uwsgi.readthedocs.io/en/latest/WSGIquickstart.html#deploying-django https://uwsgi.readthedocs.io/en/latest/Systemd.html   https://uwsgi.readthedocs.io/en/latest/WSGIquickstart.html

2. edit /etc/uwsgi/emperor.ini | vim /etc/uwsgi/apps/available/demoweb.ini and ln -s to ../apps-enabled/demoweb.ini

    vim /etc/systemd/system/emperor.uwsgi.service

3. vim /etc/nginx/sites-available/default | vim /etc/nginx/sites-available/demoweb.conf
 
    There should be a demoweb_ssl.conf in ../snippets directory if a ssl certificate available.

### Set up website

1. copy admin/static/admin | amin/templates/admin | admin/templates/registration | modify base_site.html
https://docs.djangoproject.com/en/2.1/intro/tutorial07/

2. download and install bootstrap | 
https://getbootstrap.com/docs/4.1/getting-started/introduction/ | https://jquery.com/download/ | https://popper.js.org/ git hub installation documentation

    wget https://unpkg.com/popper.js

    wget https://unpkg.com/popper.js/dist/umd/popper.min.js

    wget https://code.jquery.com/jquery-3.3.1.min.js

    wget https://code.jquery.com/jquery-3.3.1.slim.min.js

### Note for login and out mechanics of www.avarun.cn

    login uses post method, so anywhere in the website will return to where the request was sent from. i.e. the same page

    logout use views.logout_view, which is named as "logout_view" and is defined in the views.py file, and redirected to the Homepage.

    django.contrib.auth has urls named as "logout" and "login". and the website self_defined urls was named "logout_view" and "login_view"


### Git backup command

    git log --graph --oneline --decorate

    git push origin dev

    
### Fontawesome js

    https://fontawesome.com/how-to-use/on-the-web/using-with/jquery

    http://www.runoob.com/bootstrap/bootstrap-collapse-plugin.html

    https://getbootstrap.com/docs/4.0/components/collapse/

    https://www.w3cschool.cn/jquery/xs75ofnl.html



### Demoweb directory structure
 
    template directory includes admin/registration for user management

    template/site directory for site base templates

    static/base for outsite css/js codekit, including bootstrap/fontawesome/bokeh etc. while static/site uses soft link to respective files in static/base to form the css/js used in the website


### Demoweb AJAX 

    /shdky/v_simu commprises of two AJAX application.

1. useing AJAX to upload file is a bit different than conventional django forms file upload. we need to define from in js code in template file instead of in forms.py and views.py. and FormData in js code defines a new form, in which we need to put in a declaration of {{crsf token}}.

        
2. class base view for all web page; and function base view for AJAX response

   https://www.cnblogs.com/yangtoude/p/jquery-ajax-formdata-upload.htmlhttps://www.cnblogs.com/yangtoude/p/jquery-ajax-formdata-upload.html


### Github setup 

   cd /home/techstar/demoweb
   git init
   git add .
   git config --global user.email "biljiang@outlook.com"
   git config --global user.name "Jiang Feng demoweb"
   git commit -m "init version"

   set up new repo on github/add readme|gitignore|license

   git remote add origin https://github.com/biljiang/demoweb

   git pull remote master

   git push -u remote master
    



### use pyinstaller compile python 
conda install -c conda-forge pyinstaller
export LD_LIBRARY_PATH="/home/techstar/anaconda3/pkgs/python-3.6.5-hc3d631a_2/lib"
pyinstaller expirationcheck.py
~/PyProjects/ShanghaiPower/dist/expirationcheck/expirationcheck



### compile python code to so

    conda install cython


creat build_up.py file

    from distutils.core import setup
    from Cython.Build import cythonize

    setup(ext_modules = cythonize(["your_file.py"]))

cd your_file.py directory

python build_up.py build_ext


~/PyProjects/ShanghaiPower/build/lib.linux-x86_64-3.6/expirationcheck.cpython-36m-x86_64-linux-gnu.so

https://blog.csdn.net/linshenyuan1213/article/details/72677246

https://blog.csdn.net/qq_20154743/article/details/77891572
### python encrypt

Windows:
pip install pycryptodomex
from Cryptodome.Cipher import AES

linux:
pip install pycryptodome
import Crypto

https://www.cnblogs.com/renfanzi/p/6062261.html

https://www.cnblogs.com/wangxiaoqun/p/9045260.html

https://www.cnblogs.com/kaituorensheng/p/4501128.html



### demoweb on Chengdu server has license check directory

which has been compiled under C code and could make license check.




