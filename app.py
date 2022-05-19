from flask import Flask, render_template, request

API_BASE_URL = "https://wger.de/api/v2/"

app = Flask(__name__)