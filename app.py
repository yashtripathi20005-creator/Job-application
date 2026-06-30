from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from models import db, Application
from forms import ApplicationForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Get filter parameters
    status_filter = request.args.get('status', '')
    search_query = request.args.get('search', '')
    
    query = Application.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if search_query:
        query = query.filter(
            db.or_(
                Application.company_name.contains(search_query),
                Application.job_title.contains(search_query),
                Application.location.contains(search_query)
            )
        )
    
    applications = query.order_by(Application.application_date.desc()).all()
    
    # Get status counts for dashboard
    status_counts = {}
    for app in Application.query.all():
        status_counts[app.status] = status_counts.get(app.status, 0) + 1
    
    return render_template('index.html', 
                         applications=applications, 
                         status_counts=status_counts,
                         status_filter=status_filter,
                         search_query=search_query)

@app.route('/application/add', methods=['GET', 'POST'])
def add_application():
    form = ApplicationForm()
    
    if form.validate_on_submit():
        application = Application(
            company_name=form.company_name.data,
            job_title=form.job_title.data,
            job_description=form.job_description.data,
            status=form.status.data,
            contact_name=form.contact_name.data,
            contact_email=form.contact_email.data,
            contact_phone=form.contact_phone.data,
            salary_expectation=form.salary_expectation.data,
            notes=form.notes.data,
            application_url=form.application_url.data,
            location=form.location.data,
            resume_version=form.resume_version.data,
            follow_up_date=form.follow_up_date.data,
            application_date=datetime.utcnow()
        )
        
        db.session.add(application)
        db.session.commit()
        
        flash('Application added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_application.html', form=form)

@app.route('/application/<int:id>')
def view_application(id):
    application = Application.query.get_or_404(id)
    return render_template('application_detail.html', application=application)

@app.route('/application/<int:id>/edit', methods=['GET', 'POST'])
def edit_application(id):
    application = Application.query.get_or_404(id)
    form = ApplicationForm(obj=application)
    
    if form.validate_on_submit():
        application.company_name = form.company_name.data
        application.job_title = form.job_title.data
        application.job_description = form.job_description.data
        application.status = form.status.data
        application.contact_name = form.contact_name.data
        application.contact_email = form.contact_email.data
        application.contact_phone = form.contact_phone.data
        application.salary_expectation = form.salary_expectation.data
        application.notes = form.notes.data
        application.application_url = form.application_url.data
        application.location = form.location.data
        application.resume_version = form.resume_version.data
        application.follow_up_date = form.follow_up_date.data
        application.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Application updated successfully!', 'success')
        return redirect(url_for('view_application', id=application.id))
    
    return render_template('edit_application.html', form=form, application=application)

@app.route('/application/<int:id>/delete', methods=['POST'])
def delete_application(id):
    application = Application.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/application/<int:id>/update_status', methods=['POST'])
def update_status(id):
    application = Application.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status:
        application.status = new_status
        application.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Status updated successfully!', 'success')
    
    return redirect(url_for('view_application', id=application.id))

# API endpoints
@app.route('/api/applications')
def api_applications():
    applications = Application.query.all()
    return jsonify([app.to_dict() for app in applications])

@app.route('/api/application/<int:id>')
def api_application(id):
    application = Application.query.get_or_404(id)
    return jsonify(application.to_dict())

@app.route('/api/stats')
def api_stats():
    total = Application.query.count()
    by_status = {}
    for app in Application.query.all():
        by_status[app.status] = by_status.get(app.status, 0) + 1
    
    return jsonify({
        'total': total,
        'by_status': by_status
    })

if __name__ == '__main__':
    app.run(debug=True)
