import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from functools import wraps
import json

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///barnum_stem.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Handle PostgreSQL URL format for render
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student')  # teacher, student, parent, admin
    
    # Personal info
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Student-specific fields
    grade_level = db.Column(db.String(20))
    parent_email = db.Column(db.String(120))
    tinkercad_username = db.Column(db.String(100))
    
    # Relationships
    student_progress = db.relationship('StudentProgress', backref='student', lazy=True, cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='creator', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class STEMClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False)
    teacher_first_name = db.Column(db.String(50), nullable=False)
    grade_level = db.Column(db.String(20), nullable=False)
    tinkercad_class_link = db.Column(db.String(300))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lesson_plans = db.relationship('LessonPlan', backref='stem_class', lazy=True, cascade='all, delete-orphan')
    student_progress = db.relationship('StudentProgress', backref='stem_class', lazy=True)
    
    def __repr__(self):
        return f'<STEMClass {self.class_name}>'

class LessonPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('stem_class.id'), nullable=False)
    
    # Lesson details
    subject_area = db.Column(db.String(50))  # Engineering, Science, Technology, Math, Art
    quarter = db.Column(db.String(10))  # Q1, Q2, Q3, Q4
    duration_minutes = db.Column(db.Integer)
    learning_objectives = db.Column(db.Text)
    materials_needed = db.Column(db.Text)
    lesson_content = db.Column(db.Text)
    assessment_method = db.Column(db.Text)
    standards_alignment = db.Column(db.Text)
    difficulty_level = db.Column(db.String(20))  # Beginner, Intermediate, Advanced
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student_progress = db.relationship('StudentProgress', backref='lesson_plan', lazy=True)
    
    def __repr__(self):
        return f'<LessonPlan {self.title}>'

class StudentProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson_plan.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('stem_class.id'), nullable=False)
    
    # Progress tracking
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed, needs_help
    completion_percentage = db.Column(db.Integer, default=0)
    time_spent_minutes = db.Column(db.Integer, default=0)
    
    # Assessment
    skill_demonstration = db.Column(db.String(20))  # emerging, developing, proficient, advanced
    notes = db.Column(db.Text)
    teacher_feedback = db.Column(db.Text)
    
    # Sharing settings
    shared_publicly = db.Column(db.Boolean, default=False)
    showcase_ready = db.Column(db.Boolean, default=False)
    
    # Timestamps
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<StudentProgress {self.student.first_name} - {self.lesson_plan.title}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Project details
    project_type = db.Column(db.String(50))  # Tinkercad, Scratch, Unreal Engine, Robotics
    quarter = db.Column(db.String(10))  # Q1, Q2, Q3, Q4
    
    # Links and media
    tinkercad_link = db.Column(db.String(500))
    scratch_link = db.Column(db.String(500))
    project_url = db.Column(db.String(500))
    image_path = db.Column(db.String(300))
    video_path = db.Column(db.String(300))
    
    # Metadata
    grade_level = db.Column(db.String(20))
    subject_areas = db.Column(db.String(200))  # comma-separated
    skills_used = db.Column(db.Text)
    learning_goals_met = db.Column(db.Text)
    
    # Sharing settings
    is_public = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    expo_ready = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Project {self.title}>'

class Expo(db.Model):
    """Track the quarterly expos"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    quarter = db.Column(db.String(10), nullable=False)  # Q1, Q2, Q3, Q4
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    
    # Expo details
    focus_area = db.Column(db.String(100))  # 3D Design, Game Development, etc.
    location = db.Column(db.String(200))
    attendee_count = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TeacherReflection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson_plan.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('stem_class.id'))
    
    # Reflection content
    reflection_content = db.Column(db.Text, nullable=False)
    what_worked_well = db.Column(db.Text)
    challenges_faced = db.Column(db.Text)
    modifications_needed = db.Column(db.Text)
    student_engagement_level = db.Column(db.Integer)  # 1-5 scale
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Decorators
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['teacher', 'admin']:
            flash('Teacher access required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Public homepage showcasing student work"""
    featured_projects = Project.query.filter_by(is_featured=True, is_public=True).limit(6).all()
    recent_projects = Project.query.filter_by(is_public=True).order_by(Project.created_at.desc()).limit(8).all()
    
    # Calculate stats
    stats = {
        'total_students': User.query.filter_by(role='student').count(),
        'total_projects': Project.query.filter_by(is_public=True).count(),
        'active_classes': STEMClass.query.count(),
        'lesson_plans': LessonPlan.query.count()
    }
    
    # Get upcoming expo
    upcoming_expo = Expo.query.filter(Expo.date >= datetime.now().date()).order_by(Expo.date).first()
    
    return render_template('index.html', 
                         featured_projects=featured_projects,
                         recent_projects=recent_projects,
                         stats=stats,
                         upcoming_expo=upcoming_expo)

