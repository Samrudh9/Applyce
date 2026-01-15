from models import db
from werkzeug. security import generate_password_hash, check_password_hash
from datetime import datetime


class Admin(db. Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120))
    role = db.Column(db.String(20), default='admin')  # superadmin, admin, manager, developer, viewer
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db. DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Hash and set password securely"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username} ({self.role})>'


def create_default_admins():
    """
    Create default admin users if they don't exist.
    Call this function during app initialization.
    """
    default_admins = [
        {
            'username': 'dishita',
            'password': 'dishita@097',
            'role': 'Lead/Flask Dev',
            'email': 'dishita@applyce.com'
        },
        {
            'username': 'khyathi',
            'password': 'khyathi@095',
            'role': 'Data Specialist',
            'email': 'khyathi@applyce.com'
        },
        {
            'username': 'samrudh',
            'password': 'samrudh@502',
            'role': 'Developer',
            'email': 'samrudh@applyce.com'
        },
        {
            'username': 'shaabdhik',
            'password':  'shaabdhik@055',
            'role': 'Frontend Dev',
            'email': 'shaabdhik@applyce.com'
        },
        {
            'username': 'sathwik',
            'password': 'sathwik@053',
            'role': 'UI/UX Designer',
            'email': 'sathwik@applyce.com'
        },
    ]
    
    admins_created = 0
    
    for admin_data in default_admins:
        existing = Admin.query.filter_by(username=admin_data['username']).first()
        
        if not existing:
            admin = Admin(
                username=admin_data['username'],
                email=admin_data['email'],
                role=admin_data['role'],
                is_active=True
            )
            admin.set_password(admin_data['password'])
            db.session.add(admin)
            admins_created += 1
            print(f"  ✅ Created admin: {admin_data['username']} ({admin_data['role']})")
        else:
            print(f"  ℹ️ Admin exists: {admin_data['username']}")
    
    if admins_created > 0:
        try:
            db.session.commit()
            print(f"✅ {admins_created} new admin(s) saved to database!")
        except Exception as e:
            db.session. rollback()
            print(f"❌ Error saving admins: {e}")
    else:
        print("ℹ️ All admins already exist in database.")