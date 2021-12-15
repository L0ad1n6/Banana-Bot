from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return "ESR Card Trading Bot is Operational."

def run():
  app.run(host="0.0.0.0", port=8080, debug=True)

def keep_alive():
  server = Thread(target=run)
  server.start()