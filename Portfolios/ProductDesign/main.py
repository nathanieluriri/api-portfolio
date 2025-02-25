import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware
from utils.business_logic import get_all_projects_func ,get_particular_project_func ,update_project_func,create_project_func,delete_project_func
ui_ux_app = FastAPI(redoc_url=None)
origins=[
    "https://localhost:8000"
]
ui_ux_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
class Project(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    case_study_image_link: Optional[str] = None
    case_study_link: Optional[str] = None

DB = "ui_ux_portfolio"

@ui_ux_app.get('/get/projects',tags=['Get Projects'])
def get_projects():
    """
    returns a list of projects for this app
    """
    try:
        projects = get_all_projects_func(DB=DB)
    except:
        raise HTTPException(status_code=500,detail=f"Couldn't get a projects") 
    if json.dumps(projects) =='None':
        raise HTTPException(status_code=404,detail="There isn't a project with that project id in the database")
    print(json.dumps(projects))
    return {"projects":json.dumps(projects)}


@ui_ux_app.get('/get/project/{projectId}',tags=['Get Projects'])
def get_project(projectId:str):
    """
    returns a project Object using the project id 
    """
    try:
       project= get_particular_project_func(DB=DB,projectId=projectId)
    except:
        raise HTTPException(status_code=500,detail=f"Couldn't get a particular project with projectid {projectId}") 
    
    if project =='None':
        raise HTTPException(status_code=404,detail="There isn't a project with that project id in the database")
    return {"project":project}



@ui_ux_app.patch("/update/project/{projectId}",tags=['Update Projects'])
def update_project_details(projectId:str, project: Project):
    """
    using the projectId it updates a specific project 

    """
    # this specifies which field should be edited 
    updated_fields = project.model_dump(exclude_unset=True)
    try:
        count = update_project_func(DB=DB,project_id=projectId,update_fields=updated_fields)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    if count["Affected"]==0:
        raise HTTPException(status_code=404,detail="There isn't a project with that project id in the database")

    return {"updated project":projectId,"project":updated_fields, "count":count}


@ui_ux_app.post("/create/project",tags=['Create Projects'])
def create_project( project: Project):
    """
    Creates a new project
    """
    # this specifies which field should be edited 
    if project.case_study_image_link==None or project.case_study_link==None or project.description==None or project.name==None:
        parsed_project = project.model_dump()
        missing_fields = {key: value for key, value in parsed_project.items() if value is None}
        missing_keys= [keys for keys in missing_fields.keys()]        
        raise HTTPException(status_code=422,detail=f"Didn't find these fields in request body: {missing_keys}")
    else:
        result = create_project_func(DB=DB,project=project.model_dump())
    return {"created project":result}





@ui_ux_app.delete("/delete/project/{projectid}",tags=['Delete Projects'])
def delete_project( projectid:str):
    """
    Delets a particular  project
    """
    # this specifies which field should be edited 
    try:
        count =delete_project_func(DB=DB,projectId=projectid)
    except Exception as e:
        raise HTTPException(status_code=500 ,detail=f"failed to delete because {e}")
        
    if count["Affected"]==0:
        raise HTTPException(status_code=404,detail="There isn't a project with that project id in the database")
    return count


@ui_ux_app.delete("/delete/projects",tags=['Delete Projects'])
def delete_projects( ):
    """
    Delets all projects 
    """
    # this specifies which field should be edited 
    
    return {"deleted project"}


