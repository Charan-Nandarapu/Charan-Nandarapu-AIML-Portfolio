# Charan Nandarapu - AI & ML Engineer Portfolio

[![React](https://img.shields.io/badge/React-19.0-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.1-green.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-3.3.1-brightgreen.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Professional portfolio website showcasing my experience, projects, and skills in Artificial Intelligence and Machine Learning.

## 🌟 Live Demo

**Portfolio URL:** ![Visit Here](https://charann.me/)

## 📋 About

This is a full-stack portfolio application built to showcase my professional journey as an AI & ML Engineer. The website features a modern, technical design with comprehensive sections covering my experience at BNP Paribas, research projects, certifications, and ways to get in touch.

## ✨ Features

### Frontend
- **9 Comprehensive Sections:**
  - 🏠 Hero - Introduction with neural network background
  - 👤 About - Professional summary with key statistics
  - 🛠️ Skills - Technical and soft skills categorized
  - 💼 Experience - Work history at BNP Paribas
  - 🚀 Projects - ActiveBrainNet, Animal Intrusion Detection, Production Automation
  - 🎓 Education - Academic background (B.Tech AI, 9.18 CGPA)
  - 🏆 Certifications - Oracle, NVIDIA, AJNA AI credentials
  - 📝 Articles - Research publications and technical writing
  - 📧 Contact - Working contact form with backend integration

- **Design:**
  - Technical/professional GitHub-inspired aesthetic
  - Black, gray, purple, and violet color scheme
  - Fully responsive across all devices
  - Smooth scrolling navigation
  - Hover effects and micro-animations
  - Accessible Shadcn UI components

- **Special Features:**
  - Beautiful apology pages for private/unavailable content
  - Resume download functionality
  - External links to GitHub, LinkedIn, certifications
  - Project metrics and achievements highlighted

### Backend
- **FastAPI REST API** with async/await support
- **MongoDB Integration** for contact form submissions
- **Health Check Endpoint** for monitoring
- **CRUD Operations** for messages
- **Data Validation** with Pydantic
- **Email Validation** and sanitization
- **Error Handling** and comprehensive logging
- **Indexed Queries** for optimal performance

## 🛠️ Tech Stack

### Frontend
- **Framework:** React 19.0
- **Styling:** Tailwind CSS 3.4
- **UI Components:** Shadcn UI (Radix UI)
- **Routing:** React Router DOM 7.5
- **HTTP Client:** Axios 1.8
- **Icons:** Lucide React
- **Form Handling:** React Hook Form
- **Build Tool:** Craco (Create React App Config Override)

### Backend
- **Framework:** FastAPI 0.110.1
- **Server:** Uvicorn 0.25.0
- **Database Driver:** Motor 3.3.1 (Async MongoDB)
- **Validation:** Pydantic 2.6+
- **Email Validation:** email-validator 2.2+
- **Environment:** python-dotenv 1.0+

### Database
- **Database:** MongoDB
- **Collections:** contact_messages, status_checks
- **Indexes:** id (unique), email, timestamp (desc), status

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ and Yarn
- Python 3.8+
- MongoDB

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Charan-Nandarapu/Charan-Nandarapu-AIML-Portfolio.git
cd Charan-Nandarapu-AIML-Portfolio
```

2. **Frontend Setup**
```bash
cd frontend
yarn install
```

3. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

4. **Environment Configuration**

Create `.env` files:

**Frontend (.env):**
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

**Backend (.env):**
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=portfolio_db
CORS_ORIGINS=*
```

5. **Start MongoDB**
```bash
mongod
```

6. **Run the Application**

**Backend:**
```bash
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Frontend:**
```bash
cd frontend
yarn start
```

Visit: `http://localhost:3000`

## 📁 Project Structure

```
/app
├── frontend/
│   ├── public/
│   │   └── Charan_AI_ML_Engineer.pdf
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/          # Shadcn UI components
│   │   │   ├── Header.js
│   │   │   ├── Hero.js
│   │   │   ├── About.js
│   │   │   ├── Skills.js
│   │   │   ├── Experience.js
│   │   │   ├── Projects.js
│   │   │   ├── Education.js
│   │   │   ├── Certifications.js
│   │   │   ├── Articles.js
│   │   │   ├── Contact.js
│   │   │   └── Footer.js
│   │   ├── pages/
│   │   │   ├── Portfolio.js
│   │   │   ├── ActiveBrainNetUnavailable.js
│   │   │   ├── ProductionAutomationUnavailable.js
│   │   │   └── NvidiaCertUnavailable.js
│   │   ├── data/
│   │   │   └── mock.js      # Portfolio data
│   │   ├── hooks/
│   │   │   └── use-toast.js
│   │   ├── lib/
│   │   │   └── utils.js
│   │   └── App.js
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/
│   ├── models/
│   │   └── contact.py       # Pydantic models
│   ├── routes/
│   │   └── contact.py       # API endpoints
│   ├── server.py            # Main FastAPI app
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

## 🔌 API Endpoints

### Health Check
```http
GET /api/health
```
Response:
```json
{
  "status": "healthy",
  "api": "running",
  "database": "connected",
  "version": "1.0.0"
}
```

### Contact Form
```http
POST /api/contact
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Opportunity",
  "message": "Let's connect!"
}
```

### Get All Messages (Admin)
```http
GET /api/contact?limit=50&skip=0
```

## 🎨 Design Features

- **Color Scheme:** Black (#0a0a0a), Dark Gray (#1a1a1a), Purple (#a855f7), Violet (#7c3aed)
- **Typography:** Space Grotesk (headings), Inter (body), JetBrains Mono (code)
- **Principles:**
  - 90/10 color rule (black backgrounds with purple accents only on buttons/links)
  - High contrast for readability
  - No AI emojis, only Lucide React icons
  - Professional GitHub-inspired aesthetic

## 📊 Key Metrics & Achievements

- **2+ Years** of professional experience
- **3 Major Projects** completed
- **1 Research Paper** (CVIP-2025)
- **3 Professional Certifications**
- **94% Accuracy** on ActiveBrainNet with only 22% labeled data
- **96% Accuracy** on Animal Intrusion Detection
- **30% Efficiency Gain** through production automation

## 🔗 Links

- **GitHub:** [github.com/Charan-Nandarapu](https://github.com/Charan-Nandarapu)
- **LinkedIn:** [linkedin.com/in/charan-nandarapu](https://in.linkedin.com/in/charan-nandarapu)
- **Email:** nandarapucharan065@gmail.com
- **Location:** Chennai, India

## 📜 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Charan Nandarapu**  
AI & ML Engineer | BNP Paribas  
Building intelligent solutions with Machine Learning and Deep Learning

---

⭐ If you find this portfolio interesting, please consider giving it a star!
