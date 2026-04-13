from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from board.models import Company, Job

User = get_user_model()

COMPANIES = [
    {
        "username": "techcorp_hr",
        "email": "hr@techcorp.io",
        "company_name": "TechCorp Solutions",
        "website": "https://www.techcorp.io",
        "location": "San Francisco, CA",
    },
    {
        "username": "nova_systems",
        "email": "jobs@novasystems.com",
        "company_name": "Nova Systems",
        "website": "https://www.novasystems.com",
        "location": "New York, NY",
    },
    {
        "username": "bluewave_agency",
        "email": "careers@bluewave.agency",
        "company_name": "Bluewave Digital Agency",
        "website": "https://www.bluewave.agency",
        "location": "Austin, TX",
    },
    {
        "username": "greenpath_labs",
        "email": "hr@greenpathlabs.com",
        "company_name": "GreenPath Labs",
        "website": "https://www.greenpathlabs.com",
        "location": "Seattle, WA",
    },
    {
        "username": "skyline_ventures",
        "email": "talent@skylineventures.com",
        "company_name": "Skyline Ventures",
        "website": "https://www.skylineventures.com",
        "location": "Chicago, IL",
    },
]

JOBS = [
    {
        "company_index": 0,
        "title": "Senior Backend Engineer",
        "description": (
            "We are looking for a Senior Backend Engineer to join our growing engineering team at TechCorp Solutions. "
            "In this role, you will design, build, and maintain scalable APIs and microservices that power our core platform.\n\n"
            "Responsibilities:\n"
            "- Architect and implement RESTful and GraphQL APIs using Python (Django/FastAPI)\n"
            "- Collaborate with frontend engineers and product managers to deliver features\n"
            "- Optimize database queries and ensure high availability of services\n"
            "- Participate in code reviews and mentor junior engineers\n"
            "- Drive technical decisions and contribute to engineering roadmap\n\n"
            "Requirements:\n"
            "- 5+ years of backend development experience\n"
            "- Strong proficiency in Python and at least one ORM (SQLAlchemy, Django ORM)\n"
            "- Experience with PostgreSQL and Redis\n"
            "- Familiarity with Docker and Kubernetes\n"
            "- Excellent communication and problem-solving skills\n\n"
            "What we offer:\n"
            "- Competitive salary and equity package\n"
            "- Fully remote-friendly environment\n"
            "- Health, dental, and vision insurance\n"
            "- $2,000 annual learning & development budget"
        ),
        "salary": 145000,
        "location": "San Francisco, CA",
        "job_type": "remote",
        "employment_type": "full_time",
    },
    {
        "company_index": 0,
        "title": "DevOps Engineer",
        "description": (
            "TechCorp Solutions is seeking a skilled DevOps Engineer to help us scale our infrastructure and improve our CI/CD pipelines.\n\n"
            "Responsibilities:\n"
            "- Manage and improve our cloud infrastructure on AWS\n"
            "- Build and maintain CI/CD pipelines using GitHub Actions and Jenkins\n"
            "- Monitor system health and respond to incidents\n"
            "- Automate repetitive operational tasks using Terraform and Ansible\n"
            "- Collaborate with developers to ensure smooth deployments\n\n"
            "Requirements:\n"
            "- 3+ years of experience in DevOps or SRE roles\n"
            "- Hands-on experience with AWS (EC2, RDS, EKS, S3)\n"
            "- Proficiency with Docker and Kubernetes\n"
            "- Experience with infrastructure-as-code tools (Terraform)\n"
            "- Strong Linux/Unix administration skills\n\n"
            "Nice to have:\n"
            "- AWS certifications\n"
            "- Experience with Datadog or Prometheus/Grafana"
        ),
        "salary": 130000,
        "location": "San Francisco, CA",
        "job_type": "hybrid",
        "employment_type": "full_time",
    },
    {
        "company_index": 1,
        "title": "Full Stack Developer",
        "description": (
            "Nova Systems is hiring a Full Stack Developer to help build the next generation of our enterprise SaaS platform.\n\n"
            "Responsibilities:\n"
            "- Develop and maintain features across the full stack (React frontend + Node.js backend)\n"
            "- Write clean, well-tested code following best practices\n"
            "- Work closely with UX designers to implement responsive UI components\n"
            "- Participate in agile sprints, daily standups, and retrospectives\n"
            "- Contribute to system architecture discussions\n\n"
            "Requirements:\n"
            "- 3+ years of experience with React and TypeScript\n"
            "- 3+ years of experience with Node.js and Express or NestJS\n"
            "- Solid understanding of REST API design\n"
            "- Experience with relational databases (PostgreSQL or MySQL)\n"
            "- Familiarity with Git and agile workflows\n\n"
            "Benefits:\n"
            "- Flexible working hours\n"
            "- 20 days PTO + public holidays\n"
            "- Monthly wellness stipend"
        ),
        "salary": 120000,
        "location": "New York, NY",
        "job_type": "hybrid",
        "employment_type": "full_time",
    },
    {
        "company_index": 1,
        "title": "Data Analyst Intern",
        "description": (
            "Join Nova Systems as a Data Analyst Intern and gain hands-on experience working with real business data.\n\n"
            "What you'll do:\n"
            "- Assist the analytics team in collecting, cleaning, and analyzing datasets\n"
            "- Build dashboards and reports using Tableau or Power BI\n"
            "- Identify trends and present insights to stakeholders\n"
            "- Write SQL queries to extract data from our data warehouse\n\n"
            "Requirements:\n"
            "- Currently pursuing a degree in Data Science, Statistics, Computer Science, or related field\n"
            "- Familiarity with SQL and Excel\n"
            "- Basic knowledge of Python (pandas, matplotlib) is a plus\n"
            "- Strong analytical and communication skills\n\n"
            "Duration: 3 months (with possibility of extension)\n"
            "Stipend: $2,500/month"
        ),
        "salary": 2500,
        "location": "New York, NY",
        "job_type": "on_site",
        "employment_type": "internship",
    },
    {
        "company_index": 2,
        "title": "UI/UX Designer",
        "description": (
            "Bluewave Digital Agency is looking for a creative and user-centric UI/UX Designer to lead the design of web and mobile products for our clients.\n\n"
            "Responsibilities:\n"
            "- Conduct user research and translate insights into design solutions\n"
            "- Create wireframes, prototypes, and high-fidelity mockups in Figma\n"
            "- Collaborate with developers to ensure accurate implementation\n"
            "- Maintain and expand design systems and component libraries\n"
            "- Present design concepts to clients and incorporate feedback\n\n"
            "Requirements:\n"
            "- 3+ years of UI/UX design experience\n"
            "- Expert-level proficiency in Figma\n"
            "- Strong portfolio demonstrating web and mobile design work\n"
            "- Understanding of accessibility standards (WCAG)\n"
            "- Excellent visual design skills and attention to detail\n\n"
            "Nice to have:\n"
            "- Experience with motion design (Lottie, After Effects)\n"
            "- Basic knowledge of HTML/CSS"
        ),
        "salary": 95000,
        "location": "Austin, TX",
        "job_type": "remote",
        "employment_type": "full_time",
    },
    {
        "company_index": 2,
        "title": "Digital Marketing Specialist",
        "description": (
            "Bluewave Digital Agency is looking for a results-driven Digital Marketing Specialist to manage paid and organic campaigns for our portfolio of clients.\n\n"
            "Responsibilities:\n"
            "- Plan, execute, and optimize Google Ads, Meta Ads, and LinkedIn campaigns\n"
            "- Manage SEO strategy including on-page and off-page optimization\n"
            "- Analyze campaign performance and produce weekly/monthly reports\n"
            "- Collaborate with the content team to develop marketing materials\n"
            "- Manage email marketing campaigns via Mailchimp or HubSpot\n\n"
            "Requirements:\n"
            "- 2+ years of digital marketing experience\n"
            "- Proficiency in Google Analytics, Google Ads, and Meta Business Manager\n"
            "- Strong understanding of SEO principles\n"
            "- Data-driven mindset with experience in A/B testing\n"
            "- Excellent copywriting and communication skills\n\n"
            "Benefits:\n"
            "- Fully remote position\n"
            "- Performance bonuses\n"
            "- Access to top marketing tools and courses"
        ),
        "salary": 72000,
        "location": "Remote",
        "job_type": "remote",
        "employment_type": "full_time",
    },
    {
        "company_index": 3,
        "title": "Machine Learning Engineer",
        "description": (
            "GreenPath Labs is pioneering sustainable technology solutions powered by AI. We are looking for a Machine Learning Engineer to join our research team.\n\n"
            "Responsibilities:\n"
            "- Design and train ML models for environmental data analysis\n"
            "- Build data pipelines and feature engineering workflows\n"
            "- Deploy models to production using MLflow and cloud infrastructure\n"
            "- Collaborate with domain experts to frame problems and validate results\n"
            "- Stay current with the latest research in ML and AI\n\n"
            "Requirements:\n"
            "- 4+ years of experience in machine learning or data science\n"
            "- Strong Python skills (scikit-learn, PyTorch or TensorFlow)\n"
            "- Experience with MLOps and model deployment\n"
            "- Proficiency in SQL and data wrangling\n"
            "- Published research or open-source contributions are a plus\n\n"
            "What we offer:\n"
            "- Mission-driven work with real-world impact\n"
            "- Competitive compensation + equity\n"
            "- Remote-first culture with quarterly team retreats"
        ),
        "salary": 155000,
        "location": "Seattle, WA",
        "job_type": "remote",
        "employment_type": "full_time",
    },
    {
        "company_index": 3,
        "title": "Environmental Data Scientist (Contract)",
        "description": (
            "GreenPath Labs is seeking a contract Data Scientist to support a 6-month project focused on climate data modeling and reporting.\n\n"
            "Project scope:\n"
            "- Analyze large-scale environmental datasets (temperature, emissions, land use)\n"
            "- Build predictive models to forecast climate impact scenarios\n"
            "- Produce visualizations and reports for government stakeholders\n"
            "- Document methodology and ensure reproducibility\n\n"
            "Requirements:\n"
            "- Demonstrated experience in environmental or climate data analysis\n"
            "- Proficiency in Python or R for statistical modeling\n"
            "- Experience with geospatial data (GIS, GDAL, shapely)\n"
            "- Strong written communication skills\n\n"
            "Contract details:\n"
            "- Duration: 6 months\n"
            "- Rate: $90–$110/hour depending on experience\n"
            "- Fully remote"
        ),
        "salary": 90000,
        "location": "Remote",
        "job_type": "remote",
        "employment_type": "contract",
    },
    {
        "company_index": 4,
        "title": "Product Manager",
        "description": (
            "Skyline Ventures is looking for an experienced Product Manager to lead the development of our flagship B2B SaaS product.\n\n"
            "Responsibilities:\n"
            "- Define and communicate product vision, strategy, and roadmap\n"
            "- Gather and prioritize requirements from customers, sales, and stakeholders\n"
            "- Work closely with engineering and design teams to deliver features on time\n"
            "- Track key product metrics and use data to drive decisions\n"
            "- Conduct market research and competitive analysis\n\n"
            "Requirements:\n"
            "- 4+ years of product management experience in a SaaS company\n"
            "- Proven track record of launching successful products\n"
            "- Strong analytical skills and comfort with data (SQL, Mixpanel, Amplitude)\n"
            "- Excellent stakeholder management and communication abilities\n"
            "- Experience working in agile/scrum environments\n\n"
            "Benefits:\n"
            "- Base salary + bonus + equity\n"
            "- Comprehensive health benefits\n"
            "- Flexible hybrid work model"
        ),
        "salary": 135000,
        "location": "Chicago, IL",
        "job_type": "hybrid",
        "employment_type": "full_time",
    },
    {
        "company_index": 4,
        "title": "Customer Success Manager",
        "description": (
            "Skyline Ventures is looking for a proactive Customer Success Manager to ensure our enterprise clients achieve their goals with our platform.\n\n"
            "Responsibilities:\n"
            "- Serve as the primary point of contact for a portfolio of 30–50 enterprise accounts\n"
            "- Conduct onboarding, training sessions, and quarterly business reviews\n"
            "- Monitor customer health scores and proactively address churn risk\n"
            "- Collaborate with the sales team on renewal and upsell opportunities\n"
            "- Collect and relay product feedback to the product team\n\n"
            "Requirements:\n"
            "- 2+ years of customer success or account management experience (SaaS preferred)\n"
            "- Excellent communication and relationship-building skills\n"
            "- Ability to manage multiple accounts and priorities simultaneously\n"
            "- Comfort with CRM tools (Salesforce, HubSpot)\n"
            "- Empathetic and customer-first mindset\n\n"
            "Benefits:\n"
            "- Competitive base + performance bonuses\n"
            "- On-site office in downtown Chicago\n"
            "- Team events and annual company retreat"
        ),
        "salary": 85000,
        "location": "Chicago, IL",
        "job_type": "on_site",
        "employment_type": "full_time",
    },
    {
        "company_index": 0,
        "title": "Frontend Engineer (React)",
        "description": (
            "TechCorp Solutions is growing its frontend team! We are looking for a talented React engineer who cares deeply about user experience and code quality.\n\n"
            "Responsibilities:\n"
            "- Build and maintain performant, accessible React components\n"
            "- Work with designers to translate Figma mockups into pixel-perfect UI\n"
            "- Write unit and integration tests using Jest and React Testing Library\n"
            "- Participate in code reviews and technical design discussions\n"
            "- Contribute to our internal component library\n\n"
            "Requirements:\n"
            "- 3+ years of professional React experience\n"
            "- Strong TypeScript skills\n"
            "- Familiarity with state management (Redux, Zustand, or React Query)\n"
            "- Understanding of web performance optimization\n"
            "- Experience with testing frameworks\n\n"
            "Nice to have:\n"
            "- Experience with Next.js\n"
            "- Contributions to open-source projects"
        ),
        "salary": 115000,
        "location": "San Francisco, CA",
        "job_type": "remote",
        "employment_type": "full_time",
    },
    {
        "company_index": 2,
        "title": "Content Writer (Part-time)",
        "description": (
            "Bluewave Digital Agency is seeking a talented Content Writer to create engaging content for our clients across various industries.\n\n"
            "Responsibilities:\n"
            "- Write blog posts, articles, landing page copy, and social media content\n"
            "- Research industry topics to produce accurate and insightful content\n"
            "- Optimize content for SEO using keywords and best practices\n"
            "- Meet deadlines and manage multiple writing projects simultaneously\n"
            "- Collaborate with the design team on creative assets\n\n"
            "Requirements:\n"
            "- Proven writing portfolio (blog posts, articles, or copywriting samples)\n"
            "- Strong command of English grammar and style\n"
            "- Basic understanding of SEO principles\n"
            "- Ability to adapt tone and voice for different brands\n\n"
            "Details:\n"
            "- Part-time: 20 hours/week\n"
            "- Fully remote\n"
            "- Pay: $35–$50/hour"
        ),
        "salary": 35000,
        "location": "Remote",
        "job_type": "remote",
        "employment_type": "part_time",
    },
]


