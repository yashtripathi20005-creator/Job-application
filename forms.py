from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, URL

class ApplicationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    job_title = StringField('Job Title', validators=[DataRequired()])
    job_description = TextAreaField('Job Description')
    status = SelectField('Status', choices=[
        ('Applied', 'Applied'),
        ('Phone Screen', 'Phone Screen'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Interview Completed', 'Interview Completed'),
        ('Offer Received', 'Offer Received'),
        ('Offer Accepted', 'Offer Accepted'),
        ('Offer Declined', 'Offer Declined'),
        ('Rejected', 'Rejected'),
        ('Withdrawn', 'Withdrawn')
    ])
    contact_name = StringField('Contact Name')
    contact_email = StringField('Contact Email', validators=[Optional(), Email()])
    contact_phone = StringField('Contact Phone')
    salary_expectation = StringField('Salary Expectation')
    notes = TextAreaField('Notes')
    application_url = StringField('Application URL', validators=[Optional(), URL()])
    location = StringField('Location')
    resume_version = StringField('Resume Version')
    follow_up_date = DateTimeField('Follow-up Date', format='%Y-%m-%d %H:%M', validators=[Optional()])
    submit = SubmitField('Save Application')
