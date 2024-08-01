from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.task import TaskModel
from sqlalchemy.exc import SQLAlchemyError
from schemas import TaskSchema
from flask import jsonify


blp = Blueprint("tasks", __name__, description="Operations on tasks")

@blp.route("/task")
class TaskList(MethodView):
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        tasks = TaskModel.query.all()
        if not tasks:
            return jsonify({"message": "No tasks found"}), 200
        return tasks
    
    @blp.arguments(TaskSchema)
    def post(self, task_data):
        task = TaskModel(**task_data)
        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return {"message": "Task created successfully"}, 201
    
@blp.route("/task/<int:task_id>")
class Task(MethodView):
    @blp.arguments(TaskSchema)
    def put(self, task_data, task_id):
        task = TaskModel.query.get_or_404(task_id)
        if "name" in task_data:
            task.name = task_data.get("name")
        
        db.session.add(task)
        db.session.commit()
        return {"message": "Task updated successfully"}
    
    # @blp.arguments(TaskSchema)
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted successfully"}
       
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        return task
