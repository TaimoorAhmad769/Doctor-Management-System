# Doctor Management System

A RESTful Doctor Management System built with **Django** and **Django REST Framework (DRF)**.

The project provides APIs for managing doctors, patients, and appointments, with **JWT authentication** and **role-based permissions** to control access to resources.

## 🚀 Features

* Doctor management
* Patient management
* Appointment management
* RESTful APIs using Django REST Framework
* JWT-based authentication
* Protected API endpoints
* Role-based access control
* Doctor ownership permissions
* Admin access to manage system resources
* Patient and doctor relationships
* Appointment status management
* Django ORM with database migrations

## 🛠️ Tech Stack

* **Python**
* **Django**
* **Django REST Framework**
* **Simple JWT**
* **SQLite**
* **Git & GitHub**
* **Postman** for API testing

## 🔐 Authentication & Authorization

The API uses **JSON Web Tokens (JWT)** for authentication.

Users can obtain an access token and use it to access protected API endpoints.

The project also implements role-based permissions to control what different users can access.

For example:

* **Admin** → Can manage doctors, patients, and appointments.
* **Doctor** → Can access resources according to their assigned permissions and ownership.
* **Authenticated users** → Can access protected endpoints where permitted.

## 📌 API Endpoints

### Authentication

| Method | Endpoint              | Description                          |
| ------ | --------------------- | ------------------------------------ |
| POST   | `/api/token/`         | Obtain JWT access and refresh tokens |
| POST   | `/api/token/refresh/` | Refresh an access token              |

### Doctors

| Method | Endpoint             | Description       |
| ------ | -------------------- | ----------------- |
| GET    | `/api/doctors/`      | List doctors      |
| POST   | `/api/doctors/`      | Create a doctor   |
| GET    | `/api/doctors/<id>/` | Retrieve a doctor |
| PUT    | `/api/doctors/<id>/` | Update a doctor   |
| DELETE | `/api/doctors/<id>/` | Delete a doctor   |

### Patients

| Method | Endpoint              | Description        |
| ------ | --------------------- | ------------------ |
| GET    | `/api/patients/`      | List patients      |
| POST   | `/api/patients/`      | Create a patient   |
| GET    | `/api/patients/<id>/` | Retrieve a patient |
| PUT    | `/api/patients/<id>/` | Update a patient   |
| DELETE | `/api/patients/<id>/` | Delete a patient   |

### Appointments

| Method | Endpoint                  | Description             |
| ------ | ------------------------- | ----------------------- |
| GET    | `/api/appointments/`      | List appointments       |
| POST   | `/api/appointments/`      | Create an appointment   |
| GET    | `/api/appointments/<id>/` | Retrieve an appointment |
| PUT    | `/api/appointments/<id>/` | Update an appointment   |
| DELETE | `/api/appointments/<id>/` | Delete an appointment   |

> Endpoint behavior and permissions may vary depending on the authenticated user's role.

## 📂 Project Structure

```text
Doctor-Management-System/
│
├── appointments/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .gitignore
├── manage.py
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/TaimoorAhmad769/Doctor-Management-System.git
```

### 2. Navigate into the project

```bash
cd Doctor-Management-System
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```bash
venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

The API will then be available at:

```text
http://127.0.0.1:8000/
```

## 🧪 API Testing

The APIs were tested using **Postman**.

For protected endpoints, include the JWT access token in the request headers:

```text
Authorization: Bearer <access_token>
```

## 🎯 What I Learned

This project helped me practice and understand:

* Building REST APIs with Django REST Framework
* Serializers and API views
* Django models and relationships
* CRUD operations
* JWT authentication
* API endpoint protection
* Role-based permissions
* Object ownership permissions
* Testing APIs with Postman
* Managing a project with Git and GitHub

## 🔮 Future Improvements

Some possible improvements for future versions include:

* API documentation with Swagger/OpenAPI
* Automated unit and API tests
* PostgreSQL database integration
* Docker support
* Frontend integration with React
* Appointment filtering and searching
* Email notifications
* Deployment to a production environment

## 👨‍💻 Author

**Taimoor Ahmad Durrani**

Built as a practical Django REST Framework project to strengthen backend development and API development skills.
