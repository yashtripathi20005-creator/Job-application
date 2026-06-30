from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Applied')
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    salary_expectation = db.Column(db.String(50))
    notes = db.Column(db.Text)
    application_url = db.Column(db.String(200))
    location = db.Column(db.String(100))
    resume_version = db.Column(db.String(50))
    follow_up_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Application {self.company_name} - {self.job_title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'job_title': self.job_title,
            'job_description': self.job_description,
            'application_date': self.application_date.strftime('%Y-%m-%d %H:%M') if self.application_date else None,
            'status': self.status,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'salary_expectation': self.salary_expectation,
            'notes': self.notes,
            'application_url': self.application_url,
            'location': self.location,
            'resume_version': self.resume_version,
            'follow_up_date': self.follow_up_date.strftime('%Y-%m-%d %H:%M') if self.follow_up_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None
        }
