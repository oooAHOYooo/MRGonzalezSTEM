# Barnum STEM Portfolio - Site Map

## 🌐 Public Pages (No Login Required)

### Homepage
- **URL**: `/`
- **Template**: `index.html`
- **Description**: Public homepage showcasing featured projects, stats, and upcoming events
- **Features**:
  - Hero section with program overview
  - Featured projects carousel
  - Recent projects grid
  - Statistics dashboard
  - Upcoming expo information
  - Call-to-action sections

### Project Showcase
- **URL**: `/showcase`
- **Template**: `showcase.html`
- **Description**: Public gallery of student projects organized by quarter
- **Features**:
  - Quarter-based navigation (Q1-Q4)
  - Project cards with descriptions
  - Skills and learning goals display
  - External project links
  - Search and filter functionality

### Curriculum Overview
- **URL**: `/curriculum`
- **Template**: `curriculum.html`
- **Description**: Detailed curriculum information and learning progression
- **Features**:
  - Quarter-by-quarter breakdown
  - Learning objectives and skills
  - Timeline visualization
  - Assessment information
  - Standards alignment

### About Page
- **URL**: `/about`
- **Template**: `about.html`
- **Description**: Information about the program and teaching team
- **Features**:
  - Mission statement
  - Educational philosophy
  - Teacher spotlight
  - Program highlights
  - Impact statistics

## 🔐 Authentication

### Login Page
- **URL**: `/login`
- **Template**: `login.html`
- **Description**: User authentication portal
- **Features**:
  - Username/password login
  - Demo credentials display
  - Role-based redirects
  - Error handling

### Logout
- **URL**: `/logout`
- **Description**: User logout and session cleanup

## 👨‍🎓 Student Dashboard

### Student Dashboard
- **URL**: `/student-dashboard`
- **Template**: `student_dashboard.html`
- **Access**: Students only
- **Features**:
  - Progress overview statistics
  - Personal project gallery
  - Learning progress tracking
  - Quick actions menu
  - Achievement badges
  - Grade level information

### Create Project
- **URL**: `/create-project`
- **Template**: `create_project.html`
- **Access**: All authenticated users
- **Features**:
  - Project information form
  - Quarter and type selection
  - Link management (Tinkercad, Scratch, etc.)
  - Learning details capture
  - Sharing settings
  - Project idea suggestions

## 👨‍🏫 Teacher Dashboard

### Teacher Dashboard
- **URL**: `/teacher-dashboard`
- **Template**: `teacher_dashboard.html`
- **Access**: Teachers and admins only
- **Features**:
  - Overview statistics
  - Class performance summary
  - Recent activity feed
  - Quick actions menu
  - Recent projects display

### Class Management
- **URL**: `/manage-classes`
- **Template**: `manage_classes.html`
- **Access**: Teachers and admins only
- **Features**:
  - Class listing with statistics
  - Class creation and editing
  - Tinkercad integration
  - Class performance metrics

### Create Class
- **URL**: `/create-class`
- **Template**: `create_class.html`
- **Access**: Teachers and admins only
- **Features**:
  - Class information form
  - Grade level selection
  - Tinkercad classroom setup
  - Description and goals

### Lesson Management
- **URL**: `/manage-lessons`
- **Template**: `manage_lessons.html`
- **Access**: Teachers and admins only
- **Features**:
  - Lesson plan listing
  - Lesson creation and editing
  - Subject area organization
  - Difficulty level tracking

### Create Lesson
- **URL**: `/create-lesson`
- **Template**: `create_lesson.html`
- **Access**: Teachers and admins only
- **Features**:
  - Comprehensive lesson form
  - Learning objectives
  - Materials and content
  - Assessment methods
  - Standards alignment

### Student Progress
- **URL**: `/student-progress`
- **Template**: `student_progress.html`
- **Access**: Teachers and admins only
- **Features**:
  - Individual student tracking
  - Progress statistics
  - Completion percentages
  - Recent activity monitoring
  - Performance insights

## 🔌 API Endpoints

### Progress Management
- **URL**: `/api/update-progress`
- **Method**: POST
- **Access**: Teachers and admins only
- **Purpose**: Update student progress data
- **Parameters**:
  - `student_id`: Student identifier
  - `lesson_id`: Lesson identifier
  - `class_id`: Class identifier
  - `status`: Progress status
  - `completion_percentage`: Completion percentage
  - `skill_demonstration`: Skill level
  - `notes`: Teacher notes
  - `teacher_feedback`: Feedback text
  - `shared_publicly`: Public sharing flag

### Project Management
- **URL**: `/api/featured-project/<int:project_id>`
- **Method**: POST
- **Access**: Teachers and admins only
- **Purpose**: Toggle project featured status
- **Response**: Success status and new featured state

## 📁 Static Assets

### CSS Files
- **Path**: `/static/css/custom.css`
- **Purpose**: Custom styling and animations
- **Features**:
  - Responsive design
  - Gradient backgrounds
  - Card animations
  - Timeline styling
  - Form enhancements

### JavaScript Files
- **Path**: `/static/js/dashboard.js`
- **Purpose**: Interactive functionality
- **Features**:
  - Form validation
  - API communication
  - Progress animations
  - Notification system
  - Search functionality

### Upload Directory
- **Path**: `/static/uploads/`
- **Purpose**: User-uploaded files
- **Features**:
  - Project images
  - Video files
  - Document attachments

## 🗄️ Database Models

### User Management
- **User**: Student and teacher accounts
- **STEMClass**: Class information and settings
- **StudentProgress**: Individual progress tracking

### Content Management
- **LessonPlan**: Curriculum and lesson details
- **Project**: Student project submissions
- **Expo**: Quarterly showcase events
- **TeacherReflection**: Teaching reflections and notes

## 🔒 Access Control

### Public Access
- Homepage, showcase, curriculum, about pages
- No authentication required
- Read-only access to public projects

### Student Access
- Personal dashboard and projects
- Project creation and editing
- Progress viewing (own data only)

### Teacher Access
- All student features
- Class and lesson management
- Student progress monitoring
- Project featuring and moderation

### Admin Access
- All teacher features
- User management
- System configuration
- Data export and backup

## 📱 Responsive Design

### Mobile Optimization
- Bootstrap 5 responsive framework
- Touch-friendly navigation
- Optimized card layouts
- Collapsible content sections

### Tablet Support
- Medium screen optimizations
- Grid layout adjustments
- Touch interface enhancements

### Desktop Experience
- Full feature set
- Multi-column layouts
- Advanced interactions
- Keyboard shortcuts

## 🎨 Design System

### Color Palette
- **Primary**: Blue (#007bff)
- **Success**: Green (#28a745)
- **Info**: Cyan (#17a2b8)
- **Warning**: Yellow (#ffc107)
- **Danger**: Red (#dc3545)

### Typography
- **Font Family**: Inter, system fonts
- **Headings**: Bold weights, large sizes
- **Body**: Regular weight, readable sizes
- **Code**: Monospace for technical content

### Components
- **Cards**: Rounded corners, subtle shadows
- **Buttons**: Gradient backgrounds, hover effects
- **Forms**: Clean inputs, validation states
- **Navigation**: Sticky header, dropdown menus

## 🚀 Performance Features

### Loading Optimization
- Lazy loading for images
- Progressive enhancement
- Minimal JavaScript dependencies
- CSS animations for feedback

### Caching Strategy
- Static asset caching
- Database query optimization
- Session management
- CDN integration ready

---

This sitemap provides a comprehensive overview of the Barnum STEM Portfolio application structure, helping users understand the complete navigation and functionality available.
