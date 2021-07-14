docker container exec -it wagtail-cms_web_1 python manage.py migrate
docker container exec -it wagtail-cms_web_1 python manage.py populate_cms
docker container exec -it wagtail-cms_web_1 python manage.py populate_courses
docker container exec -it wagtail-cms_web_1 python manage.py populate_institutions
