"""Admin user model for secure admin authentication"""
from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Admin(db. Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db. Column(db.String(256), nullable=False)
    email = db.Column(db.String(120))
    role = db.Column(db.String(20), default='admin')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db. Column(db.DateTime)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

def create_default_admins():
    """Create default admin users if they don't exist"""
    default_admins = [
        {'username': 'dishitha', 'password': 'dishitha@097 ', 'role': 'Lead/Flask Dev', 'email': 'dishitha@applyce.com'},
        {'username':  'khyathi', 'password': 'khyathi@095', 'role':  'Data specialist', 'email':  'khyathi@applyce.com'},
        {'username':  'samrudh', 'password':  'samrudh@502', 'role': 'Developer', 'email': 'samrudh@applyce.com'},
        {'username': 'shaabdhik', 'password': 'shaabdhik@055', 'role': 'Frontend Dev', 'email': 'shaabdhik@applyce.com'},
        {'username': 'sathwik', 'password': 'sathwik@053', 'role': 'UI Designer', 'email': 'sathwik@applyce.com'},
    ]
    
        for admin_data in default_admins: 
        existing = Admin.query. filter_by(username=admin_data['username']).first()
        if not existing:
            admin = Admin(
                username=admin_data['username'],
                email=admin_data['email'],
                role=admin_data['role']
            )
            admin.set_password(admin_data['password'])
            db.session. add(admin)
            print(f"✅ Created admin: {admin_data['username']}")
    
    try:
        db.session.commit()
        print("✅ All admin users saved to database!")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error saving admins: {e}")