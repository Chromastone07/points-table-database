from flask import Flask, request, render_template

app = Flask(__name__)

def get_romantic_message(choice): 
    """Returns a romantic message based on the user's choice."""
    if choice == 1:
        return " Arey aap yaha ? 😍❤️"
    elif choice == 2:
        return "😍 ohh curious hoke saare options select kroge kya ab 🥰🥰🥰 💖"
    elif choice == 3:
        return "💖 I knew it dekha yaha bhi aagye na 🥰 💘"
    elif choice == 4:
        return "ye to yahi khatam hota hai but aapki sundarta to anant hai vo to hamesha aise hi barkarar rahegi  🥰 💘 "
    else:
        return "Arey bas ho gya khatam, itna hi tha baki aur chahiye to hum hai na 🥰🥰🥰 " 

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
