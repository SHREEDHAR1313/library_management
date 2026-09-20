# Library Management System (Django)

A full-stack library management web app — built with Django, matching the
same stack as my DPLOY e-commerce project (Django, Python, SQLite).

## Features

- **Book management** — add, search, and delete books; tracks total vs. available copies
- **Member management** — add and remove library members
- **Issue / Return workflow** — issue a book to a member with a due date; returning it restores the available copy count
- **Overdue tracking** — issued books past their due date are flagged automatically
- **Dashboard** — live summary stats (titles, copies available, members, active issues, overdue count)
- **Transaction history** — full log of every issue/return
- **Django Admin** — full CRUD on all models out of the box at `/admin/`

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (swap-in ready for MySQL/PostgreSQL via `DATABASES` in `settings.py`)
- **Frontend:** Django templates + Tailwind CSS (CDN, no build step)

## Project Structure

```
library_management/
├── catalog/
│   ├── models.py            # Book, Member, Transaction models
│   ├── views.py              # Dashboard, CRUD, issue/return logic
│   ├── admin.py               # Django admin registration
│   ├── urls.py                 # App routes
│   ├── management/commands/
│   │   └── seed_data.py          # Seeds 5 sample books
│   └── templates/catalog/
│       ├── base.html               # Shared layout + nav (Tailwind)
│       ├── dashboard.html
│       ├── books.html
│       ├── members.html
│       ├── issue.html
│       └── transactions.html
├── library_management/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt
```

## Setup & Run

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_data      # optional: adds 5 sample books
python manage.py createsuperuser  # optional: for /admin/ access

python manage.py runserver
```

Visit `http://localhost:8000/` for the app, or `http://localhost:8000/admin/`
for the Django admin panel.

## Design Notes (for interview discussion)

- **Data integrity:** issuing/returning a book updates `available_copies` and
  creates/updates a `Transaction` row inside a single `db_transaction.atomic()`
  block, so the two writes can't get out of sync if one fails partway.
- **Guard rails:** a book or member with an active (unreturned) issue can't
  be deleted, and a book with zero available copies can't be issued.
- **Overdue detection** is computed on read (`due_date < now`) via a model
  property rather than stored, so it's always accurate without a background job.
- **Why Django:** reused the same framework as my DPLOY project — model
  layer, admin panel, and template system all came from the same toolkit,
  so this stayed consistent with the rest of my backend work instead of
  introducing a new stack just for one project.

## Possible Extensions

- Add authentication (member login/self-service) using Django's built-in auth
- Fines calculation for late returns
- Email reminders for due/overdue books (Django's `send_mail`)
- REST API layer with Django REST Framework for a React frontend
- Deploy on Render/Railway with a live demo link on the resume
