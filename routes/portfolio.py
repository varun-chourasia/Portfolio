from flask import Blueprint, request, jsonify
from models import db, PortfolioVisit
from datetime import datetime, timedelta

portfolio_bp = Blueprint('portfolio', __name__)

# Portfolio data
PORTFOLIO_DATA = {
    "profile": {
        "name": "Varun Choursiya",
        "title": "Data Scientist",
        "email": "chourasiavarun16@gmail.com",
        "phone": "+91 975-287-5092",
        "location": "Indore, India",
        "github": "https://github.com/varun-chourasia",
        "linkedin": "https://linkedin.com/in/varun-chourasia-62b255266/",
        "twitter": "https://twitter.com/_varunchourasia_"
    },
    "stats": {
        "experience_programs": "2+",
        "projects": "15+",
        "certifications": "7+",
        "cgpa": "7.42"
    }
}

@portfolio_bp.route('/data', methods=['GET'])
def get_portfolio_data():
    """Get complete portfolio data"""
    return jsonify(PORTFOLIO_DATA), 200

@portfolio_bp.route('/track-visit', methods=['POST'])
def track_visit():
    """Track portfolio visit"""
    try:
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        
        visit = PortfolioVisit(
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(visit)
        db.session.commit()
        
        return jsonify({'success': True}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get portfolio statistics"""
    try:
        total_visits = PortfolioVisit.query.count()
        
        # Visits in last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_visits = PortfolioVisit.query.filter(
            PortfolioVisit.visited_at >= seven_days_ago
        ).count()
        
        # Total messages
        from models import ContactMessage
        total_messages = ContactMessage.query.count()
        unread_messages = ContactMessage.query.filter_by(is_read=False).count()
        
        return jsonify({
            'total_visits': total_visits,
            'recent_visits': recent_visits,
            'total_messages': total_messages,
            'unread_messages': unread_messages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/download-resume', methods=['GET'])
def download_resume():
    """Endpoint for resume download tracking"""
    try:
        # Log resume download
        # You can add tracking logic here
        return jsonify({
            'success': True,
            'message': 'Resume download initiated'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
