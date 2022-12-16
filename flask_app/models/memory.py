from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
from werkzeug.utils import secure_filename
import os
from PIL import Image
import base64
from io import BytesIO
db = "memories"



class Memory:
    db = "memories"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.media = data['media']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def add_memory(cls, data):
        query = """INSERT INTO memories (title, description, media, user_id)
        VALUES (%(title)s, %(description)s, %(media)s, %(user_id)s);"""
        result = connectToMySQL(cls.db).query_db(query,data)
        return result


    @classmethod
    def update_mem(cls,data):
        query = """UPDATE memories SET title=%(title)s, description=%(description)s,
        media=%(media)s
        WHERE id = %(id)s;"""
        result = connectToMySQL('memories').query_db(query, data)
        return result


    @classmethod
    def get_one_memory(cls, data):
        query = """
        SELECT * FROM memories 
        WHERE id = %(id)s;
        """
        results = connectToMySQL('memories').query_db(query, data)
        return cls(results[0])


    @classmethod
    def get_all_memories(cls):
        query = """SELECT * FROM memories;
        """
        results = connectToMySQL('memories').query_db(query)
        all_memories = []
        for memory in results:
            all_memories.append(cls(memory))
        return all_memories

    


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM memories WHERE id= %(id)s;"
        return connectToMySQL('memories').query_db(query,data)


    @staticmethod
    def validate_memory(memory):
        is_valid = True 
        query = """SELECT * FROM memories WHERE user_id = %(user_id)s;"""
        results = connectToMySQL(Memory.db).query_db(query, memory)

        if len(memory['title']) < 3:
            flash("Title is required and must be at least 3 characters long.", "report")
            is_valid = False
        if len(memory['description']) < 1:
            flash("Description is required and must be at least 10 characters long.", "report")
            is_valid = False
        return is_valid