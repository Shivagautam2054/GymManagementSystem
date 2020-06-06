> Creating a new project:-
    django-admin startproject projectName

> Run Application:-
    python manage.py runserver

> Setup initial database and create required tables and data for   defult applications:-
    python manage.py migrate

> Admin: Create super user
    python manage.py createsuperuser

> Create application
    python manage.py startapp appname

> SQlite Browser

>Whenever there is change in Models, we need to migrate the changes in the database.
1. Create Migrations
	python manage.py makemigrations >> will create migrate related files in migrations/ of the app

2. Migrate
	python manage.py migrate


> Database Relations
	ForeignKey has maintain relation in our project.

> Testing Django Models
	python manage.py shell

> CRUD Operations
	To select:
		User.objects.all() : SELECT * From gyms_user
	To insert:
		user = User()
		user.full_name = "Shiva Gautam"
		user.save() : "INSERT into gyms_user......"
	To Update:
		user_list = User.objects.all()
		user = user_list[0]
		user.password = 'shiva'
		user.save() :"Update gyms_user set password = 'shiva' where user = user"
	To Delete:
		user.delete() : Delete gym_user where user = user

day15_1
