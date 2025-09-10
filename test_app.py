#!/usr/bin/env python3
"""
Simple test script to verify the Flask application works correctly.
"""

import os
import sys
import tempfile
from app import app, db, create_sample_data

def test_app():
    """Test the Flask application."""
    print("🧪 Testing Barnum STEM Portfolio Application...")
    
    # Set up test database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        try:
            # Create database tables
            print("📊 Creating database tables...")
            db.create_all()
            
            # Create sample data
            print("📝 Creating sample data...")
            create_sample_data()
            
            # Test database queries
            print("🔍 Testing database queries...")
            from app import User, Project, STEMClass, LessonPlan
            
            # Test user queries
            users = User.query.all()
            print(f"✅ Found {len(users)} users")
            
            # Test project queries
            projects = Project.query.all()
            print(f"✅ Found {len(projects)} projects")
            
            # Test class queries
            classes = STEMClass.query.all()
            print(f"✅ Found {len(classes)} classes")
            
            # Test lesson queries
            lessons = LessonPlan.query.all()
            print(f"✅ Found {len(lessons)} lesson plans")
            
            # Test Flask routes
            print("🌐 Testing Flask routes...")
            with app.test_client() as client:
                # Test homepage
                response = client.get('/')
                assert response.status_code == 200
                print("✅ Homepage loads successfully")
                
                # Test showcase
                response = client.get('/showcase')
                assert response.status_code == 200
                print("✅ Showcase page loads successfully")
                
                # Test curriculum
                response = client.get('/curriculum')
                assert response.status_code == 200
                print("✅ Curriculum page loads successfully")
                
                # Test about
                response = client.get('/about')
                assert response.status_code == 200
                print("✅ About page loads successfully")
                
                # Test login
                response = client.get('/login')
                assert response.status_code == 200
                print("✅ Login page loads successfully")
            
            print("\n🎉 All tests passed! The application is working correctly.")
            return True
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = test_app()
    sys.exit(0 if success else 1)
