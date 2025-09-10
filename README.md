# 🚀 Barnum STEM Portfolio

A comprehensive web application for showcasing student STEM projects and tracking learning progress. Built with Flask and designed for educational institutions to highlight student innovation and creativity.

## ✨ Features

### 🎯 For Students
- **Personal Dashboard**: Track learning progress and achievements
- **Project Creation**: Submit and showcase creative projects
- **Progress Tracking**: Monitor completion of lessons and activities
- **Portfolio Building**: Build a digital portfolio of work

### 👨‍🏫 For Teachers
- **Class Management**: Organize students and lesson plans
- **Progress Monitoring**: Track individual and class-wide progress
- **Project Curation**: Feature outstanding student work
- **Assessment Tools**: Evaluate student learning and skills

### 👨‍👩‍👧‍👦 For Parents & Community
- **Public Showcase**: View amazing student projects
- **Curriculum Overview**: Understand learning objectives
- **Progress Visibility**: See student achievements
- **Event Information**: Stay informed about showcases

## 🏗️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Deployment**: Render.com
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (for production)
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/barnum-stem-portfolio.git
   cd barnum-stem-portfolio
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export SECRET_KEY=your-secret-key
   export DATABASE_URL=sqlite:///barnum_stem.db
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open http://localhost:5000 in your browser
   - Login with demo credentials:
     - Teacher: `teacher` / `password123`
     - Student: `emma_k` / `student123`

## 🌐 Deployment

### Render.com Deployment

1. **Fork this repository** to your GitHub account
2. **Connect to Render.com** and create a new Web Service
3. **Configure the service** using the provided `render.yaml`
4. **Create a PostgreSQL database** in Render
5. **Deploy!** Your app will be live at `https://your-app-name.onrender.com`

For detailed deployment instructions, see [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md).

## 📚 Curriculum Structure

The application is designed around a quarterly STEM curriculum:

### Q1: 3D Design & Treehouses
- **Tool**: Tinkercad
- **Focus**: Spatial reasoning, engineering principles
- **Projects**: Architectural models, treehouse designs

### Q2: Game Development
- **Tool**: Scratch
- **Focus**: Programming logic, creative storytelling
- **Projects**: Interactive games, educational applications

### Q3: Unreal Engine
- **Tool**: Unreal Engine
- **Focus**: Advanced 3D environments, interactive experiences
- **Projects**: Immersive worlds, virtual experiences

### Q4: Robotics
- **Tool**: Various robotics platforms
- **Focus**: Physical computing, real-world problem solving
- **Projects**: Automated systems, interactive installations

## 🗂️ Project Structure

```
barnum-stem-portfolio/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── render.yaml                # Render deployment config
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── index.html            # Homepage
│   ├── showcase.html         # Project showcase
│   ├── curriculum.html       # Curriculum overview
│   ├── about.html            # About page
│   ├── login.html            # Authentication
│   ├── teacher_dashboard.html # Teacher interface
│   ├── student_dashboard.html # Student interface
│   └── ...                   # Additional templates
├── static/                   # Static assets
│   ├── css/
│   │   └── custom.css        # Custom styles
│   ├── js/
│   │   └── dashboard.js      # JavaScript functionality
│   └── uploads/              # User uploads
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables

- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: Environment (development/production)
- `UPLOAD_FOLDER`: Path for file uploads

### Database Models

- **User**: Student and teacher accounts
- **STEMClass**: Class information
- **LessonPlan**: Curriculum content
- **Project**: Student submissions
- **StudentProgress**: Learning tracking
- **Expo**: Showcase events

## 🎨 Customization

### Branding
- Update school name and colors in `templates/base.html`
- Modify color scheme in `static/css/custom.css`
- Add school logo to navigation

### Content
- Customize curriculum information
- Update about page with school details
- Modify project categories and requirements

### Features
- Add new project types
- Extend progress tracking
- Integrate additional tools

## 📊 Usage Statistics

Track these key metrics:
- Student engagement and progress
- Project completion rates
- Teacher productivity
- Parent engagement
- Showcase attendance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Bootstrap** for responsive design framework
- **Font Awesome** for icons
- **Flask** community for excellent documentation
- **Render** for hosting platform
- **Students and teachers** who inspire this project

## 📞 Support

- **Documentation**: See [SITEMAP.md](SITEMAP.md) for complete site structure
- **Deployment**: Follow [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md)
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Email**: [your-email@school.edu]

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Basic project showcase
- ✅ Student progress tracking
- ✅ Teacher dashboard
- ✅ Public portfolio

### Phase 2 (Planned)
- 🔄 Parent portal
- 🔄 Mobile app
- 🔄 Advanced analytics
- 🔄 Integration with school systems

### Phase 3 (Future)
- 🔮 AI-powered project recommendations
- 🔮 Virtual reality showcase
- 🔮 Advanced collaboration tools
- 🔮 Multi-language support

---

**Built with ❤️ for STEM education**

*Empowering the next generation of innovators through technology and creativity.*
