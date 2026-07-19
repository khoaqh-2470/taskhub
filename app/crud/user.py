from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_profile(db: Session, username: str) -> User | None:
    return (
        db.query(User)
        .options(
            joinedload(User.projects).joinedload(Project.tasks).joinedload(Task.tags),
            joinedload(User.assigned_tasks).joinedload(Task.tags),
        )
        .filter(User.username == username)
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user: UserUpdate) -> User:
    update_data = user.model_dump(exclude_unset=True)
    password = update_data.pop("password", None)
    if password is not None:
        update_data["hashed_password"] = password

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: User) -> None:
    db.delete(db_user)
    db.commit()