@app.route('/showcase')
def showcase():
    """Project showcase organized by quarters"""
    # Get projects by quarter
    quarters = {
        'Q1': {'name': '3D Design & Treehouses', 'projects': Project.query.filter_by(quarter='Q1', is_public=True).all()},
        'Q2': {'name': 'Game Development', 'projects': Project.query.filter_by(quarter='Q2', is_public=True).all()},
        'Q3': {'name': 'Unreal Engine', 'projects': Project.query.filter_by(quarter='Q3', is_public=True).all()},
        'Q4': {'name': 'Robotics', 'projects': Project.query.filter_by(quarter='Q4', is_public=True).all()}
    }
    
    return render_template('showcase.html', quarters=quarters)

@app.route('/curriculum')
def curriculum():
    """Curriculum overview page"""
    return render_template('curriculum.html')

@app.route('/about')
def about():
    """About the program and teacher"""
    return render_template('about.html')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif user.role == 'teacher' or user.role == 'admin':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# Student routes
@app.route('/student-dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    # Get student's progress and projects
    progress = StudentProgress.query.filter_by(student_id=current_user.id).all()
    projects = Project.query.filter_by(creator_id=current_user.id).all()
    
    # Calculate stats
    completed_lessons = len([p for p in progress if p.status == 'completed'])
    total_lessons = len(progress)
    avg_completion = sum([p.completion_percentage for p in progress]) / len(progress) if progress else 0
    
    return render_template('student_dashboard.html',
                         progress=progress,
                         projects=projects,
                         completed_lessons=completed_lessons,
                         total_lessons=total_lessons,
                         avg_completion=round(avg_completion, 1))

# Teacher routes
@app.route('/teacher-dashboard')
@login_required
@teacher_required
def teacher_dashboard():
    # Overview stats
    total_students = User.query.filter_by(role='student').count()
    total_classes = STEMClass.query.count()
    total_lessons = LessonPlan.query.count()
    total_projects = Project.query.count()
    
    # Recent activity
    recent_progress = StudentProgress.query.order_by(StudentProgress.last_updated.desc()).limit(10).all()
    recent_projects = Project.query.order_by(Project.updated_at.desc()).limit(5).all()
    
    # Class performance summary
    classes = STEMClass.query.all()
    class_performance = []
    
    for cls in classes:
        students_in_class = db.session.query(StudentProgress.student_id).filter_by(class_id=cls.id).distinct().count()
        avg_completion = db.session.query(db.func.avg(StudentProgress.completion_percentage)).filter_by(class_id=cls.id).scalar()
        
        class_performance.append({
            'class': cls,
            'student_count': students_in_class,
            'avg_completion': round(avg_completion or 0, 1)
        })
    
    return render_template('teacher_dashboard.html',
                         total_students=total_students,
                         total_classes=total_classes,
                         total_lessons=total_lessons,
                         total_projects=total_projects,
                         recent_progress=recent_progress,
                         recent_projects=recent_projects,
                         class_performance=class_performance)

@app.route('/manage-classes')
@login_required
@teacher_required
def manage_classes():
    classes = STEMClass.query.all()
    return render_template('manage_classes.html', classes=classes)

@app.route('/create-class', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_class():
    if request.method == 'POST':
        new_class = STEMClass(
            class_name=request.form['class_name'],
            teacher_first_name=request.form['teacher_first_name'],
            grade_level=request.form['grade_level'],
            tinkercad_class_link=request.form.get('tinkercad_class_link', ''),
            description=request.form.get('description', '')
        )
        db.session.add(new_class)
        db.session.commit()
        flash('Class created successfully!', 'success')
        return redirect(url_for('manage_classes'))
    
    return render_template('create_class.html')

@app.route('/manage-lessons')
@login_required
@teacher_required
def manage_lessons():
    lessons = LessonPlan.query.order_by(LessonPlan.created_at.desc()).all()
    return render_template('manage_lessons.html', lessons=lessons)

@app.route('/create-lesson', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_lesson():
    if request.method == 'POST':
        new_lesson = LessonPlan(
            title=request.form['title'],
            class_id=request.form['class_id'],
            subject_area=request.form['subject_area'],
            quarter=request.form.get('quarter', 'Q1'),
            duration_minutes=int(request.form['duration_minutes']),
            learning_objectives=request.form['learning_objectives'],
            materials_needed=request.form['materials_needed'],
            lesson_content=request.form['lesson_content'],
            assessment_method=request.form['assessment_method'],
            standards_alignment=request.form.get('standards_alignment', ''),
            difficulty_level=request.form['difficulty_level']
        )
        db.session.add(new_lesson)
        db.session.commit()
        flash('Lesson plan created successfully!', 'success')
        return redirect(url_for('manage_lessons'))
    
    classes = STEMClass.query.all()
    return render_template('create_lesson.html', classes=classes)

@app.route('/student-progress')
@login_required
@teacher_required
def view_student_progress():
    students = User.query.filter_by(role='student').all()
    progress_data = []
    
    for student in students:
        progress = StudentProgress.query.filter_by(student_id=student.id).all()
        completed = len([p for p in progress if p.status == 'completed'])
        total = len(progress)
        avg_completion = sum([p.completion_percentage for p in progress]) / len(progress) if progress else 0
        
        progress_data.append({
            'student': student,
            'completed_lessons': completed,
            'total_lessons': total,
            'avg_completion': round(avg_completion, 1),
            'recent_activity': progress[-1].last_updated if progress else None
        })
    
    return render_template('student_progress.html', progress_data=progress_data)

@app.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        new_project = Project(
            title=request.form['title'],
            description=request.form['description'],
            creator_id=current_user.id,
            project_type=request.form['project_type'],
            quarter=request.form.get('quarter', 'Q1'),
            tinkercad_link=request.form.get('tinkercad_link', ''),
            scratch_link=request.form.get('scratch_link', ''),
            project_url=request.form.get('project_url', ''),
            grade_level=current_user.grade_level if current_user.role == 'student' else request.form.get('grade_level', ''),
            subject_areas=request.form.get('subject_areas', ''),
            skills_used=request.form.get('skills_used', ''),
            learning_goals_met=request.form.get('learning_goals_met', ''),
            is_public=bool(request.form.get('is_public'))
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('student_dashboard' if current_user.role == 'student' else 'teacher_dashboard'))
    
    return render_template('create_project.html')

# API routes
@app.route('/api/update-progress', methods=['POST'])
@login_required
@teacher_required
def update_progress():
    """API endpoint to update student progress"""
    data = request.get_json()
    
    progress = StudentProgress.query.filter_by(
        student_id=data['student_id'],
        lesson_id=data['lesson_id']
    ).first()
    
    if not progress:
        progress = StudentProgress(
            student_id=data['student_id'],
            lesson_id=data['lesson_id'],
            class_id=data['class_id']
        )
        db.session.add(progress)
    
    # Update fields
    progress.status = data.get('status', progress.status)
    progress.completion_percentage = data.get('completion_percentage', progress.completion_percentage)
    progress.skill_demonstration = data.get('skill_demonstration', progress.skill_demonstration)
    progress.notes = data.get('notes', progress.notes)
    progress.teacher_feedback = data.get('teacher_feedback', progress.teacher_feedback)
    progress.shared_publicly = data.get('shared_publicly', progress.shared_publicly)
    
    if data.get('status') == 'completed' and not progress.completed_at:
        progress.completed_at = datetime.utcnow()
    elif data.get('status') == 'in_progress' and not progress.started_at:
        progress.started_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Progress updated successfully'})

@app.route('/api/featured-project/<int:project_id>', methods=['POST'])
@login_required
@teacher_required
def toggle_featured_project(project_id):
    """Toggle project featured status"""
    project = Project.query.get_or_404(project_id)
    project.is_featured = not project.is_featured
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'featured': project.is_featured,
        'message': f'Project {"featured" if project.is_featured else "unfeatured"} successfully'
    })

# Initialize database and sample data
def create_sample_data():
    """Create sample data for development"""
    # Create admin/teacher user
    admin = User.query.filter_by(username='teacher').first()
    if not admin:
        admin = User(
            username='teacher',
            email='teacher@barnum.edu',
            password_hash=generate_password_hash('password123'),
            role='teacher',
            first_name='STEM',
            last_name='Teacher'
        )
        db.session.add(admin)
    
    # Create sample classes
    if not STEMClass.query.first():
        classes = [
            STEMClass(
                class_name='3rd Grade Digital Designers',
                teacher_first_name='Ms. Johnson',
                grade_level='3rd Grade',
                tinkercad_class_link='https://www.tinkercad.com/classrooms/3rd-grade',
                description='Introduction to 3D design and engineering for 3rd graders'
            ),
            STEMClass(
                class_name='4th Grade Innovation Lab',
                teacher_first_name='Ms. Johnson',
                grade_level='4th Grade',
                tinkercad_class_link='https://www.tinkercad.com/classrooms/4th-grade',
                description='Advanced STEM projects for 4th grade students'
            )
        ]
        for cls in classes:
            db.session.add(cls)
        db.session.flush()
    
    # Create sample students
    if User.query.filter_by(role='student').count() == 0:
        students = [
            {'username': 'emma_k', 'first_name': 'Emma', 'last_name': 'K', 'grade': '3rd Grade'},
            {'username': 'marcus_t', 'first_name': 'Marcus', 'last_name': 'T', 'grade': '4th Grade'},
            {'username': 'sophia_l', 'first_name': 'Sophia', 'last_name': 'L', 'grade': '3rd Grade'},
            {'username': 'jayden_m', 'first_name': 'Jayden', 'last_name': 'M', 'grade': '4th Grade'},
        ]
        
        for student_data in students:
            student = User(
                username=student_data['username'],
                email=f"{student_data['username']}@student.barnum.edu",
                password_hash=generate_password_hash('student123'),
                role='student',
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                grade_level=student_data['grade'],
                tinkercad_username=f"{student_data['username']}_tinkercad"
            )
            db.session.add(student)
    
    # Create sample projects
    if Project.query.count() == 0:
        sample_projects = [
            {
                'title': 'Dream Treehouse Design',
                'description': 'A multi-level treehouse with spiral slide and rope bridge',
                'project_type': 'Tinkercad',
                'quarter': 'Q1',
                'tinkercad_link': 'https://www.tinkercad.com/things/abc123',
                'skills_used': '3D Design, Architecture, Problem Solving',
                'is_public': True,
                'is_featured': True
            },
            {
                'title': 'Space Adventure Quest',
                'description': 'Interactive space exploration game with multiple planets',
                'project_type': 'Scratch',
                'quarter': 'Q2',
                'scratch_link': 'https://scratch.mit.edu/projects/123456/',
                'skills_used': 'Programming Logic, Game Design, Storytelling',
                'is_public': True,
                'is_featured': True
            }
        ]
        
        students = User.query.filter_by(role='student').all()
        for i, project_data in enumerate(sample_projects):
            if students:
                project = Project(
                    creator_id=students[i % len(students)].id,
                    grade_level=students[i % len(students)].grade_level,
                    **project_data
                )
                db.session.add(project)
    
    db.session.commit()
    print("Sample data created successfully!")

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize database
    with app.app_context():
        db.create_all()
        create_sample_data()
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('FLASK_ENV') == 'development', host='0.0.0.0', port=port)
