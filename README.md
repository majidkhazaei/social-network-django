# 📱 Social Network Project with Django

A modern and complete social network built with the Django framework. This project includes full user features, posts, comment and reply system, likes, search, user profiles, and profile editing.

## ✨ Key Features

- **User Authentication**  
  Register, login, and logout with full form validation (using Django)

- **User Profiles**  
  View other users' profiles, edit personal profile (extendable)

- **Post Management**  
  Create new posts, edit posts, delete posts (only for the post owner)

- **Like System**  
  Like posts with like count display, and disable the button for users who have already liked

- **Comments & Replies**  
  Any logged-in user can comment on posts and reply to others' comments.  
  Comment and reply forms are **collapsible** to keep the page clean.

- **Post Search**  
  Simple search using a GET form on the home page

- **Responsive & Dark Mode**  
  Fully optimized for mobile and tablet; also supports browser's Dark Mode preference

- **Modern & Consistent Styling**  
  Custom CSS with gradients, smooth animations, and beautiful shadows across all pages (home, post detail, profile, edit profile, register)

## 🛠 Technologies Used

- **Backend**: Django 6.x
- **Frontend**: HTML5, CSS3 (pure, no framework)
- **Font & Icons**: Google Fonts (Inter) + FontAwesome 6
- **Database**: SQLite (can be switched to PostgreSQL, MySQL)
- **JavaScript** (Vanilla + jQuery for collapsible comment section)


## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/majidkhazaei/social-network-django.git
   cd social-network

2. **Create a virtual environment (recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    
3. **Install dependencies**    
    ```bash
    pip install django
    
4. **Run migrations**
    ```bash
    python manage.py migrate
    
5. **Start the development server**
    ```bash
    python manage.py runserver

