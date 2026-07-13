from app.schemas.project import ProjectCreate, ProjectUpdate


ProjectRecord = dict[str, object]


def get_project(projects: list[ProjectRecord], project_id: int) -> ProjectRecord | None:
    return next((project for project in projects if project["id"] == project_id), None)


def get_projects(projects: list[ProjectRecord], skip: int = 0, limit: int = 100) -> list[ProjectRecord]:
    return projects[skip : skip + limit]


def create_project(projects: list[ProjectRecord], project: ProjectCreate) -> ProjectRecord:
    next_id = max((int(item["id"]) for item in projects), default=0) + 1
    new_project = {"id": next_id, **project.model_dump()}
    projects.append(new_project)
    return new_project


def update_project(db_project: ProjectRecord, project: ProjectUpdate) -> ProjectRecord:
    for field, value in project.model_dump(exclude_unset=True).items():
        db_project[field] = value

    return db_project


def delete_project(projects: list[ProjectRecord], db_project: ProjectRecord) -> None:
    projects.remove(db_project)
