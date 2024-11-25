This is a Movie ticket booking system designed for booking shows and food orders through an online platform. Here,  both theater admins and regular users can create and edit details to efficiently manage the theater. All the pages have role based access and checks to prevent the wrong user from accessing a page. 

Setup process:
1. terminal commands
    brew install python
    pip install django
    django-admin --version  //verify if it has been installed successfully


    python3 -m venv venv //optional,  but recommended
    source venv/bin/activate 
    pip install jwt
    pip install allauth
    pip install requests
    pip install psycopg
    pip install psycopg2
    pip install pyjwt
    pip install python-dotenv


    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser

Execute the commands one by one or you may also run sh myscript.sh to run all at once

2. Go to admin site,  login and under Social Applications,  create a new one,  set provider as Google and set the name as Google Login(for example),  and choose a site(localhost:8000),  set 
Client ID = 1063058262520-nj0g9ou3g2k132k6egrimd0jehemb1jqapps.googleusercontent.com,  and 
secret key = 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,  as already mentioned in movie/settings.py.

Now,  in movie/settings.py set SITE_ID acc to the site(localhost:8000) on the machine. For my machine it was 2.

Install docker on your machine.

Terminal Commands:
    pip freeze > requirements.txt
    docker-compose build
    docker-compose up
    docker-compose up -d
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec web python manage.py runserver