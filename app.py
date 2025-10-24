from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
from routes.contact import contact_bp
from routes.portfolio import portfolio_bp
from models import db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(
    __name__,
    static_folder='templates/',
    template_folder='templates/'
)

# --- Configuration ---
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

# Use DATABASE_URL (Render default), fallback to local Postgres for development
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Optional: Mail configuration (only if you use Flask-Mail)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Enable CORS
CORS(app)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(contact_bp, url_prefix='/api/contact')
app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')

# Create tables automatically (only once)
with app.app_context():
    db.create_all()

# --- Frontend Routes ---
@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('templates/assets', filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('templates/css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('templates/js', filename)

# --- Health Check ---
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# --- Error Handlers ---
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# --- Main Entry Point ---
if __name__ == '__main__':
    port = int(os.environ('PORT'))  # Render usually assigns PORT dynamically
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
