from datetime import datetime
from . import db

class Provider(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)   # openai / anthropic / google
    # keys are only in .env – we store nothing secret in DB

    models = db.relationship("LLMModel", backref="provider", lazy=True)

class LLMModel(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    provider_id   = db.Column(db.Integer, db.ForeignKey("provider.id"), nullable=False)
    model_id      = db.Column(db.String(120), nullable=False)      # e.g. gpt-4o
    display_name  = db.Column(db.String(120))
    enabled       = db.Column(db.Boolean, default=False)

class ChatMessage(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow)
    model_id    = db.Column(db.String(120))
    role        = db.Column(db.String(10))     # user / assistant
    content     = db.Column(db.Text)
