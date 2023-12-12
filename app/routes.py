from flask import render_template, request, redirect, url_for, flash
from app import app, bcrypt
from app.models import  db, Login, User, Task, Comment
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Login.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = Login.query.filter_by(username=username).first()
        existing_email = Login.query.filter_by(email=email).first()
        if existing_user is None and existing_email is None:
            new_user = Login(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        elif existing_user is not None:
            flash('Username already exists')
        elif existing_email is not None:
            flash('Email already exists')
        else:
            flash('Something went wrong')
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user_filter = request.args.get('user', 'all')
    priority_filter = request.args.get('priority', 'all')

    query = Task.query.join(User, Task.assigned_to == User.id).add_columns(
        Task.id, Task.title, Task.description, Task.status, Task.priority, Task.category, Task.assigned_to, Task.due_date, 
        User.username.label('assigned_username')
    )

    if user_filter != 'all':
        query = query.filter(Task.assigned_to == user_filter)
    if priority_filter != 'all':
        query = query.filter(Task.priority == priority_filter)

    tasks = query.all()
    users = User.query.all()
    #get the username for user_filter if it is not all, else set it to all
    if user_filter != 'all':
        user = User.query.get_or_404(user_filter).username
    else:
        user = 'all'
    return render_template('dashboard.html', tasks=tasks, users=users,user_filter=user, priority_filter=priority_filter)


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already in use.', 'danger')
            return redirect(url_for('create_user'))

        # Create new user
        new_user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()

        flash('User created successfully!', 'success')
        return redirect(url_for('users'))

    return render_template('create_user.html')


@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except SQLAlchemyError as e:
        flash('Error deleting user!', 'danger')
    return redirect(url_for('users'))


@app.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    users = User.query.all()

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        priority = request.form.get('priority')
        category = request.form.get('category')
        assigned_to = request.form.get('assignedTo')
        due_date = request.form.get('dueDate')
        created_by = request.form.get('createdBy')
        new_task = Task(
            title=title, description=description, status=status, priority=priority, 
            category=category, assigned_to=assigned_to, created_by=created_by,
            due_date=due_date
        )
        db.session.add(new_task)
        db.session.commit()

        flash('Task created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_task.html', users=users)


@app.route('/task_details/<int:task_id>')
@login_required
def task_details(task_id):
    query = Task.query.join(User, Task.assigned_to == User.id).add_columns(
        Task.id, Task.title, Task.description, Task.status, Task.priority, Task.category, Task.assigned_to, Task.due_date, 
        User.username.label('assigned_username')
    )
    task = query.filter(Task.id == task_id).first()
    comments = Comment.query.filter_by(task_id=task_id).all()
    users = User.query.all()
    return render_template('task_details.html', task=task, comments=comments,users=users)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    users = User.query.all()
    if request.method == 'POST':
        try:
            task.title = request.form.get('title')
            task.description = request.form.get('description')
            task.priority = request.form.get('priority')
            task.category = request.form.get('category')
            task.assigned_to = request.form.get('assignedTo')
            db.session.commit()
            flash('Task updated successfully!', 'success')
        except SQLAlchemyError as e:
            flash('Error updating task!', 'danger')
        return redirect(url_for('task_details', task_id=task_id))
    return render_template('edit_task.html', task=task, users=users)


@app.route('/add_comment/<int:task_id>', methods=['POST'])
@login_required
def add_comment(task_id):
    comment_text = request.form.get('comment')
    user_id = request.form.get('user_id')
    new_comment = Comment(task_id=task_id, comment_text=comment_text, user_id=user_id, created_at=datetime.now())
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('task_details', task_id=task_id))


@app.route('/delete_comment/<int:comment_id>', methods=['POST', 'GET'])
@login_required
def delete_comment(comment_id):
    try:
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully!', 'success')
    except SQLAlchemyError as e:
        flash('Error deleting comment!', 'danger')
    return redirect(url_for('dashboard'))


@app.route('/delete_task/<int:task_id>', methods=['POST', 'GET'])
@login_required
def delete_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        print(task)
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except SQLAlchemyError as e:
        flash('Error deleting task! Delete Comments First', 'danger')
    return redirect(url_for('dashboard'))
