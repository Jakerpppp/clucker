# Clucker - Django Project

## Overview

Welcome to Clucker, a Django-based microblogging application developed as part of the Software Engineering Group Project by Dr Jeroen Keppens in order to learn the Fundamentals of Django Website Development. This project is a Chicken Styled Microblogs application inspired by Twitter, where the primary focus is on mastering Django and Test Driven Development (TDD) with automated testing. Clucker allows users to create authenticated profiles, post blog messages, follow other users, and view personalized feeds.
- Made in from October 2023 to November 2023

## Features

- **User Authentication:**
  - Create, edit, and manage secure user profiles.

- **Microblogging:**
  - Post short messages, akin to tweets on Twitter.

- **Following System:**
  - Follow other users.
  - Be followed back by other users.

- **Personalized Feed:**
  - View a feed showcasing blog posts from users you follow.

## Getting Started

Follow these steps to set up the Clucker project locally:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/jakerpppp/clucker.git
   cd clucker
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment:**
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Database Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application:**
   Open your web browser and go to `http://127.0.0.1:8000/` to access Clucker.

## Running Tests

To run automated tests and ensure the robustness of your application, use the following command:

```bash
python manage.py test
```

Feel free to explore, contribute, and make Clucker your own microblogging playground!
