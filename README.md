<div align="center">

# 🍽️ MealMate

### A full-stack food delivery web application built with Django

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_Site-ff5722?style=for-the-badge)](https://meal-mate-e3lr.onrender.com)

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)
![Razorpay](https://img.shields.io/badge/Razorpay-Integrated-02042B?style=flat-square&logo=razorpay&logoColor=white)
![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)

</div>

---

MealMate lets customers browse restaurants, search by cuisine, manage a cart, and pay securely online — while admins manage restaurants and menus through a dedicated dashboard.

> ⚠️ Hosted on a free tier — the first load after inactivity may take ~50 seconds to wake up.

<br>

## ✨ Features

| | |
|---|---|
| 🔍 **Search & Filter** | Find restaurants by name or cuisine |
| 🛒 **Smart Cart** | Add items, adjust quantities, remove items |
| 💳 **Secure Checkout** | Razorpay integration with server-side signature verification |
| 📦 **Order History** | Every completed order saved with itemized details |
| 🛠️ **Admin Dashboard** | Add, edit, and delete restaurants and menu items |
| 👤 **User Accounts** | Sign up, sign in, role-based routing |
| 🎨 **Custom UI** | Hand-built responsive design, no CSS framework |

<br>

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Backend** | Django (Python) |
| **Database** | SQLite |
| **Payments** | Razorpay API |
| **Frontend** | HTML, custom CSS |
| **Deployment** | Render · Gunicorn · WhiteNoise |

</div>

<br>

## 📸 Screenshots

<img width="1917" height="867" alt="image" src="https://github.com/user-attachments/assets/8a4d9a0b-49e0-43d7-abaa-5267635b08ba" />


<br>

## 🚀 Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/ssuvadeep/meal_mate.git
cd meal_mate
```

**2. Set up a virtual environment**
```bash
python -m venv myenv
myenv\Scripts\activate      # Windows
pip install -r requirements.txt
```

**3. Create a `.env` file** in the project root:
```env
SECRET_KEY=your-secret-key
DEBUG=True
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
ALLOWED_HOSTS=127.0.0.1,localhost
```

**4. Run migrations and start the server**
```bash
python manage.py migrate
python manage.py runserver
```

**5. Open your browser**
http://127.0.0.1:8000

<br>

## 📌 Notes

- 🎓 This is a learning/portfolio project — not production-hardened
- 🔓 Passwords are stored in plain text — not for real-world use
- 🔄 Database resets on redeploy (SQLite on free hosting isn't persistent)
- 🧪 Razorpay runs in **test mode** — no real payments are processed

<br>

## 👤 Author

**Suvadeep Samanta**

<div align="center">

*Built as a hands-on project to learn full-stack web development*

</div>
