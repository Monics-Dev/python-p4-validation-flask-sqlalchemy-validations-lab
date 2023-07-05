from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Author must have a name.')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and len(phone_number) != 10:
            raise ValueError('Phone number must be exactly ten digits.')
        return phone_number

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'

    @validates('title')
    def validate_title(self, key, title):
        required_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        pattern = r"\b(" + "|".join(required_keywords) + r")\b"

        if not re.search(pattern, title):
            raise ValueError('Title must contain clickbait keywords.')

        return title


    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError('Post content must be at least 250 characters long.')
        return content
        
            

    @validates('summary')
    def validate_summary(self, key, summary):
      if summary and len(summary) > 250:
          raise ValueError('Post summary can have a maximum of 250 characters.')
      return summary



    @validates('category')
    def validate_category(self, key, category):
        allowed_categories = ['Fiction', 'Non-Fiction']
        if category not in allowed_categories:
            raise ValueError(f'Post category must be one of {", ".join(allowed_categories)}.')
        return category
