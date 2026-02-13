"""OAuth account linkage model."""

from datetime import datetime
from models import db


class OAuthAccount(db.Model):
    __tablename__ = "oauth_accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    provider = db.Column(db.String(50), nullable=False)
    provider_user_id = db.Column(db.String(255), nullable=False)
    provider_email = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("provider", "provider_user_id", name="uq_oauth_provider_user"),
    )

    def __repr__(self):
        return f"<OAuthAccount {self.provider}:{self.provider_user_id}>"
