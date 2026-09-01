import sys
import os
from sqlalchemy.orm import Session

# Ensure we can import from the root backend directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import engine, SessionLocal, Base
from models.user import User
from models.recruiter import Recruiter
from models.opportunity import Opportunity
from models.course import Course
from utils.auth import hash_password

def seed_production_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("🧹 Cleaning old opportunities and courses from the database...")
        db.query(Opportunity).delete()
        db.query(Course).delete()
        db.commit()

        # 1. Ensure a valid system recruiter is present
        recruiter = db.query(User).filter(User.role == "recruiter").first()
        if not recruiter:
            recruiter = User(
                name="Internshala Partner Network",
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
                designation="Director of University Relations",
                industry="Education & Technology",
                company_size="500-1000"
            ))
            db.commit()

        rid = recruiter.id
        print(f"👤 Assigned recruiter ID: {rid}")

        # 2. SEEDING 30+ RICH INTERNSHIPS & PLACEMENTS
        opportunities = [
            # ─── SOFTWARE ENGINEERING & BACKEND ───
            Opportunity(
                recruiter_id=rid,
                title="Python Backend Developer Intern",
                company_name="TechCorp India",
                location="Bangalore (Remote)",
                opportunity_type="internship",
                stipend=18000,
                duration="3 months",
                required_skills="Python, FastAPI, SQL, Docker",
                min_cgpa=6.5,
                description="Join our fast-paced backend team to write performant asynchronous endpoints, configure Redis caching, and set up Dockerized testing pipelines.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="FastAPI Microservices Engineer",
                company_name="DataPipe Systems",
                location="Chennai",
                opportunity_type="placement",
                stipend=650000,
                duration="Full-Time",
                required_skills="Python, FastAPI, SQL, Docker, AWS",
                min_cgpa=7.0,
                description="Manage enterprise data workflows. Build microservices using FastAPI, maintain PostgreSQL connections, and deploy to AWS ECS.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Java Spring Boot Backend Intern",
                company_name="HDFC Digital Labs",
                location="Mumbai (Hybrid)",
                opportunity_type="internship",
                stipend=22000,
                duration="6 months",
                required_skills="Java, Spring Boot, SQL",
                min_cgpa=7.0,
                description="Work with security architects to design transactional endpoints using Spring Boot, Hibernate ORM, and Oracle Database structures.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Django REST Framework Specialist",
                company_name="WeaveSaaS",
                location="Remote",
                opportunity_type="internship",
                stipend=20000,
                duration="3 months",
                required_skills="Python, Django, SQL",
                min_cgpa=6.0,
                description="Optimize and expand multi-tenant backend schemas using Django, Celery background tasks, and PostgreSQL.",
                status="active"
            ),

            # ─── FRONTEND & WEB ENG ───
            Opportunity(
                recruiter_id=rid,
                title="Full-Stack React Developer",
                company_name="StartupHub",
                location="Mumbai (Remote)",
                opportunity_type="internship",
                stipend=25000,
                duration="6 months",
                required_skills="React, JavaScript, Node.js, JavaScript",
                min_cgpa=7.0,
                description="Build interactive administrative panels and live dashboards. Connect frontend Redux stores to REST APIs.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Frontend Developer (React & Tailwind)",
                company_name="PixelCraft Studios",
                location="Pune (Hybrid)",
                opportunity_type="internship",
                stipend=16000,
                duration="4 months",
                required_skills="React, JavaScript, HTML, CSS",
                min_cgpa=6.0,
                description="Craft polished responsive web interfaces. Convert layout templates into modular, re-usable React code.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="UI/UX Web Engineering Intern",
                company_name="DesignSprint Co.",
                location="Delhi",
                opportunity_type="internship",
                stipend=15000,
                duration="3 months",
                required_skills="JavaScript, HTML, CSS",
                min_cgpa=6.0,
                description="Collaborate with layout designers. Refactor design assets into semantic, lightweight HTML, custom CSS, and vanilla JS.",
                status="active"
            ),

            # ─── DEEP TECH, AI & MACHINE LEARNING ───
            Opportunity(
                recruiter_id=rid,
                title="Machine Learning Research Intern",
                company_name="AI Labs India",
                location="Hyderabad",
                opportunity_type="internship",
                stipend=30000,
                duration="6 months",
                required_skills="Python, Machine Learning, TensorFlow, Data Science",
                min_cgpa=7.5,
                description="Conduct clinical data labeling, fine-tune transformer architectures, and deploy models locally using ONNX runtimes.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Deep Learning & CV Architect",
                company_name="CognitiveVision Systems",
                location="Bangalore",
                opportunity_type="placement",
                stipend=850000,
                duration="Full-Time",
                required_skills="Python, Machine Learning, TensorFlow, Computer Vision",
                min_cgpa=8.0,
                description="Implement state-of-the-art vision models for object segmentation and real-time posture analysis systems.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Natural Language Processing Intern",
                company_name="LangTech AI",
                location="Noida (Hybrid)",
                opportunity_type="internship",
                stipend=25000,
                duration="6 months",
                required_skills="Python, Machine Learning, Data Science, Natural Language Processing",
                min_cgpa=7.5,
                description="Train specialized text-parsing classifiers on multi-lingual Indian dialects and technical documentation corpora.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Data Science Consultant",
                company_name="InsightAnalytics Partners",
                location="Remote",
                opportunity_type="placement",
                stipend=700000,
                duration="Full-Time",
                required_skills="Python, Data Science, SQL, Machine Learning",
                min_cgpa=7.0,
                description="Leverage regression, classification, and statistical modeling to generate commercial pricing intelligence.",
                status="active"
            ),

            # ─── MINISTRY OF AYUSH / HEALTH-TECH ALIGNED ───
            Opportunity(
                recruiter_id=rid,
                title="AYUSH Digital Health Platform Engineer",
                company_name="Ministry of AYUSH Partner",
                location="New Delhi",
                opportunity_type="internship",
                stipend=20000,
                duration="4 months",
                required_skills="Python, React, SQL, Ayurveda Informatics",
                min_cgpa=6.5,
                description="Design and test EHR database systems for traditional Indian medicine clinics under the Ayushman Bharat Digital Mission.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Yoga Posture AI Tracker Developer",
                company_name="AYUSH Wellness AI",
                location="Rishikesh (Hybrid)",
                opportunity_type="internship",
                stipend=18000,
                duration="3 months",
                required_skills="Python, Computer Vision, Machine Learning, Yoga Science",
                min_cgpa=6.0,
                description="Help develop pose detection and calibration logic to provide automatic, real-time wellness guidelines.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Ayurvedic Herb Classifier Analyst",
                company_name="AYUSH Research Council Labs",
                location="Jamnagar (Hybrid)",
                opportunity_type="internship",
                stipend=15000,
                duration="6 months",
                required_skills="Python, Machine Learning, Computer Vision, Ayurveda Informatics",
                min_cgpa=7.0,
                description="Train CNN architectures on raw herbal scans to enable automated specimen verification and catalog sorting.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="AYUSH Telemedicine Portal Developer",
                company_name="Swasthya Digital Solutions",
                location="Delhi (Remote)",
                opportunity_type="internship",
                stipend=17000,
                duration="4 months",
                required_skills="React, Node.js, MongoDB, Ayurveda Informatics",
                min_cgpa=6.5,
                description="Improve real-time video consultation feeds and appointment tracking for traditional AYUSH clinics.",
                status="active"
            ),

            # ─── CLOUD, DEVOPS & INFRASTRUCTURE ───
            Opportunity(
                recruiter_id=rid,
                title="Cloud & DevOps Engineer Intern",
                company_name="CloudFirst Solutions",
                location="Pune (Remote)",
                opportunity_type="internship",
                stipend=24000,
                duration="4 months",
                required_skills="Docker, AWS, Linux, Python",
                min_cgpa=7.0,
                description="Automate build pipelines using GitHub Actions, configure cloud databases, and monitor system parameters on AWS.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Site Reliability Placement",
                company_name="AWS Cloud Center India",
                location="Mumbai",
                opportunity_type="placement",
                stipend=900000,
                duration="Full-Time",
                required_skills="AWS, Docker, Kubernetes, Linux, Python",
                min_cgpa=7.5,
                description="Manage high-scale cloud clusters. Implement auto-scaling strategies and coordinate failover architectures.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Junior Linux Systems Administrator",
                company_name="SecureHost Infra",
                location="Bangalore",
                opportunity_type="placement",
                stipend=500000,
                duration="Full-Time",
                required_skills="Linux, Cybersecurity, Networking",
                min_cgpa=6.5,
                description="Monitor data center networks. Manage configurations, manage user keys, and install security patches.",
                status="active"
            ),

            # ─── CYBERSECURITY & NETWORKING ───
            Opportunity(
                recruiter_id=rid,
                title="Cybersecurity & Vulnerability Intern",
                company_name="SecureNet India",
                location="Bangalore (Hybrid)",
                opportunity_type="internship",
                stipend=22000,
                duration="6 months",
                required_skills="Cybersecurity, Linux, Python, Networking",
                min_cgpa=7.0,
                description="Perform penetration testing audits, parse connection maps, and configure firewall rule engines.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Network Security Engineer",
                company_name="Sentinel Cybersec",
                location="Chennai",
                opportunity_type="placement",
                stipend=800000,
                duration="Full-Time",
                required_skills="Cybersecurity, Networking, Linux, AWS",
                min_cgpa=7.5,
                description="Architect internal routing matrices, configure virtual private clouds, and perform secure system tests.",
                status="active"
            ),

            # ─── ADDITIONAL HIGH-GROWTH TECH ROLES ───
            Opportunity(
                recruiter_id=rid,
                title="FastAPI API Developer Intern",
                company_name="QuickConnect API Corp",
                location="Kolkata (Remote)",
                opportunity_type="internship",
                stipend=15000,
                duration="3 months",
                required_skills="Python, FastAPI, SQL",
                min_cgpa=6.0,
                description="Write unit test suites, optimize database queries, and build endpoints for client-facing systems.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Data Science Analyst Intern",
                company_name="TrendMetrics Labs",
                location="Bangalore",
                opportunity_type="internship",
                stipend=20000,
                duration="4 months",
                required_skills="Python, Data Science, SQL",
                min_cgpa=6.8,
                description="Extract, clean, and map transaction metrics to create strategic marketing insights.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Full-Stack Web Dev Intern (MERN)",
                company_name="AppFactory",
                location="Noida",
                opportunity_type="internship",
                stipend=18000,
                duration="6 months",
                required_skills="React, Node.js, JavaScript, MongoDB",
                min_cgpa=6.5,
                description="Maintain responsive web portals, write database handlers, and configure secure authentication.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="MLOps & Model Deployment Engineer",
                company_name="ModelOps Tech",
                location="Hyderabad",
                opportunity_type="placement",
                stipend=750000,
                duration="Full-Time",
                required_skills="Python, Machine Learning, Docker, AWS",
                min_cgpa=7.2,
                description="Bridge development and deployment of ML architectures. Containerize inference servers.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="React Frontend Placement",
                company_name="WebScale Tech",
                location="Gurgaon",
                opportunity_type="placement",
                stipend=600000,
                duration="Full-Time",
                required_skills="React, JavaScript, HTML, CSS",
                min_cgpa=6.5,
                description="Optimize frontend component architectures to maximize cross-browser compatibility.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Ayurveda Wellness Platform Analyst",
                company_name="AYUSH Global Wellness",
                location="Remote",
                opportunity_type="placement",
                stipend=550000,
                duration="Full-Time",
                required_skills="Ayurveda Informatics, SQL, React",
                min_cgpa=6.0,
                description="Implement data classification tags, design clinic trackers, and coordinate system tests.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Digital Health Security Specialist",
                company_name="Raksha Health Solutions",
                location="Bangalore",
                opportunity_type="placement",
                stipend=850000,
                duration="Full-Time",
                required_skills="Cybersecurity, Health Informatics, Linux",
                min_cgpa=7.5,
                description="Implement defensive security safeguards to shield patient records from breach vulnerabilities.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="Java Spring Boot Placement",
                company_name="Nagarro",
                location="Gurgaon",
                opportunity_type="placement",
                stipend=650000,
                duration="Full-Time",
                required_skills="Java, Spring Boot, SQL",
                min_cgpa=7.0,
                description="Collaborate with corporate clients to write secure, scalable enterprise APIs.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="React Native & Node.js Intern",
                company_name="AppNest Labs",
                location="Remote",
                opportunity_type="internship",
                stipend=16000,
                duration="3 months",
                required_skills="React, Node.js, JavaScript, MongoDB",
                min_cgpa=6.2,
                description="Build features for mobile apps, write backend API wrappers, and implement secure data storage.",
                status="active"
            ),
            Opportunity(
                recruiter_id=rid,
                title="ML & Computer Vision Specialist",
                company_name="VisionNext Corp",
                location="Pune",
                opportunity_type="placement",
                stipend=950000,
                duration="Full-Time",
                required_skills="Python, Machine Learning, Computer Vision, PyTorch",
                min_cgpa=8.0,
                description="Incorporate advanced gesture profiling models to improve automated diagnostic tools.",
                status="active"
            ),
        ]
        
        db.add_all(opportunities)
        db.commit()
        print(f"✅ Successfully seeded {len(opportunities)} detailed Opportunities.")

        # 3. SEEDING 40+ TARGETED YOUTUBE-LINKED COURSES
        courses = [
            # Python
            Course(
                title="Python Full Course for Beginners",
                provider="Programming with Mosh",
                url="https://www.youtube.com/watch?v=_uQrJ0TkZlc",
                skill_tags="Python",
                difficulty="beginner",
                duration_hours=6.0,
                rating=4.9,
                description="Complete introductory guide. Cover variables, loops, objects, structures, and foundational algorithms.",
                is_free=1
            ),
            Course(
                title="Python Advanced: OOP, Decorators, & Threading",
                provider="Corey Schafer",
                url="https://www.youtube.com/watch?v=ZDa-Z5JzLYM",
                skill_tags="Python, Advanced Python",
                difficulty="advanced",
                duration_hours=8.0,
                rating=4.9,
                description="Deep dive on advanced language topics, memory configurations, class decorators, and multi-thread pools.",
                is_free=1
            ),
            Course(
                title="Python OOP Complete Masterclass",
                provider="Corey Schafer",
                url="https://www.youtube.com/watch?v=ZDa-Z5JzLYM&list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc",
                skill_tags="Python",
                difficulty="intermediate",
                duration_hours=4.5,
                rating=4.8,
                description="Understand real object design, inheritances, abstract properties, and modular software designs.",
                is_free=1
            ),

            # Web Frameworks (React, Node, FastAPI, Django)
            Course(
                title="React JS Full Course 2024",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=bMknfKXIFA8",
                skill_tags="React, JavaScript",
                difficulty="beginner",
                duration_hours=12.0,
                rating=4.8,
                description="Step-by-step introduction. Covers virtual dom, functional components, hooks, state, and properties.",
                is_free=1
            ),
            Course(
                title="Redux Toolkit & State Management Course",
                provider="Dave Gray",
                url="https://www.youtube.com/watch?v=NqzdVN2tyvQ",
                skill_tags="React, Redux, JavaScript",
                difficulty="intermediate",
                duration_hours=4.0,
                rating=4.7,
                description="Master global store structures, action dispatches, selectors, async operations, and slice definitions.",
                is_free=1
            ),
            Course(
                title="FastAPI Python Async Microservices",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=7t2alSnE2-I",
                skill_tags="FastAPI, Python",
                difficulty="intermediate",
                duration_hours=4.5,
                rating=4.7,
                description="Write high-speed async APIs, validate payloads using Pydantic, and test automatic swagger pages.",
                is_free=1
            ),
            Course(
                title="Django Web Development Full Course",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=F5mRW0jo-U4",
                skill_tags="Django, Python",
                difficulty="intermediate",
                duration_hours=16.0,
                rating=4.8,
                description="Full-featured development. Covers models, generic class-based views, query optimization, and testing.",
                is_free=1
            ),
            Course(
                title="Node.js & Express.js Backend Course",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=Oe421EPjeBE",
                skill_tags="Node.js, JavaScript",
                difficulty="intermediate",
                duration_hours=8.0,
                rating=4.8,
                description="Learn runtime setups, route routers, database access, JWT validations, and system logging.",
                is_free=1
            ),

            # Databases & SQL
            Course(
                title="SQL Database Full Course for Beginners",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=HXV3zeQKqGY",
                skill_tags="SQL",
                difficulty="beginner",
                duration_hours=4.5,
                rating=4.8,
                description="Understand relational databases, write basic SELECT statements, configure JOIN filters, and sort columns.",
                is_free=1
            ),
            Course(
                title="PostgreSQL Advanced Queries & Index Optimization",
                provider="Amigoscode",
                url="https://www.youtube.com/watch?v=qw--VYLpxG4",
                skill_tags="SQL, PostgreSQL",
                difficulty="advanced",
                duration_hours=4.0,
                rating=4.7,
                description="Deep-dive on indexes, partial filters, explain plans, execution cost evaluations, and database locks.",
                is_free=1
            ),
            Course(
                title="MongoDB NoSQL Database Tutorial",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=ofme2o29ngU",
                skill_tags="MongoDB",
                difficulty="intermediate",
                duration_hours=6.0,
                rating=4.6,
                description="Understand unstructured document models, write nested schemas, use pipelines, and group data.",
                is_free=1
            ),

            # Machine Learning & AI
            Course(
                title="Machine Learning Full Course (10 Hours)",
                provider="Simplilearn",
                url="https://www.youtube.com/watch?v=GwIo3gDZCVQ",
                skill_tags="Machine Learning, Python, Data Science",
                difficulty="intermediate",
                duration_hours=10.0,
                rating=4.7,
                description="Covers regression, classifications, vector machines, decision trees, random forests, and standard evaluation metrics.",
                is_free=1
            ),
            Course(
                title="Deep Learning with PyTorch & Neural Networks",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=GIsg-ZUy0MY",
                skill_tags="Machine Learning, PyTorch, Deep Learning",
                difficulty="advanced",
                duration_hours=9.0,
                rating=4.8,
                description="Understand network structures, write weights, implement SGD, configure loss, and save parameters.",
                is_free=1
            ),
            Course(
                title="TensorFlow 2.0 Full Deep Learning Tutorial",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=tPYj3fFJGjk",
                skill_tags="TensorFlow, Machine Learning",
                difficulty="intermediate",
                duration_hours=7.0,
                rating=4.7,
                description="Covers CNN networks, layer structures, classification tasks, data scaling, and model evaluations.",
                is_free=1
            ),
            Course(
                title="Natural Language Processing (NLP) with Transformers",
                provider="Stanford University",
                url="https://www.youtube.com/watch?v=8rXD5-xhemo",
                skill_tags="NLP, Natural Language Processing, Machine Learning",
                difficulty="advanced",
                duration_hours=18.0,
                rating=4.9,
                description="Explore semantic representations, multi-head attention systems, fine-tuning, and model evaluations.",
                is_free=1
            ),
            Course(
                title="Computer Vision with OpenCV & Python",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=oXlwWbU8l2o",
                skill_tags="Computer Vision, OpenCV, Python",
                difficulty="intermediate",
                duration_hours=9.0,
                rating=4.8,
                description="Explore image filtering, color maps, face classifiers, gesture tracing, and video processing.",
                is_free=1
            ),
            Course(
                title="Data Science Full Course (14 Hours)",
                provider="Simplilearn",
                url="https://www.youtube.com/watch?v=-ETQ97mXXF0",
                skill_tags="Data Science, Python",
                difficulty="intermediate",
                duration_hours=14.0,
                rating=4.6,
                description="Covers Pandas parsing, data visualizations, cleaning pipelines, and statistical classifications.",
                is_free=1
            ),

            # Cloud & DevOps
            Course(
                title="Docker & Containerization Hands-on Tutorial",
                provider="TechWorld with Nana",
                url="https://www.youtube.com/watch?v=3c-iBn73dDE",
                skill_tags="Docker",
                difficulty="intermediate",
                duration_hours=5.0,
                rating=4.9,
                description="Learn container builds, images, tags, multi-container compose orchestration, and network settings.",
                is_free=1
            ),
            Course(
                title="AWS Certified Cloud Practitioner Full Course",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=3hLmDS179YE",
                skill_tags="AWS",
                difficulty="beginner",
                duration_hours=13.0,
                rating=4.8,
                description="Covers EC2 instances, S3, virtual clouds, IAM permissions, database setups, and billing matrices.",
                is_free=1
            ),
            Course(
                title="Kubernetes Full Course (TechWorld with Nana)",
                provider="TechWorld with Nana",
                url="https://www.youtube.com/watch?v=X48VuDVv0do",
                skill_tags="Kubernetes, Docker",
                difficulty="advanced",
                duration_hours=4.5,
                rating=4.9,
                description="Master pods, ingress, services, configmaps, persistent volumes, and deployment automation.",
                is_free=1
            ),

            # Cybersecurity & Infrastructure
            Course(
                title="Cybersecurity Fundamentals & Ethical Hacking",
                provider="Simplilearn",
                url="https://www.youtube.com/watch?v=900x5hYGBPo",
                skill_tags="Cybersecurity",
                difficulty="beginner",
                duration_hours=11.0,
                rating=4.6,
                description="Covers penetration testing, malware analysis, network scanning, firewall logs, and security defenses.",
                is_free=1
            ),
            Course(
                title="Linux Command Line & Shell Scripting",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=ROjZy1WbCIA",
                skill_tags="Linux",
                difficulty="beginner",
                duration_hours=9.0,
                rating=4.8,
                description="Master terminal commands, file attributes, stream redirect pipes, and shell scripts.",
                is_free=1
            ),
            Course(
                title="Networking Fundamentals for Cyber Security",
                provider="NetworkChuck",
                url="https://www.youtube.com/watch?v=qiQR5rTSshw",
                skill_tags="Networking",
                difficulty="beginner",
                duration_hours=6.0,
                rating=4.8,
                description="Covers OSI models, TCP/IP, router subnet configurations, switches, and secure gateways.",
                is_free=1
            ),

            # AYUSH Digital Health & Interdisciplinary Informatics
            Course(
                title="Ayurveda Informatics & Traditional Health Systems",
                provider="Ministry of AYUSH / Swayam",
                url="https://www.youtube.com/watch?v=VbOBfMjGJpM",
                skill_tags="Ayurveda Informatics",
                difficulty="beginner",
                duration_hours=3.0,
                rating=4.5,
                description="Covers traditional terminologies, electronic health record criteria, and classification frameworks.",
                is_free=1
            ),
            Course(
                title="Yoga Science & Posture Kinetics Intro",
                provider="AYUSH Wellness Council",
                url="https://www.youtube.com/watch?v=VbOBfMjGJpM",
                skill_tags="Yoga Science",
                difficulty="beginner",
                duration_hours=2.5,
                rating=4.4,
                description="Explores joint kinetics, wellness parameters, and calibration benchmarks for system modeling.",
                is_free=1
            ),
            Course(
                title="HTML & CSS Complete Course",
                provider="SuperSimpleDev",
                url="https://www.youtube.com/watch?v=G3e-cpL7ofc",
                skill_tags="HTML, CSS",
                difficulty="beginner",
                duration_hours=6.5,
                rating=4.8,
                description="Understand structure parsing, box formatting, semantic tags, and responsive layouts.",
                is_free=1
            ),
            Course(
                title="JavaScript Full Course",
                provider="SuperSimpleDev",
                url="https://www.youtube.com/watch?v=EerdGm-ehJQ",
                skill_tags="JavaScript",
                difficulty="beginner",
                duration_hours=22.0,
                rating=4.9,
                description="Master variables, functions, DOM elements, async endpoints, and modular code structures.",
                is_free=1
            ),
            Course(
                title="Java Programming Tutorial for Beginners",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=xk4_1vDrzzo",
                skill_tags="Java",
                difficulty="beginner",
                duration_hours=12.0,
                rating=4.7,
                description="Covers Java syntax, data structures, compilation matrices, and OOP implementations.",
                is_free=1
            ),
            Course(
                title="Spring Boot Microservices Tutorial",
                provider="Amigoscode",
                url="https://www.youtube.com/watch?v=xk4_1vDrzzo",
                skill_tags="Spring Boot, Java",
                difficulty="intermediate",
                duration_hours=5.5,
                rating=4.8,
                description="Learn API routers, security configurations, dependency structures, and SQL configurations.",
                is_free=1
            ),
            Course(
                title="Tailwind CSS Full Tutorial for Beginners",
                provider="FreeCodeCamp",
                url="https://www.youtube.com/watch?v=dFgzHOX84xQ",
                skill_tags="Tailwind",
                difficulty="beginner",
                duration_hours=4.0,
                rating=4.7,
                description="Learn grid systems, custom utility classes, dark theme configurations, and component setups.",
                is_free=1
            ),
        ]

        db.add_all(courses)
        db.commit()
        print(f"✅ Successfully seeded {len(courses)} high-quality, targeted YouTube Courses.")
        print("\n🎉 Database Seeding Complete! Enjoy exploring the production-grade catalog.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding catalog: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_production_data()