class Command(BaseCommand):
    help = "Seed the database with realistic job listings and company accounts."

    def handle(self, *args, **options):
        self.stdout.write("Seeding companies...")
        company_objects = []

        for c in COMPANIES:
            user, created = User.objects.get_or_create(
                username=c["username"],
                defaults={"email": c["email"], "role": "COMPANY"},
            )
            if created:
                user.set_password("password123")
                user.save()

            company, _ = Company.objects.get_or_create(
                user=user,
                defaults={
                    "email": c["email"],
                    "company_name": c["company_name"],
                    "website": c["website"],
                    "location": c["location"],
                },
            )
            company_objects.append(company)
            self.stdout.write(f"  Company ready: {company.company_name}")

        self.stdout.write("Seeding jobs...")
        created_count = 0
        for j in JOBS:
            company = company_objects[j["company_index"]]
            job, created = Job.objects.get_or_create(
                company=company,
                title=j["title"],
                defaults={
                    "description": j["description"],
                    "salary": j["salary"],
                    "location": j["location"],
                    "job_type": j["job_type"],
                    "employment_type": j["employment_type"],
                    "is_active": True,
                },
            )
            if created:
                created_count += 1
                self.stdout.write(f"  Created job: {job.title} @ {company.company_name}")
            else:
                self.stdout.write(f"  Already exists: {job.title} @ {company.company_name}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! {created_count} new job(s) created across {len(company_objects)} companies."
        ))
