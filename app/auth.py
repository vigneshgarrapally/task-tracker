from app import login_manager
from .models import Login

@login_manager.user_loader
def load_user(user_id):
    return Login.query.get(int(user_id))