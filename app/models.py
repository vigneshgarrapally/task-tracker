from datetime import datetime
from app import db, app, bcrypt
from flask_login import UserMixin

class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column('UserID', db.Integer, primary_key=True)
    username = db.Column('Username', db.String(50), nullable=False, unique=True)
    email = db.Column('Email', db.String(100), nullable=False, unique=True)
    password = db.Column('Password', db.String(100), nullable=False)
    created_at = db.Column('CreatedAt', db.DateTime, default=datetime.utcnow)

    # Relationships
    tasks_created = db.relationship('Task', backref='creator', lazy=True, foreign_keys='Task.created_by')
    tasks_assigned = db.relationship('Task', backref='assignee', lazy=True, foreign_keys='Task.assigned_to')
    comments = db.relationship('Comment', backref='user', lazy=True)

class Task(db.Model):
    __tablename__ = 'Tasks'

    id = db.Column('TaskID', db.Integer, primary_key=True)
    title = db.Column('Title', db.String(100), nullable=False)
    description = db.Column('Description', db.Text)
    status = db.Column('Status', db.Enum('Pending', 'In Progress', 'Completed'), nullable=False, default='Pending')
    priority = db.Column('Priority', db.Enum('Low', 'Medium', 'High'), nullable=False, default='Medium')
    category = db.Column('Category', db.String(100))
    assigned_to = db.Column('AssignedTo', db.Integer, db.ForeignKey('Users.UserID'))
    created_by = db.Column('CreatedBy', db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    due_date = db.Column('DueDate', db.Date)
    created_at = db.Column('CreatedAt', db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='task', lazy=True)

class Comment(db.Model):
    __tablename__ = 'Comments'

    id = db.Column('CommentID', db.Integer, primary_key=True)
    task_id = db.Column('TaskID', db.Integer, db.ForeignKey('Tasks.TaskID'), nullable=False)
    comment_text = db.Column('Comment', db.Text)
    user_id = db.Column('UserID', db.Integer, db.ForeignKey('Users.UserID'))
    created_at = db.Column('CreatedAt', db.DateTime, default=datetime.utcnow)


class Login(db.Model, UserMixin):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255))
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Login {self.username}>'
    

with app.app_context():
    db.create_all()