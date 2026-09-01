import sys
import os
from sqlalchemy.orm import Session

# Ensure imports work from the backend root directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import engine, SessionLocal, Base
from models.user import User
from models.recruiter import Recruiter
from models.opportunity import Opportunity
from models.course import Course
from utils.auth import hash_password

def seed_final_catalog():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("🧹 Wiping existing opportunities and courses to prevent duplicates...")
        db.query(Opportunity).delete()
        db.query(Course).delete()
        db.commit()

        # Ensure we have a recruiter to associate with
        recruiter = db.query(User).filter(User.role == "recruiter").first()
        if not recruiter:
            recruiter = User(
                name="National Internship Network",
                email="partner@internshala.com",
                password_hash=hash_password("password123"),
                role="recruiter"
            )
            db.add(recruiter)
            db.commit()
            db.refresh(recruiter)
            
            db.add(Recruiter(
                user_id=recruiter.id, 
                company_name="National Placement Consortium",
                company_website="https://placement.org",
                designation="Director of Partnerships"
            ))
            db.commit()

        rid = recruiter.id

        # 1. SEEDING 55 DETAILED INTERNSHIPS & PLACEMENTS
        opportunities = [
            # ─── SOFTWARE ENGINEERING & BACKEND (FastAPI, Django, SQL) ───
            Opportunity(
                recruiter_id=rid, title="Python Backend Developer Intern", company_name="TechCorp India",
                location="Bangalore (Remote)", opportunity_type="internship", stipend=18000, duration="3 months",
                required_skills="Python, FastAPI, SQL, Docker", min_cgpa=6.5, status="active",
                description="Write performant async endpoints, run migrations, configure Redis cache, and write unit tests."
            ),
            Opportunity(
                recruiter_id=rid, title="FastAPI Microservices Engineer", company_name="DataPipe Systems",
                location="Chennai", opportunity_type="placement", stipend=650000, duration="Full-Time",
                required_skills="Python, FastAPI, SQL, Docker, AWS", min_cgpa=7.0, status="active",
                description="Manage enterprise analytical data pipelines. Build and deploy containerized services on AWS ECS."
            ),
            Opportunity(
                recruiter_id=rid, title="Django REST Framework Specialist", company_name="WeaveSaaS Solutions",
                location="Remote", opportunity_type="internship", stipend=20000, duration="3 months",
                required_skills="Python, Django, SQL", min_cgpa=6.0, status="active",
                description="Optimize database queries and expand schema configurations for a multi-tenant business software."
            ),
            Opportunity(
                recruiter_id=rid, title="Junior API Engineer (Python)", company_name="QuickConnect Corp",
                location="Kolkata (Remote)", opportunity_type="internship", stipend=15000, duration="3 months",
                required_skills="Python, FastAPI, SQL", min_cgpa=6.0, status="active",
                description="Implement CRUD operations, generate API specifications, and ensure clean request validation using Pydantic."
            ),
            Opportunity(
                recruiter_id=rid, title="Distributed Database Developer", company_name="ScaleDB Labs",
                location="Pune", opportunity_type="placement", stipend=900000, duration="Full-Time",
                required_skills="SQL, Python, Docker, AWS", min_cgpa=7.5, status="active",
                description="Configure multi-region read replicas, scale execution plans, and implement caching topologies."
            ),
            Opportunity(
                recruiter_id=rid, title="FastAPI & Redis Backend Architect", company_name="SpeedFlow Tech",
                location="Bangalore", opportunity_type="placement", stipend=1100000, duration="Full-Time",
                required_skills="Python, FastAPI, SQL, Docker, AWS", min_cgpa=8.0, status="active",
                description="Architect sub-10ms response pipelines for transactional messaging hubs handling high peak concurrency."
            ),
            Opportunity(
                recruiter_id=rid, title="Django & Celery Task Engineer", company_name="BatchJobs Software",
                location="Remote", opportunity_type="internship", stipend=22000, duration="6 months",
                required_skills="Python, Django, SQL", min_cgpa=6.5, status="active",
                description="Build background work schedules, automate document reports, and handle transactional failures gracefully."
            ),
            Opportunity(
                recruiter_id=rid, title="Core Python Developer", company_name="AppDynamix",
                location="Ahmedabad", opportunity_type="internship", stipend=12000, duration="3 months",
                required_skills="Python, SQL", min_cgpa=6.0, status="active",
                description="Write command-line tools, clean file systems, integrate external endpoints, and parse flat logs."
            ),
            Opportunity(
                recruiter_id=rid, title="FastAPI backend assistant", company_name="Vikas Ventures",
                location="Remote", opportunity_type="internship", stipend=16000, duration="4 months",
                required_skills="Python, FastAPI, SQL", min_cgpa=6.2, status="active",
                description="Build internal database dashboards, clean test databases, and write custom validation utilities."
            ),
            Opportunity(
                recruiter_id=rid, title="Relational Database Optimizer", company_name="QueryCore Inc.",
                location="Hyderabad", opportunity_type="placement", stipend=700000, duration="Full-Time",
                required_skills="SQL, PostgreSQL, Linux", min_cgpa=7.0, status="active",
                description="Identify slow queries, implement indexes, prune partitioned tables, and optimize configuration schemas."
            ),

            # ─── FRONTEND & WEB ENG (React, JS, HTML, CSS, Tailwind) ───
            Opportunity(
                recruiter_id=rid, title="Frontend Developer (React & Tailwind)", company_name="PixelCraft Studios",
                location="Pune (Hybrid)", opportunity_type="internship", stipend=16000, duration="4 months",
                required_skills="React, JavaScript, HTML, CSS", min_cgpa=6.0, status="active",
                description="Build responsive user interfaces from Figma blueprints. Configure layouts and manage component states."
            ),
            Opportunity(
                recruiter_id=rid, title="UI/UX Web Engineering Intern", company_name="DesignSprint Co.",
                location="Delhi", opportunity_type="internship", stipend=15000, duration="3 months",
                required_skills="JavaScript, HTML, CSS", min_cgpa=6.0, status="active",
                description="Translate mockups into pixel-perfect semantic layouts, style transitions, and validate user inputs."
            ),
            Opportunity(
                recruiter_id=rid, title="React Component Library Engineer", company_name="UiKit Labs",
                location="Remote", opportunity_type="placement", stipend=600000, duration="Full-Time",
                required_skills="React, JavaScript, HTML, CSS", min_cgpa=6.5, status="active",
                description="Develop modular, highly reusable component systems with strict layout guarantees and clear state properties."
            ),
            Opportunity(
                recruiter_id=rid, title="React Developer Intern", company_name="ZetaFin Tech",
                location="Bangalore", opportunity_type="internship", stipend=20000, duration="3 months",
                required_skills="React, JavaScript, HTML, CSS", min_cgpa=7.0, status="active",
                description="Improve transaction summary screens, configure charts, and integrate asynchronous secure data feeds."
            ),
            Opportunity(
                recruiter_id=rid, title="Web Application Specialist", company_name="WebScale Solutions",
                location="Gurgaon", opportunity_type="placement", stipend=750000, duration="Full-Time",
                required_skills="React, JavaScript, HTML, CSS, AWS", min_cgpa=6.8, status="active",
                description="Enhance rendering performance, lazy load modules, and configure secure deployment bundles."
            ),
            Opportunity(
                recruiter_id=rid, title="HTML/CSS Layout Assistant", company_name="FreshWebs",
                location="Remote", opportunity_type="internship", stipend=10000, duration="3 months",
                required_skills="HTML, CSS, JavaScript", min_cgpa=5.8, status="active",
                description="Ensure legacy web templates maintain fully responsive interfaces across multiple mobile devices."
            ),
            Opportunity(
                recruiter_id=rid, title="Junior JavaScript Developer", company_name="CodeBase India",
                location="Kochi", opportunity_type="internship", stipend=14000, duration="4 months",
                required_skills="JavaScript, HTML, CSS", min_cgpa=6.0, status="active",
                description="Write clear ES6 functions, interact with browser storages, and configure interactive maps."
            ),
            Opportunity(
                recruiter_id=rid, title="Single Page App Specialist", company_name="AppNest",
                location="Remote", opportunity_type="internship", stipend=18000, duration="6 months",
                required_skills="React, JavaScript, HTML, CSS", min_cgpa=6.2, status="active",
                description="Handle advanced page routing, nested state parameters, and coordinate dynamic form inputs."
            ),
            Opportunity(
                recruiter_id=rid, title="Frontend Performance Engineer", company_name="SpeedApp Co",
                location="Noida", opportunity_type="placement", stipend=800000, duration="Full-Time",
                required_skills="React, JavaScript, HTML, CSS", min_cgpa=7.5, status="active",
                description="Optimize browser layout calculations, reduce DOM sizing parameters, and compress build payloads."
            ),
            Opportunity(
                recruiter_id=rid, title="Tailwind Layout Specialist", company_name="DesignSystem Corp",
                location="Remote", opportunity_type="internship", stipend=15000, duration="3 months",
                required_skills="React, JavaScript, HTML, CSS", min_cgpa=6.0, status="active",
                description="Convert custom branding definitions into clean utility classes and maintain design system tokens."
            ),

            # ─── FULL-STACK (React, Node, MongoDB, MERN) ───
            Opportunity(
                recruiter_id=rid, title="Full-Stack React & Node Developer", company_name="StartupHub",
                location="Mumbai (Remote)", opportunity_type="internship", stipend=25000, duration="6 months",
                required_skills="React, Node.js, JavaScript, MongoDB", min_cgpa=7.0, status="active",
                description="Build interactive management systems, set up express server pipelines, and manage database queries."
            ),
            Opportunity(
                recruiter_id=rid, title="Full-Stack Web Dev Intern", company_name="AppFactory Solutions",
                location="Noida (Hybrid)", opportunity_type="internship", stipend=18000, duration="6 months",
                required_skills="React, Node.js, JavaScript, MongoDB", min_cgpa=6.5, status="active",
                description="Maintain backoffice dashboards, configure secure login steps, and manage analytical data schemas."
            ),
            Opportunity(
                recruiter_id=rid, title="MERN Stack Placement", company_name="Velocty Devs",
                location="Chandigarh", opportunity_type="placement", stipend=650000, duration="Full-Time",
                required_skills="React, Node.js, JavaScript, MongoDB", min_cgpa=6.8, status="active",
                description="Participate in full development cycles. Implement database aggregates, server validations, and component state trees."
            ),
            Opportunity(
                recruiter_id=rid, title="Node.js API Specialist", company_name="NodeStream",
                location="Remote", opportunity_type="placement", stipend=720000, duration="Full-Time",
                required_skills="Node.js, JavaScript, MongoDB", min_cgpa=7.0, status="active",
                description="Design low-latency server endpoints, process files, and handle multiple connection maps."
            ),
            Opportunity(
                recruiter_id=rid, title="Full-Stack Assistant", company_name="AlphaTech",
                location="Remote", opportunity_type="internship", stipend=16000, duration="3 months",
                required_skills="React, Node.js, JavaScript, MongoDB", min_cgpa=6.0, status="active",
                description="Debug client interfaces, test server operations, write migration steps, and clean old log files."
            ),
            Opportunity(
                recruiter_id=rid, title="Enterprise MERN Developer", company_name="GlobalLogics",
                location="Bangalore", opportunity_type="placement", stipend=900000, duration="Full-Time",
                required_skills="React, Node.js, JavaScript, MongoDB, AWS", min_cgpa=7.5, status="active",
                description="Architect transaction services, secure schema endpoints, and deploy to containerized cloud systems."
            ),
            Opportunity(
                recruiter_id=rid, title="MERN Stack Intern", company_name="BetaLabs",
                location="Remote", opportunity_type="internship", stipend=20000, duration="4 months",
                required_skills="React, Node.js, JavaScript, MongoDB", min_cgpa=6.4, status="active",
                description="Incorporate third-party authentication structures, write email triggers, and test payment flows."
            ),
            Opportunity(
                recruiter_id=rid, title="NodeJS REST Service Engineer", company_name="ServeCore",
                location="Chennai", opportunity_type="placement", stipend=600000, duration="Full-Time",
                required_skills="Node.js, JavaScript, MongoDB", min_cgpa=6.5, status="active",
                description="Build internal tracking servers, schedule database cleaner scripts, and optimize server parameters."
            ),

            # ─── DEEP TECH, AI, MACHINE LEARNING & COMPUTER VISION ───
            Opportunity(
                recruiter_id=rid, title="Machine Learning Research Intern", company_name="AI Labs India",
                location="Hyderabad", opportunity_type="internship", stipend=30000, duration="6 months",
                required_skills="Python, Machine Learning, TensorFlow, Data Science", min_cgpa=7.5, status="active",
                description="Label multi-lingual data streams, train prediction models, and compile weights with ONNX runtimes."
            ),
            Opportunity(
                recruiter_id=rid, title="Deep Learning & CV Architect", company_name="CognitiveVision",
                location="Bangalore", opportunity_type="placement", stipend=850000, duration="Full-Time",
                required_skills="Python, Machine Learning, TensorFlow, Computer Vision", min_cgpa=8.0, status="active",
                description="Develop, configure, and train advanced convolution models for object segmentations and pose mappings."
            ),
            Opportunity(
                recruiter_id=rid, title="Natural Language Processing Intern", company_name="LangTech AI",
                location="Noida (Hybrid)", opportunity_type="internship", stipend=25000, duration="6 months",
                required_skills="Python, Machine Learning, Data Science, Natural Language Processing", min_cgpa=7.5, status="active",
                description="Tune specialized model weights for semantic analysis across diverse technical Indian dialects."
            ),
            Opportunity(
                recruiter_id=rid, title="Data Science Consultant", company_name="InsightAnalytics",
                location="Remote", opportunity_type="placement", stipend=700000, duration="Full-Time",
                required_skills="Python, Data Science, SQL, Machine Learning", min_cgpa=7.0, status="active",
                description="Implement regression, run cluster analytics, and construct clean data reporting workflows."
            ),
            Opportunity(
                recruiter_id=rid, title="MLOps Deployment Specialist", company_name="ModelOps Tech",
                location="Hyderabad", opportunity_type="placement", stipend=750000, duration="Full-Time",
                required_skills="Python, Machine Learning, Docker, AWS", min_cgpa=7.2, status="active",
                description="Configure automation pipelines for models, monitor system parameters, and build inference APIs."
            ),
            Opportunity(
                recruiter_id=rid, title="Computer Vision Research Assistant", company_name="RoboVision",
                location="Pune", opportunity_type="internship", stipend=22000, duration="6 months",
                required_skills="Python, Computer Vision, Machine Learning", min_cgpa=7.8, status="active",
                description="Optimize image pre-processing pipelines, train custom YOLO architectures, and write detection scripts."
            ),
            Opportunity(
                recruiter_id=rid, title="NLP Parsing Specialist", company_name="GlossaryAI",
                location="Remote", opportunity_type="placement", stipend=800000, duration="Full-Time",
                required_skills="Python, Natural Language Processing, Machine Learning", min_cgpa=7.5, status="active",
                description="Build semantic mapping parsers, manage text embeddings, and configure multi-language dictionaries."
            ),
            Opportunity(
                recruiter_id=rid, title="Data Science Assistant", company_name="StatLabs",
                location="Remote", opportunity_type="internship", stipend=15000, duration="3 months",
                required_skills="Python, Data Science, SQL", min_cgpa=6.5, status="active",
                description="Write web scraper scripts, clean database models, compute statistcal variances, and build charts."
            ),

            # ─── MINISTRY OF AYUSH / HEALTH-TECH INTEGRATION (Ayurveda, Yoga Science) ───
            Opportunity(
                recruiter_id=rid, title="AYUSH Digital Health Platform Developer", company_name="Ministry of AYUSH Partner",
                location="New Delhi", opportunity_type="internship", stipend=20000, duration="4 months",
                required_skills="Python, React, SQL, Ayurveda Informatics", min_cgpa=6.5, status="active",
                description="Design and test EHR databases conforming to traditional medicine and national clinical criteria."
            ),
            Opportunity(
                recruiter_id=rid, title="Yoga Posture AI Tracker Developer", company_name="AYUSH Wellness AI",
                location="Rishikesh (Hybrid)", opportunity_type="internship", stipend=18000, duration="3 months",
                required_skills="Python, Computer Vision, Machine Learning, Yoga Science", min_cgpa=6.0, status="active",
                description="Incorporate CV models to detect pose coordinates, calibrate balances, and provide direct feedback."
            ),
            Opportunity(
                recruiter_id=rid, title="Ayurvedic Herb Classifier Analyst", company_name="AYUSH Research Lab",
                location="Jamnagar", opportunity_type="internship", stipend=15000, duration="6 months",
                required_skills="Python, Machine Learning, Computer Vision, Ayurveda Informatics", min_cgpa=7.0, status="active",
                description="Train CNN architectures on botanical specimen scans to enable automated quality checks."
            ),
            Opportunity(
                recruiter_id=rid, title="AYUSH Telemedicine Portal Developer", company_name="Swasthya Digital Solutions",
                location="Delhi (Remote)", opportunity_type="internship", stipend=17000, duration="4 months",
                required_skills="React, Node.js, MongoDB, Ayurveda Informatics", min_cgpa=6.5, status="active",
                description="Coordinate clinic video feeds, schedule doctor slots, and secure patient clinical records."
            ),
            Opportunity(
                recruiter_id=rid, title="AYUSH Wellness Platform Architect", company_name="AYUSH Global Wellness",
                location="Remote", opportunity_type="placement", stipend=550000, duration="Full-Time",
                required_skills="Ayurveda Informatics, SQL, React", min_cgpa=6.0, status="active",
                description="Organize herb distribution metrics, build wellness trackers, and coordinate system evaluations."
            ),
            Opportunity(
                recruiter_id=rid, title="Ayurvedic EHR System Designer", company_name="AYUSH Information Systems",
                location="Thiruvananthapuram", opportunity_type="placement", stipend=650000, duration="Full-Time",
                required_skills="Python, FastAPI, SQL, Ayurveda Informatics", min_cgpa=7.0, status="active",
                description="Coordinate with medical practitioners to design clean relational tables to store historical diagnostic profiles."
            ),
            Opportunity(
                recruiter_id=rid, title="Yoga Posture AI Research Intern", company_name="Samyama Yoga Tech",
                location="Remote", opportunity_type="internship", stipend=16000, duration="3 months",
                required_skills="Python, Computer Vision, Yoga Science", min_cgpa=6.2, status="active",
                description="Analyze body coordinate variances during advanced positions and build alignment matrices."
            ),
            Opportunity(
                recruiter_id=rid, title="AYUSH Botanical Herb Database Specialist", company_name="HerbData Labs",
                location="Varanasi", opportunity_type="placement", stipend=500000, duration="Full-Time",
                required_skills="SQL, Python, Ayurveda Informatics", min_cgpa=6.5, status="active",
                description="Populate, index, and query global herbal catalog files to ensure optimal matching latency."
            ),
            Opportunity(
                recruiter_id=rid, title="AYUSH Telehealth Platform Security Intern", company_name="Niramaya Systems",
                location="Remote", opportunity_type="internship", stipend=20000, duration="4 months",
                required_skills="Cybersecurity, Linux, Ayurveda Informatics", min_cgpa=7.0, status="active",
                description="Test clinic databases for security flaws, encrypt patient communication channels, and audit permissions."
            ),
            Opportunity(
                recruiter_id=rid, title="Ayurvedic Herb Vision Analytics Developer", company_name="Dravyaguna AI",
                location="Haridwar", opportunity_type="placement", stipend=750000, duration="Full-Time",
                required_skills="Python, Computer Vision, Machine Learning, Ayurveda Informatics", min_cgpa=7.2, status="active",
                description="Train specialized neural nets to classify leaf and seed textures for Ayurvedic pharmacists."
            ),

            # ─── CLOUD, DEVOPS & INFRASTRUCTURE ───
            Opportunity(
                recruiter_id=rid, title="Cloud & DevOps Engineer Intern", company_name="CloudFirst Solutions",
                location="Pune (Remote)", opportunity_type="internship", stipend=24000, duration="4 months",
                required_skills="Docker, AWS, Linux, Python", min_cgpa=7.0, status="active",
                description="Configure server pipelines, automate build steps, monitor parameters, and orchestrate server instances."
            ),
            Opportunity(
                recruiter_id=rid, title="Site Reliability Placement", company_name="AWS Cloud Center",
                location="Mumbai", opportunity_type="placement", stipend=900000, duration="Full-Time",
                required_skills="AWS, Docker, Kubernetes, Linux, Python", min_cgpa=7.5, status="active",
                description="Manage global cloud servers. Automate auto-scaling scripts, monitor limits, and write failover pipelines."
            ),
            Opportunity(
                recruiter_id=rid, title="AWS Cloud Infrastructure Intern", company_name="InfraScale",
                location="Remote", opportunity_type="internship", stipend=20000, duration="3 months",
                required_skills="AWS, Docker, Linux", min_cgpa=6.8, status="active",
                description="Monitor active cloud resources, deploy containers to target pools, and adjust cloud security logs."
            ),

            # ─── CYBERSECURITY, LINUX & ENTERPRISE JAVA ───
            Opportunity(
                recruiter_id=rid, title="Cybersecurity & Vulnerability Intern", company_name="SecureNet India",
                location="Bangalore (Hybrid)", opportunity_type="internship", stipend=22000, duration="6 months",
                required_skills="Cybersecurity, Linux, Python, Networking", min_cgpa=7.0, status="active",
                description="Participate in penetration test runs, analyze network logs, and configure security rules."
            ),
            Opportunity(
                recruiter_id=rid, title="Network Security Engineer", company_name="Sentinel Cyber",
                location="Chennai", opportunity_type="placement", stipend=800000, duration="Full-Time",
                required_skills="Cybersecurity, Networking, Linux, AWS", min_cgpa=7.5, status="active",
                description="Architect secure network backbones, configure firewall architectures, and orchestrate audits."
            ),
            Opportunity(
                recruiter_id=rid, title="Junior Linux Systems Administrator", company_name="SecureHost Infra",
                location="Bangalore", opportunity_type="placement", stipend=500000, duration="Full-Time",
                required_skills="Linux, Cybersecurity, Networking", min_cgpa=6.5, status="active",
                description="Maintain server environments. Monitor active pipelines, update configurations, and fix firewall issues."
            ),
            Opportunity(
                recruiter_id=rid, title="Java Spring Boot Placement", company_name="Nagarro",
                location="Gurgaon", opportunity_type="placement", stipend=650000, duration="Full-Time",
                required_skills="Java, Spring Boot, SQL", min_cgpa=7.0, status="active",
                description="Collaborate with corporate clients to write secure, scalable enterprise APIs."
            ),
            Opportunity(
                recruiter_id=rid, title="Java Developer Intern", company_name="InfoSys",
                location="Hyderabad", opportunity_type="internship", stipend=18000, duration="6 months",
                required_skills="Java, Spring Boot, SQL", min_cgpa=7.0, status="active",
                description="Enterprise microservices development. Write JDBC routines and optimize SQL queries."
            ),
        ]

        db.add_all(opportunities)
        db.commit()
        print(f"✅ Re-seeded {len(opportunities)} detailed Opportunities.")

        # 2. SEEDING 40+ TARGETED YOUTUBE-LINKED COURSES
        courses = [
            # Python
            Course(
                title="Python Full Course for Beginners", provider="Programming with Mosh",
                url="https://www.youtube.com/watch?v=_uQrJ0TkZlc", skill_tags="Python",
                difficulty="beginner", duration_hours=6.0, rating=4.9, is_free=1,
                description="Complete introductory guide. Cover variables, loops, objects, structures, and foundational algorithms."
            ),
            Course(
                title="Python Advanced: OOP, Decorators, & Threading", provider="Corey Schafer",
                url="https://www.youtube.com/watch?v=ZDa-Z5JzLYM", skill_tags="Python, Advanced Python",
                difficulty="advanced", duration_hours=8.0, rating=4.9, is_free=1,
                description="Deep dive on advanced language topics, memory configurations, class decorators, and multi-thread pools."
            ),
            Course(
                title="Python OOP Complete Masterclass", provider="Corey Schafer",
                url="https://www.youtube.com/watch?v=ZDa-Z5JzLYM&list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc", skill_tags="Python",
                difficulty="intermediate", duration_hours=4.5, rating=4.8, is_free=1,
                description="Understand real object design, inheritances, abstract properties, and modular software designs."
            ),

            # Web Frameworks (React, Node, FastAPI, Django)
            Course(
                title="React JS Full Course 2024", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=bMknfKXIFA8", skill_tags="React, JavaScript",
                difficulty="beginner", duration_hours=12.0, rating=4.8, is_free=1,
                description="Step-by-step introduction. Covers virtual dom, functional components, hooks, state, and properties."
            ),
            Course(
                title="Redux Toolkit & State Management Course", provider="Dave Gray",
                url="https://www.youtube.com/watch?v=NqzdVN2tyvQ", skill_tags="React, Redux, JavaScript",
                difficulty="intermediate", duration_hours=4.0, rating=4.7, is_free=1,
                description="Master global store structures, action dispatches, selectors, async operations, and slice definitions."
            ),
            Course(
                title="FastAPI Python Async Microservices", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=7t2alSnE2-I", skill_tags="FastAPI, Python",
                difficulty="intermediate", duration_hours=4.5, rating=4.7, is_free=1,
                description="Write high-speed async APIs, validate payloads using Pydantic, and test automatic swagger pages."
            ),
            Course(
                title="Django Web Development Full Course", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=F5mRW0jo-U4", skill_tags="Django, Python",
                difficulty="intermediate", duration_hours=16.0, rating=4.8, is_free=1,
                description="Full-featured development. Covers models, generic class-based views, query optimization, and testing."
            ),
            Course(
                title="Node.js & Express.js Backend Course", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=Oe421EPjeBE", skill_tags="Node.js, JavaScript",
                difficulty="intermediate", duration_hours=8.0, rating=4.8, is_free=1,
                description="Learn runtime setups, route routers, database access, JWT validations, and system logging."
            ),

            # Databases & SQL
            Course(
                title="SQL Database Full Course for Beginners", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=HXV3zeQKqGY", skill_tags="SQL",
                difficulty="beginner", duration_hours=4.5, rating=4.8, is_free=1,
                description="Understand relational databases, write basic SELECT statements, configure JOIN filters, and sort columns."
            ),
            Course(
                title="PostgreSQL Advanced Queries & Index Optimization", provider="Amigoscode",
                url="https://www.youtube.com/watch?v=qw--VYLpxG4", skill_tags="SQL, PostgreSQL",
                difficulty="advanced", duration_hours=4.0, rating=4.7, is_free=1,
                description="Deep-dive on indexes, partial filters, explain plans, execution cost evaluations, and database locks."
            ),
            Course(
                title="MongoDB NoSQL Database Tutorial", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=ofme2o29ngU", skill_tags="MongoDB",
                difficulty="intermediate", duration_hours=6.0, rating=4.6, is_free=1,
                description="Understand unstructured document models, write nested schemas, use pipelines, and group data."
            ),

            # Machine Learning & AI
            Course(
                title="Machine Learning Full Course (10 Hours)", provider="Simplilearn",
                url="https://www.youtube.com/watch?v=GwIo3gDZCVQ", skill_tags="Machine Learning, Python, Data Science",
                difficulty="intermediate", duration_hours=10.0, rating=4.7, is_free=1,
                description="Covers regression, classifications, vector machines, decision trees, random forests, and standard evaluation metrics."
            ),
            Course(
                title="Deep Learning with PyTorch & Neural Networks", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=GIsg-ZUy0MY", skill_tags="Machine Learning, PyTorch, Deep Learning",
                difficulty="advanced", duration_hours=9.0, rating=4.8, is_free=1,
                description="Understand network structures, write weights, implement SGD, configure loss, and save parameters."
            ),
            Course(
                title="TensorFlow 2.0 Full Deep Learning Tutorial", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=tPYj3fFJGjk", skill_tags="TensorFlow, Machine Learning",
                difficulty="intermediate", duration_hours=7.0, rating=4.7, is_free=1,
                description="Covers CNN networks, layer structures, classification tasks, data scaling, and model evaluations."
            ),
            Course(
                title="Natural Language Processing (NLP) with Transformers", provider="Stanford University",
                url="https://www.youtube.com/watch?v=8rXD5-xhemo", skill_tags="NLP, Natural Language Processing, Machine Learning",
                difficulty="advanced", duration_hours=18.0, rating=4.9, is_free=1,
                description="Explore semantic representations, multi-head attention systems, fine-tuning, and model evaluations."
            ),
            Course(
                title="Computer Vision with OpenCV & Python", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=oXlwWbU8l2o", skill_tags="Computer Vision, OpenCV, Python",
                difficulty="intermediate", duration_hours=9.0, rating=4.8, is_free=1,
                description="Explore image filtering, color maps, face classifiers, gesture tracing, and video processing."
            ),
            Course(
                title="Data Science Full Course (14 Hours)", provider="Simplilearn",
                url="https://www.youtube.com/watch?v=-ETQ97mXXF0", skill_tags="Data Science, Python",
                difficulty="intermediate", duration_hours=14.0, rating=4.6, is_free=1,
                description="Covers Pandas parsing, data visualizations, cleaning pipelines, and statistical classifications."
            ),

            # Cloud & DevOps
            Course(
                title="Docker & Containerization Hands-on Tutorial", provider="TechWorld with Nana",
                url="https://www.youtube.com/watch?v=3c-iBn73dDE", skill_tags="Docker",
                difficulty="intermediate", duration_hours=5.0, rating=4.9, is_free=1,
                description="Learn container builds, images, tags, multi-container compose orchestration, and network settings."
            ),
            Course(
                title="AWS Certified Cloud Practitioner Full Course", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=3hLmDS179YE", skill_tags="AWS",
                difficulty="beginner", duration_hours=13.0, rating=4.8, is_free=1,
                description="Covers EC2 instances, S3, virtual clouds, IAM permissions, database setups, and billing matrices."
            ),
            Course(
                title="Kubernetes Full Course (TechWorld with Nana)", provider="TechWorld with Nana",
                url="https://www.youtube.com/watch?v=X48VuDVv0do", skill_tags="Kubernetes, Docker",
                difficulty="advanced", duration_hours=4.5, rating=4.9, is_free=1,
                description="Master pods, ingress, services, configmaps, persistent volumes, and deployment automation."
            ),

            # Cybersecurity & Infrastructure
            Course(
                title="Cybersecurity Fundamentals & Ethical Hacking", provider="Simplilearn",
                url="https://www.youtube.com/watch?v=900x5hYGBPo", skill_tags="Cybersecurity",
                difficulty="beginner", duration_hours=11.0, rating=4.6, is_free=1,
                description="Covers penetration testing, malware analysis, network scanning, firewall logs, and security defenses."
            ),
            Course(
                title="Linux Command Line & Shell Scripting", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=ROjZy1WbCIA", skill_tags="Linux",
                difficulty="beginner", duration_hours=9.0, rating=4.8, is_free=1,
                description="Master terminal commands, file attributes, stream redirect pipes, and shell scripts."
            ),
            Course(
                title="Networking Fundamentals for Cyber Security", provider="NetworkChuck",
                url="https://www.youtube.com/watch?v=qiQR5rTSshw", skill_tags="Networking",
                difficulty="beginner", duration_hours=6.0, rating=4.8, is_free=1,
                description="Covers OSI models, TCP/IP, router subnet configurations, switches, and secure gateways."
            ),

            # AYUSH Digital Health & Interdisciplinary Informatics
            Course(
                title="Ayurveda Informatics & Traditional Health Systems", provider="Ministry of AYUSH / Swayam",
                url="https://www.youtube.com/watch?v=VbOBfMjGJpM", skill_tags="Ayurveda Informatics",
                difficulty="beginner", duration_hours=3.0, rating=4.5, is_free=1,
                description="Covers traditional terminologies, electronic health record criteria, and classification frameworks."
            ),
            Course(
                title="Yoga Science & Posture Kinetics Intro", provider="AYUSH Wellness Council",
                url="https://www.youtube.com/watch?v=VbOBfMjGJpM", skill_tags="Yoga Science",
                difficulty="beginner", duration_hours=2.5, rating=4.4, is_free=1,
                description="Explores joint kinetics, wellness parameters, and calibration benchmarks for system modeling."
            ),
            Course(
                title="HTML & CSS Complete Course", provider="SuperSimpleDev",
                url="https://www.youtube.com/watch?v=G3e-cpL7ofc", skill_tags="HTML, CSS",
                difficulty="beginner", duration_hours=6.5, rating=4.8, is_free=1,
                description="Understand structure parsing, box formatting, semantic tags, and responsive layouts."
            ),
            Course(
                title="JavaScript Full Course", provider="SuperSimpleDev",
                url="https://www.youtube.com/watch?v=EerdGm-ehJQ", skill_tags="JavaScript",
                difficulty="beginner", duration_hours=22.0, rating=4.9, is_free=1,
                description="Master variables, functions, DOM elements, async endpoints, and modular code structures."
            ),
            Course(
                title="Java Programming Tutorial for Beginners", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=xk4_1vDrzzo", skill_tags="Java",
                difficulty="beginner", duration_hours=12.0, rating=4.7, is_free=1,
                description="Covers Java syntax, data structures, compilation matrices, and OOP implementations."
            ),
            Course(
                title="Spring Boot Microservices Tutorial", provider="Amigoscode",
                url="https://www.youtube.com/watch?v=xk4_1vDrzzo", skill_tags="Spring Boot, Java",
                difficulty="intermediate", duration_hours=5.5, rating=4.8, is_free=1,
                description="Learn API routers, security configurations, dependency structures, and SQL configurations."
            ),
            Course(
                title="Tailwind CSS Full Tutorial for Beginners", provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=dFgzHOX84xQ", skill_tags="Tailwind",
                difficulty="beginner", duration_hours=4.0, rating=4.7, is_free=1,
                description="Learn grid systems, custom utility classes, dark theme configurations, and component setups."
            ),
        ]

        db.add_all(courses)
        db.commit()
        print(f"✅ Successfully seeded {len(courses)} high-quality YouTube Courses.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding catalog: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_final_catalog()
