# Barnum STEM Portfolio - Deployment Instructions

## 🚀 Quick Start Guide

This Flask application is designed to be deployed on Render.com with a PostgreSQL database. Follow these steps to get your STEM portfolio site live!

## Prerequisites

- GitHub account
- Render.com account (free tier available)
- Basic understanding of web development

## Step 1: Prepare Your Code

1. **Fork or clone this repository** to your GitHub account
2. **Ensure all files are committed** to your repository
3. **Verify the file structure** matches the expected layout:

```
barnum-stem-portfolio/
├── app.py
├── requirements.txt
├── render.yaml
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── showcase.html
│   ├── curriculum.html
│   ├── about.html
│   ├── login.html
│   ├── teacher_dashboard.html
│   ├── student_dashboard.html
│   ├── manage_classes.html
│   ├── create_class.html
│   ├── manage_lessons.html
│   ├── create_lesson.html
│   ├── create_project.html
│   └── student_progress.html
└── static/
    ├── css/
    │   └── custom.css
    ├── js/
    │   └── dashboard.js
    └── uploads/
```

## Step 2: Deploy to Render

### 2.1 Create a New Web Service

1. Go to [Render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your `barnum-stem-portfolio` repository

### 2.2 Configure the Service

Render will auto-detect the `render.yaml` configuration, but verify these settings:

- **Name**: `barnum-stem-portfolio`
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  flask db upgrade
  ```
- **Start Command**: 
  ```bash
  gunicorn app:app
  ```

### 2.3 Environment Variables

Render will automatically set these from `render.yaml`:
- `FLASK_APP=app.py`
- `FLASK_ENV=production`
- `SECRET_KEY` (auto-generated)
- `DATABASE_URL` (from the database service)

### 2.4 Create the Database

1. In your Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Name it: `barnum-stem-db`
3. Select the **Free** plan
4. Click **"Create Database"**
5. Copy the **External Database URL** for later use

## Step 3: Deploy and Test

### 3.1 Deploy the Application

1. Click **"Create Web Service"** in Render
2. Wait for the build to complete (5-10 minutes)
3. Your app will be available at: `https://barnum-stem-portfolio.onrender.com`

### 3.2 Test the Application

1. **Visit your live site** and verify it loads
2. **Test the login** with demo credentials:
   - Teacher: `teacher` / `password123`
   - Student: `emma_k` / `student123`
3. **Check all pages** load correctly
4. **Test project creation** functionality

## Step 4: Post-Deployment Setup

### 4.1 Change Default Passwords

**IMPORTANT**: Change the default passwords immediately!

1. Log in as teacher (`teacher` / `password123`)
2. Go to Teacher Dashboard
3. Update user passwords through the admin interface
4. Create new student accounts with secure passwords

### 4.2 Add Real Content

1. **Create your classes** using the "Manage Classes" section
2. **Add lesson plans** for each quarter
3. **Create sample projects** to showcase the platform
4. **Update the About page** with your information

### 4.3 Customize the Branding

1. **Update the site title** in `templates/base.html`
2. **Modify colors** in `static/css/custom.css`
3. **Add your school logo** to the navigation
4. **Update contact information** in the About page

## Step 5: Share with Students and Parents

### 5.1 Student Access

1. Create student accounts for each student
2. Share login credentials with students
3. Provide the public URL for parents to view projects

### 5.2 Parent Access

1. Share the public showcase URL
2. Parents can view all public projects without logging in
3. Consider creating a parent newsletter with project highlights

## 🔧 Troubleshooting

### Common Issues

**Build Fails**
- Check that all files are committed to GitHub
- Verify `requirements.txt` has all dependencies
- Check Render build logs for specific errors

**Database Connection Issues**
- Ensure the database service is running
- Verify `DATABASE_URL` environment variable is set
- Check database credentials in Render dashboard

**App Crashes on Startup**
- Check the application logs in Render
- Verify all environment variables are set
- Ensure the database is accessible

**Static Files Not Loading**
- Check that the `static/` directory is included
- Verify file paths in templates are correct
- Clear browser cache

### Getting Help

1. **Check Render logs** in your dashboard
2. **Review the application logs** for error messages
3. **Test locally** using the same environment variables
4. **Contact support** if issues persist

## 📊 Monitoring and Maintenance

### Regular Tasks

1. **Monitor student progress** through the teacher dashboard
2. **Backup the database** regularly (Render provides automatic backups)
3. **Update dependencies** periodically for security
4. **Review and feature student projects** regularly

### Scaling Considerations

- **Free tier limits**: 750 hours/month, 512MB RAM
- **Upgrade to paid** for more resources if needed
- **Database backups** are automatic on paid plans
- **Custom domains** available on paid plans

## 🎉 Success!

Your Barnum STEM Portfolio is now live! Students can:

- ✅ Create and showcase their projects
- ✅ Track their learning progress
- ✅ View the curriculum and upcoming events
- ✅ Share their work with parents and the community

Teachers can:

- ✅ Manage classes and lesson plans
- ✅ Track student progress
- ✅ Feature outstanding projects
- ✅ Organize quarterly showcases

Parents can:

- ✅ View the public showcase
- ✅ See their child's amazing work
- ✅ Learn about the STEM curriculum
- ✅ Stay informed about school events

## 🔗 Useful Links

- **Render Dashboard**: https://dashboard.render.com
- **Your Live Site**: https://barnum-stem-portfolio.onrender.com
- **GitHub Repository**: [Your repo URL]
- **Documentation**: This file

---

**Need help?** Check the troubleshooting section above or review the application logs in your Render dashboard.
