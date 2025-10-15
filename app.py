# Deployment setup for The Manhattan International School Flask app
# This version adds deployment configuration for services like Render or PythonAnywhere.
# Files to include when publishing:
#   - app.py (this file)
#   - requirements.txt
#   - Procfile (for Render or Heroku)
#   - runtime.txt (optional, to specify Python version)

import os
import sys
import subprocess

# Ensure Flask is installed
try:
    from flask import Flask, render_template_string
except ModuleNotFoundError:
    print("Flask not found. Installing Flask via pip...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
    from flask import Flask, render_template_string

import unittest

app = Flask(__name__)

# School information
school_info = {
    'name': 'The Manhattan International School',
    'location': 'Sufra Gardens, East Church Road, Nairobi',
    'contact': '0758 444 666',
    'email': 'manhattanschool24@gmail.com'
}

# Teacher data
teachers = [
    {'grade': 6, 'name': 'Mr. Wycliff Arons', 'contact': '0708 058 109'},
    {'grade': 7, 'name': 'Mr. Wendo Kenyanito', 'contact': '0703 910 950'},
    {'grade': 8, 'name': 'Ustadha Mumtaza Mohamed', 'contact': '0703 376 802'},
    {'grade': 9, 'name': 'Mr. Ibrahim Dida', 'contact': '0792 547 465'},
    {'grade': 10, 'name': 'Mr. Abdifatah Mohamed', 'contact': '0115 063 469'},
    {'grade': 11, 'name': 'Mr. Ismail Hassan', 'contact': '0700 444 767'},
    {'grade': 12, 'name': 'Mr. Issac Onyango', 'contact': '0728 178 075'},
    {'grade': 13, 'name': 'Mr. Abdilatif Ibrahim', 'contact': '0710 792 169'}
]

# Prepare telephone links
for t in teachers:
    t['tel'] = t['contact'].replace(' ', '')

html_template = """<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>{{ school_info.name }}</title>
<style>
body { font-family: Arial, sans-serif; background: #f4f4f9; margin: 0; padding: 0; }
header { background: #b30000; color: white; text-align: center; padding: 20px; }
.container { width: 90%; max-width: 1000px; margin: 20px auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }
th { background: #f44336; color: white; }
tr:hover { background: #f1f1f1; }
footer { text-align: center; background: #333; color: white; padding: 15px; margin-top: 20px; }
a.phone { color: inherit; text-decoration: none; }
</style>
</head>
<body>
<header>
<h1>{{ school_info.name }}</h1>
<p>{{ school_info.location }}</p>
<p>Tel: {{ school_info.contact }} | Email: <a href='mailto:{{ school_info.email }}'>{{ school_info.email }}</a></p>
</header>
<div class='container'>
<h2>Class Teachers Contact Information</h2>
<table>
<thead><tr><th>Grade</th><th>Class Teacher</th><th>Contact</th></tr></thead>
<tbody>
{% for teacher in teachers %}
<tr>
<td>{{ teacher.grade }}</td>
<td>{{ teacher.name }}</td>
<td><a class='phone' href='tel:{{ teacher.tel }}'>{{ teacher.contact }}</a></td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
<footer>&copy; {{ year }} The Manhattan International School. All rights reserved.</footer>
</body>
</html>"""

@app.route('/')
def home():
    from datetime import datetime
    return render_template_string(html_template, school_info=school_info, teachers=teachers, year=datetime.now().year)

# Unit tests
class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_status(self):
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_school_name(self):
        html = self.client.get('/').get_data(as_text=True)
        self.assertIn(school_info['name'], html)

    def test_teacher_list(self):
        html = self.client.get('/').get_data(as_text=True)
        for t in teachers:
            self.assertIn(t['name'], html)

if __name__ == '__main__':
    restricted_env = any([
        os.environ.get('SANDBOX_MODE') == '1',
        os.environ.get('CI') == 'true',
        os.environ.get('PYTHONANYWHERE_SITE'),
        'JPY_PARENT_PID' in os.environ,
        os.environ.get('GITHUB_ACTIONS') == 'true'
    ])

    if restricted_env:
        print("Restricted environment detected — Flask server won't start.")
        with app.test_request_context('/'):
            print(home())
    else:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)

# --- Deployment files to add in your project directory ---
# requirements.txt
#   flask==3.0.3
# Procfile
#   web: python app.py
# runtime.txt
#   python-3.12.3

# To deploy on Render:
# 1. Push your files to a GitHub repository.
# 2. Go to https://render.com > New Web Service > Connect repo.
# 3. Choose 'Flask' environment (Python 3), select app.py as the entry point.
# 4. It will build automatically and provide a live public URL.

# To deploy on PythonAnywhere:
# 1. Create an account on https://www.pythonanywhere.com.
# 2. Upload app.py and requirements.txt.
# 3. Set up a Flask app under 'Web' tab using app:app.
# 4. Reload the web app and open your live site URL.
