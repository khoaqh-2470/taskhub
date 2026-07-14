from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models.project import Project
from app.models.task import Task
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_project(db: Session, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.id == project_id).first()


def get_project_with_tasks(db: Session, project_id: int) -> Project | None:
    return (
        db.query(Project)
        .options(joinedload(Project.tasks).joinedload(Task.tags))
        .filter(Project.id == project_id)
        .first()
    )


def get_projects(db: Session, skip: int = 0, limit: int = 100) -> list[Project]:
    return db.query(Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: ProjectCreate) -> Project:
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, db_project: Project, project: ProjectUpdate) -> Project:
    for field, value in project.model_dump(exclude_unset=True).items():
        setattr(db_project, field, value)

    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, db_project: Project) -> None:
    db.delete(db_project)
    db.commit()
