# Neighborly: Community Event Board App

Neighborly is a Flask web app for posting and discovering local events, clubs, and announcements. It uses SQLAlchemy and SQLite to store posts and user data, Bootstrap 4 for layout, and a custom CSS design system for styling.

## Features

- Create posts for events, clubs, or announcements
- Add location, date, time, and contact info to posts
- Tag posts with custom or default tags
- Filter the board by category or tag
- Register and log in with a username and password
- Edit and delete your own posts
- Mark events as recurring weekly
- Link Instagram pages, group chats, and contact emails on posts


## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

## Project Structure

```text
neighborly/
├── main.py
└── website/
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── auth.py
    ├── static/
    │   ├── css/style.css
    │   └── index.js
    └── templates/
        ├── base.html
        ├── home.html
        ├── create.html
        ├── edit_post.html
        ├── post.html
        ├── login.html
        └── sign_up.html
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jennarentz/projects.git
cd projects/neighborly
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install flask flask-sqlalchemy flask-login
```

## How to Run

From the `neighborly` folder:

```bash
python main.py
```

Then open this URL in your browser:

```text
http://127.0.0.1:5000
```

## How to Use

1. Open the app in your browser.
2. Create a new account.
3. Click **+ Post** to create a new post.
4. Fill in the title, description, location, date, and tags.
5. Browse the board and filter posts by category or tag.
6. Click any post to view full details and contact links.
7. Edit or delete your own posts from the post detail page.

## Database

The app uses SQLite to store users and posts.

The main models are:

- **User** — stores email, username, hashed password, first name, bio, and optional social links 
- **Post** — stores title, body, category, location (city, zip, venue name), event date and time, recurring flag, contact info, and a foreign key to the author
- **Tag** — stores a unique tag name; linked to posts through a `post_tags` association table (many-to-many)


## Future Improvements
- Add a `requirements.txt` file
- Add a user profile page with bio and social links
- Add auto-tagging via the Anthropic API
- Add search by keyword
- Add image uploads for posts
- Move `SECRET_KEY` to an environment variable