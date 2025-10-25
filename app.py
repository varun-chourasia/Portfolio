from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
from routes.contact import contact_bp
from routes.portfolio import portfolio_bp
from models import db
from sqlalchemy import text


# Load environment variables
load_dotenv()


# Initialize Flask app
app = Flask(
    __name__,
    static_folder='templates/',
    template_folder='templates/'
)


# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key-change-in-production')


# ✅ DATABASE SETUP FOR RENDER
db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url  # No sslmode param
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///local.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# ✅ BREVO EMAIL CONFIGURATION
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp-relay.brevo.com')
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
    try:
        db.create_all()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")


# --- Frontend Routes ---
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('static/assets', filename)


@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)


@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)


# --- Health Check ---
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'email_configured': bool(os.getenv('MAIL_USERNAME'))
    })


# ✅ TEST DATABASE CONNECTION
@app.route("/test-db")
def test_db():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "✅ Database connected successfully!"
    except Exception as e:
        return f"❌ Database error: {e}"


# --- Error Handlers ---
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500


# --- Main Entry Point ---
if __name__ == '__main__':
    # ✅ FIXED: Provide default port for local development
    port = int(os.getenv('PORT',10000)) 
    debug = os.getenv('FLASK_ENV', 'production') != 'production'
    
    print("=" * 50)
    print("🚀 Starting Portfolio Application")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI'][:30]}...")
    print(f"Email Server: {app.config['MAIL_SERVER']}")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
