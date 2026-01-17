"""
Simple wrapper to import the Flask app for deployment compatibility.
The main application code is in checkball.py
"""
from checkball import app

if __name__ == '__main__':
    app.run()
