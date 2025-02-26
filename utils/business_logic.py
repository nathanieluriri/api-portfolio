from dotenv import load_dotenv
import os
import pprint
import re
import pymongo
import json
MONGO_URI = os.getenv("MONGO_URI")
from bson.objectid import ObjectId


def get_all_databases():
    """
    Retrieves a list of portfolio databases 

    Returns:
        list: names of portfolio databases 
    """
    list_of_portfolios=[]
    with pymongo.MongoClient(MONGO_URI) as cli:
        databases = cli.list_database_names()
        for db in databases:
            if "portfolio" in db:
                list_of_portfolios.append(db)
    return list_of_portfolios
    
    
def get_all_projects_func(DB):
    """
    Retrieves all projects from the specified MongoDB database.

    Args:
        DB (str): The name of the database.
                  Must be one of: ('backend_dev_portfolio', 'machine_learning_portfolio', 
                                  'mobile_dev_portfolio', 'ui_ux_portfolio', 'web_design_portfolio')

    Returns:
        list: A list of project documents retrieved from the database.
              Each project is represented as a dictionary.
    """
    cleaned_data = []
    with pymongo.MongoClient(MONGO_URI) as cli:
        db = cli[DB]
        project_collection = db.project
        project_list =[str(projectlist) for projectlist in project_collection.find()]
        for item in project_list:
            # Replace ObjectId with just the string value
            item = re.sub(r"ObjectId\('([a-f0-9]{24})'\)", r'"\1"', item)
            
            # Replace single quotes with double quotes
            item = item.replace("'", '"')
            item = item.replace('\"s', "'s")
            cleaned_data.append(item)
        
        return cleaned_data 
      

def create_project_func(**kwargs):
    """
    Creates a new project entry in the specified MongoDB database.

    Args:
        DB (str): The name of the database. 
                  Must be one of: ('backend_dev_portfolio', 'machine_learning_portfolio', 
                                  'mobile_dev_portfolio', 'ui_ux_portfolio', 'web_design_portfolio')
        project (dict): A dictionary containing project details with the following structure:
            - name (str): The name of the project.
            - description (str): A brief description of the project.
            - case_study_image_link (str): URL to an image related to the project.
            - case_study_link (str): URL to the project's case study.

    Returns:
        dict: A dictionary containing the newly created project's ID:
            - project_id (str): The MongoDB ObjectId of the inserted project.
    """
    with pymongo.MongoClient(MONGO_URI) as cli:
        db = cli[kwargs["DB"]]
        project_collection = db.project
        
        project_data = kwargs.get("project")
        if not project_data:
            raise ValueError("Missing required argument: 'project'")

        new_document_id = project_collection.insert_one(project_data).inserted_id
        return {"project_id": str(new_document_id)}  # Convert ObjectId to string for JSON compatibility

def update_project_func(**kwargs):
    """
    Updates a single project entry in the specified MongoDB database.

    Args:
        DB (str): The name of the database. 
                  Must be one of: ('backend_dev_portfolio', 'machine_learning_portfolio', 
                                  'mobile_dev_portfolio', 'ui_ux_portfolio', 'web_design_portfolio')
        project_id (str): The id of the document to be updated. 
        
        update_fields (dict): A dictionary containing the project fields to be updated:
            - name (str): The name of the project.
            - description (str): A brief description of the project.
            - case_study_image_link (str): URL to an image related to the project.
            - case_study_link (str): URL to the project's case study.

    Returns:
        dict: A dictionary containing the number of Modified fields:
            - project_id (str): The MongoDB ObjectId of the updated project.
    """ 
    try:
        _filter= {"_id":ObjectId(kwargs['project_id'])}
    except Exception:
            return {"error":"object Id exception"}
    
    with pymongo.MongoClient(MONGO_URI) as cli:
        db = cli[kwargs["DB"]]
        project_collection = db.project
        acknowledged=project_collection.update_one(filter=_filter,update={"$set":kwargs["update_fields"]}).modified_count
        return {"Affected":acknowledged}


def get_particular_project_func(DB, projectId: str):
    """
    Retrieves a specific project from the MongoDB database by its ID.

    Args:
        DB (str): The name of the database.
                  Must be one of: ('backend_dev_portfolio', 'machine_learning_portfolio', 
                                  'mobile_dev_portfolio', 'ui_ux_portfolio', 'web_design_portfolio')
        projectId (str): The ID of the project to retrieve (MongoDB ObjectId as a string).

    Returns:
        dict | None: The project document if found, otherwise None.
    """
    with pymongo.MongoClient(MONGO_URI) as cli:
        db = cli[DB]
        project_collection = db.project

        try:
            object_id = ObjectId(projectId)  # Convert string to ObjectId
        except Exception:
            return {"error":"object Id exception"}

        project = project_collection.find_one({'_id': object_id})
        cleaned_data =[]
        s = {}
        
        print(type(project))
        for item in project:
            # Replace ObjectId with just the string value
            item = re.sub(r"ObjectId\('([a-f0-9]{24})'\)", r'"\1"', item)
            
            # Replace single quotes with double quotes
            item = item.replace("'", '"')
            item = item.replace('\"s', "'s")
            cleaned_data.append(str(project.get(item)))
        
        return cleaned_data 


def delete_project_func(DB,projectId:str):
    try:
        object_id = ObjectId(projectId) 
    except:
        return {"error":"object Id exception"}
    _filter = {"_id":object_id}
    
    with pymongo.MongoClient(MONGO_URI) as cli:
        db = cli[DB]
        project_collection = db.project
        delete_count = project_collection.delete_one(filter=_filter).deleted_count
        return {"Affected":delete_count}    

    
    



