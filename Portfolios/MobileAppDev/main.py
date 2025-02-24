from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware

mobile_dev_app = FastAPI(docs_url=None,redoc_url=None)
origins=[
    "https://localhost:8000"
]
mobile_dev_app.add_middleware(
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


@mobile_dev_app.get('/get/projects',tags=['Get Projects'])
def get_projects():
    """
    returns a list of projects for this app
    """

    return {"project"}


@mobile_dev_app.get('/get/project/{projectId}',tags=['Get Projects'])
def get_project(projectId):
    """
    returns a project Object using the project id 
    """

    return {"project":projectId}



@mobile_dev_app.patch("/update/project/{projectId}",tags=['Update Projects'])
def update_project_details(projectId:int, project: Project):
    """
    using the projectId it updates a specific project 

    """
    # this specifies which field should be edited 
    updated_fields = project.model_dump(exclude_unset=True)

    return {"updated project":projectId,"project":updated_fields}


@mobile_dev_app.post("/create/project",tags=['Create Projects'])
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

    return {"created project":project}





@mobile_dev_app.delete("/delete/project/{projectid}",tags=['Delete Projects'])
def delete_project( projectid:int):
    """
    Delets a particular  project
    """
    # this specifies which field should be edited 
    
    return {"deleted project":projectid}


@mobile_dev_app.delete("/delete/projects",tags=['Delete Projects'])
def delete_projects( ):
    """
    Delets all projects 
    """
    # this specifies which field should be edited 
    
    return {"deleted project"}


