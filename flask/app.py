from flask import Flask, render_template, request, send_from_directory, jsonify
import damage_calc, pokédex

app = Flask(__name__)

# Route for the landing page
@app.route('/')
def landing_page():
    return render_template('landing.html')

# Route for serving font files
@app.route('/fonts/<path:filename>')
def serve_font(filename):
    return send_from_directory('static/fonts', filename)

# Route for serving image files
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

# Route for the calculator page
@app.route('/calculator', methods = ("GET", "POST"))
def calculator():
    if request.method == "POST":
        # Retrieve form inputs
        selected_move = request.form.get("move")
        selected_user = request.form.get("user")
        selected_target = request.form.get("target")
        try:
            # Calculate damage using provided inputs
            info = damage_calc.basic_damage(selected_move.replace(' ', '-').lower(), selected_user.replace(' ', '-').lower(), selected_target.replace(' ', '-').lower())
            # Render results template with calculated damage information
            return render_template('results.html', damage_info=info)
        except Exception as e:
            # Render error template if an exception occurs during calculation
            error_message = f"An error occurred: {e}"
            return render_template('error.html', error_message=error_message)
    return render_template('calculator.html')

# Route for updating move list dynamically
@app.route('/update_movelist', methods=['POST'])
def update_movelist():
    # Retrieve user input from JSON data
    user_input = request.json['userInput']
    # Generate move list based on user input
    move_list = damage_calc.moveListGenerator(user_input)
    move_list = sorted(move_list)
    if move_list == None:
        # Return error message if move list is empty
        return jsonify({"error": "Invalid input. Please provide a valid Pokémon name."}), 400
    else:
        # Return sorted move list
        return jsonify(move_list)

# Route for the Pokédex page
@app.route('/pokedex', methods=("GET", "POST"))
def pokedex():
    if request.method == "POST":
        # Retrieve selected Pokémon from form input
        selected_mon = request.form.get("mon")
        try:
            # Retrieve Pokédex entry for the selected Pokémon
            dexentry = pokédex.dex((selected_mon.replace(' ', '-').lower()))
            # Render Pokédex results template with retrieved entry
            return render_template('dexresults.html', attributes=dexentry)
        except AttributeError:
            # Render error template if no results found for the selected Pokémon
            return render_template('error.html', error_message="No results found. Maybe you spelled the name incorrectly?")
    return render_template('pokédex.html')

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
