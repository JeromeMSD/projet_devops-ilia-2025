from flask import Flask, render_template
from flags.app import flags_bp, feature_flags

app = Flask(__name__)

# Enregistre le Blueprint contenant toutes les routes de l'API de flags.
app.register_blueprint(flags_bp)

@app.route("/backoffice")
def backoffice():
    return render_template("backoffice.html", flags=feature_flags)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)