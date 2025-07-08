from flask import Flask, request, render_template

app = Flask(__name__)

def get_romantic_message(choice):
    """Returns a romantic message based on the user's choice."""
    if choice == 1:
        return " you are my happiness and thank god you're with me 😍❤️"
    elif choice == 2:
        return "😍 wondering what's here? you cutie🥰🥰🥰 💖"
    elif choice == 3:
        return "💖 you're extraordinary and thankfully  mine 🥰 💘"
    elif choice == 4:
        return" I'm glad i met you 🥰🥰🥰"
    else:
        return "I always want to be with you 💖n 🥰💘"

@app.route("/")
def index():
    """Serves the romantic HTML page."""
    return render_template("index.html")

@app.route("/choice", methods=["GET"])
def handle_choice():
    """Handles the choice from the frontend and returns a message."""
    choice = request.args.get("value", type=int)
    message = get_romantic_message(choice)
    return message

if __name__ == "__main__":
    app.run(debug=True)
