<div align="center">
    <a href="https://appseed.us/product/rocket/django/">
        <img src="https://github-production-user-asset-6210df.s3.amazonaws.com/51070104/272178364-cbac6d97-b2dc-4d95-bab6-891f4ee7d84d.png"" width="64" height="64" alt="Rocket Icon">
    </a>
    <h1>
        <a href="https://github.com/NathanPerrier/IA3-Perrier-Fishing-Website-Digital">
            IA3 Fishing Website
        </a>
    </h1>
    <p>
        <strong>Rocket Django</strong> &bull; <strong>TailwindCSS</strong> &bull; <strong>OpenAI</strong> &bull; <strong>Flowbite</strong> &bull; <strong>API (DRF)</strong> &bull; <strong>Celery Beat</strong> &bull; <strong>DataTables</strong> &bull; <strong>Charts</strong> &bull; <strong>Docker</strong> &bull; <strong>CI/CD</strong>
    </p>     
</div>

<br />

<div align="center">
    <img src="https://github-production-user-asset-6210df.s3.amazonaws.com/51070104/272299949-6f4a8fd7-7cce-472a-9566-9519db338c7d.gif" alt="Django Rocket - Open-source Starter styled with Tailwind and Flowbite.">
</div>

<br />

## About [Fishing App Name](https://github.com/NathanPerrier/IA3-Perrier-Fishing-Website-Digital)

#### ***Supercharge your app instantly, launch faster, make $***

Login users, process payments and send emails at lightspeed. Spend your time building your startup, not integrating APIs. **Rocket Django** provides you with the boilerplate code you need to launch, FAST. 

#### ***Rocket your startup in days, not weeks*** 

The Django boilerplate has all you need to build your SaaS, Analytics tool, or any other type of Web App. From idea to production in 5 minutes.

#### **48+ hours of headaches**

 - 1 hrs to setup the project 
 - 2 hrs integrate tooling
 - 2 hrs to handle Stripe
 - 1 hrs for Docker
 - 1 hr Google Oauth
 - ∞ hrs overthinking...
 - Free [Support](https://appseed.us/support/) via `Email` & [Discord](https://discord.gg/fZC6hup) 

<br />

## Manual Build 

> 👉 Download code

```bash
git clone https://github.com/app-generator/rocket-django.git
cd rocket-django
```

> 👉 Create `.env` from `env.sample`

```env
DEBUG=False

SECRET_KEY=<STRONG_KEY_HERE>

# For Myql or PgSQL Persistence 
# DB_ENGINE=mysql
# DB_HOST=localhost
# DB_NAME=appseed_rocket_django
# DB_USERNAME=root
# DB_PASS=
# DB_PORT=3306

# SMTP configaration
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=
# EMAIL_HOST_PASSWORD=
```

> 👉 Unrestrict **current user** scope   

```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force;
```

> 👉 Install **Django** modules via `VENV`  

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

> 👉 Install **Tailwind/Flowbite** (another terminal)

Tested with **Node** `v18.20.0` (use at least this version or above)

```bash
npm install
npm run dev
npx tailwindcss -i ./static/assets/style.css -o ./static/dist/css/output.css --watch # DEVELOPMENT (LIVE reload)
npx tailwindcss -i ./static/assets/style.css -o ./static/dist/css/output.css         # PRODUCTION
```

> 👉 Migrate DB

```bash
python manage.py makemigrations
python manage.py migrate
```

> 👉 `Create Superuser` & Start the [Rocket Django](https://appseed.us/product/rocket/django/) Starter

```bash
python manage.py createsuperuser # create the admin
python manage.py runserver       # start the project
```

<br />

## Start With Docker

> 👉 Download code

```bash
git clone https://github.com/app-generator/rocket-django.git
cd rocket-django
```

> 👉 Start with Docker Compose

```bash
docker-compose up --build 
``` 

Visit the app in the browser `localhost:5085`.

<br />

## Use MySql 

By default, the starter uses SQLite for persistence. In order to use MySql, here are the steps: 

- Start the MySql Server
- Create a new DataBase
- Create a new user with full privileges over the database 
- Install the MySql Python Driver (used by Django to connect)
  - `pip install mysqlclient`
- Edit the `.env` with the SQL Driver Information & DB Credentials 

```env

DB_ENGINE=mysql
DB_HOST=localhost
DB_NAME=<DB_NAME_HERE>
DB_USERNAME=<DB_USER_HERE>
DB_PASS=<DB_PASS_HERE>
DB_PORT=3306

```

Once the above settings are done, run the migration & create tables: 

```bash
python manage.py makemigrations
python manage.py migrate
```

<br />

## Production Build

To use the starter in production mode, here are the steps: 

- Set  **DEBUG=False** in `.env`
- Execute `collectstatic` command
  - `python manage.py collectstatic --no-input`

As a model, feel free to take a look at [build.sh](./build.sh), the file executed by the CI/CD flow for Render:   


<br />

## **Deploy on Render**

- Create a Blueprint instance
  - Go to https://dashboard.render.com/blueprints this link.
- Click `New Blueprint Instance` button.
- Connect the `repo` that you want to deploy.
- Fill the `Service Group Name` and click on the `Update Existing Resources` button.
- Edit the Environment and [specify the PYTHON_VERSION](https://render.com/docs/python-version)
  - Version `3.11.5` was used for **[this deployment](https://rocket-django.onrender.com/)**
- After that, your deployment will start automatically.

At this point, the product should be LIVE.

<br />

## Codebase 

```bash
< PROJECT ROOT >
   |
   |-- core/                 # Project Settings 
   |    |-- settings.py 
   |    |-- wsgi.py     
   |    |-- urls.py     
   |
   |-- home/                 # Presentation app 
   |    |-- views.py         # serve the HOMEpage  
   |    |-- urls.py     
   |    |-- models.py
   |
   |-- apps/                 # Utility Apps 
   |    |-- common/          # defines models & helpers
   |    |    |-- models.py   
   |    |    |-- util.py 
   |    |-- users            # Handles Authentication 
   |    |-- api              # DRF managed API
   |    |-- charts           # Showcase Different Charts
   |    |-- tables           # Implements DataTables
   |    |-- tasks            # Celery, async processing
   |
   |-- templates/            # UI templates 
   |-- static/               # Tailwind/Flowbite 
   |    |-- src/             # 
   |         |-- input.css   # CSS Styling
   |
   |-- Dockerfile            # Docker
   |-- docker-compose.yml    # Docker 
   |
   |-- render.yml            # CI/CD for Render
   |-- build.sh              # CI/CD for Render 
   |
   |-- manage.py             # Django Entry-Point
   |-- requirements.txt      # dependencies
   |-- .env                  # ENV File
   |
   |-- *************************************************      
```   

<br />

## License

@MIT

<br />

---
[Rocket Django](https://appseed.us/product/rocket/django/) - Open-source starter styled with `Tailwind/Flowbite` actively supported by **[AppSeed](https://appseed.us)**.