
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url + "?sslmode=prefer"
 # No sslmode param
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///local.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# ✅ BREVO EMAIL CONFIGURATION
# app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp-relay.brevo.com')
# Brevo API Config
app.config['BREVO_API_KEY'] = os.getenv('BREVO_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['RECIPIENT_EMAIL'] = os.getenv('RECIPIENT_EMAIL')

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

