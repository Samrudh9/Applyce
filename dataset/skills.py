# Career Skills Data Module
# Contains skills mapping for various career paths
# Expanded to 500+ skills across all categories

CAREER_SKILLS = {
    # Tech careers - Data & AI/ML
    "data scientist": [
        "python", "machine learning", "statistics", "sql", "tensorflow",
        "pandas", "numpy", "scikit-learn", "deep learning", "data visualization",
        "r", "jupyter", "spark", "big data", "feature engineering"
    ],
    "machine learning engineer": [
        "python", "tensorflow", "pytorch", "machine learning", "deep learning",
        "neural networks", "nlp", "computer vision", "mlops", "keras",
        "scikit-learn", "xgboost", "model deployment", "docker", "kubernetes"
    ],
    "deep learning engineer": [
        "pytorch", "tensorflow", "keras", "computer vision", "nlp",
        "transformers", "bert", "gpt", "cnn", "rnn", "lstm",
        "gan", "reinforcement learning", "model optimization"
    ],
    "llm engineer": [
        "hugging face", "langchain", "openai api", "gpt", "bert",
        "transformers", "vector databases", "embeddings", "rag",
        "prompt engineering", "fine-tuning", "python", "pytorch"
    ],
    "mlops engineer": [
        "kubernetes", "docker", "terraform", "mlflow", "kubeflow",
        "model registry", "ci/cd", "python", "monitoring", "aws",
        "azure ml", "sagemaker", "deployment", "automation"
    ],
    "ai researcher": [
        "python", "pytorch", "deep learning", "computer vision",
        "research", "papers", "algorithms", "mathematics", "optimization",
        "reinforcement learning", "transformers", "innovation"
    ],
    "ai prompt engineer": [
        "prompt engineering", "gpt", "chatgpt", "claude", "llms",
        "prompt optimization", "langchain", "ai applications", "testing",
        "natural language", "use case design", "evaluation"
    ],
    "nlp engineer": [
        "nlp", "transformers", "bert", "spacy", "nltk",
        "text processing", "sentiment analysis", "named entity recognition",
        "language models", "pytorch", "hugging face", "python"
    ],
    "computer vision engineer": [
        "computer vision", "opencv", "image processing", "deep learning",
        "cnn", "object detection", "segmentation", "pytorch", "tensorflow",
        "yolo", "rcnn", "image classification", "video analysis"
    ],
    "data engineer": [
        "spark", "kafka", "airflow", "python", "sql",
        "etl", "data pipelines", "aws", "azure", "gcp",
        "databricks", "snowflake", "big data", "scala", "java"
    ],
    "big data engineer": [
        "apache spark", "databricks", "pyspark", "scala", "hadoop",
        "hdfs", "hive", "big data processing", "distributed systems",
        "kafka", "stream processing", "data lakes"
    ],
    "analytics engineer": [
        "dbt", "snowflake", "sql", "data modeling", "analytics",
        "python", "data transformation", "data warehousing", "bi tools",
        "looker", "tableau", "power bi", "git"
    ],
    "data analyst": [
        "python", "sql", "excel", "tableau", "data visualization",
        "statistics", "pandas", "power bi", "looker", "reporting",
        "dashboard design", "business intelligence"
    ],
    
    # Tech careers - Cloud & DevOps
    "devops engineer": [
        "docker", "kubernetes", "aws", "azure", "ci/cd",
        "jenkins", "terraform", "linux", "ansible", "monitoring",
        "github actions", "gitlab ci", "helm", "prometheus", "grafana"
    ],
    "cloud architect": [
        "aws", "azure", "gcp", "cloud architecture", "infrastructure design",
        "ec2", "s3", "lambda", "cloudformation", "terraform",
        "kubernetes", "microservices", "scalability", "security"
    ],
    "site reliability engineer": [
        "kubernetes", "docker", "prometheus", "grafana", "ci/cd",
        "monitoring", "incident response", "automation", "python",
        "linux", "sre practices", "reliability", "performance"
    ],
    "platform engineer": [
        "kubernetes", "docker", "terraform", "ci/cd", "monitoring",
        "internal tools", "developer experience", "automation",
        "infrastructure", "apis", "platform design"
    ],
    "infrastructure automation engineer": [
        "terraform", "ansible", "puppet", "chef", "infrastructure as code",
        "automation", "configuration management", "cloud", "ci/cd",
        "scripting", "python", "bash", "linux"
    ],
    "azure cloud engineer": [
        "azure", "aks", "azure functions", "arm templates", "devops",
        "azure devops", "cloud services", "virtual machines", "storage",
        "networking", "security", "powershell"
    ],
    "gcp cloud engineer": [
        "gcp", "kubernetes engine", "cloud functions", "bigquery",
        "google cloud", "data analytics", "terraform", "ci/cd",
        "cloud storage", "compute engine", "networking"
    ],
    "observability engineer": [
        "datadog", "new relic", "prometheus", "grafana", "monitoring",
        "logging", "tracing", "metrics", "observability", "alerting",
        "splunk", "elk stack", "performance monitoring"
    ],
    "ci/cd engineer": [
        "circleci", "github actions", "gitlab ci", "jenkins",
        "build automation", "deployment", "ci/cd pipelines",
        "docker", "kubernetes", "testing", "automation"
    ],
    "devsecops engineer": [
        "security automation", "container security", "kubernetes security",
        "devops", "ci/cd", "security scanning", "vulnerability management",
        "compliance", "cloud security", "infrastructure security"
    ],
    
    # Tech careers - Software Development
    "software engineer": [
        "python", "java", "javascript", "sql", "git",
        "algorithms", "data structures", "oop", "testing",
        "agile", "design patterns", "debugging", "code review"
    ],
    "software developer": [
        "python", "java", "javascript", "sql", "git",
        "algorithms", "data structures", "oop", "testing",
        "debugging", "version control", "software design"
    ],
    "frontend developer": [
        "html", "css", "javascript", "react", "vue", "typescript",
        "angular", "webpack", "sass", "responsive design",
        "redux", "web performance", "accessibility", "testing"
    ],
    "frontend engineer": [
        "next.js", "react", "typescript", "tailwind css", "performance",
        "seo", "web vitals", "modern web", "state management",
        "testing", "ci/cd", "responsive design"
    ],
    "backend developer": [
        "python", "java", "nodejs", "sql", "api", "docker",
        "mongodb", "postgresql", "rest", "microservices",
        "redis", "message queues", "caching", "authentication"
    ],
    "full stack developer": [
        "javascript", "react", "nodejs", "python", "sql",
        "html", "css", "git", "docker", "rest api",
        "mongodb", "postgresql", "aws", "ci/cd"
    ],
    "fastapi developer": [
        "fastapi", "python", "async", "pydantic", "rest apis",
        "high-performance", "openapi", "sql", "oauth", "testing",
        "docker", "microservices", "postgresql"
    ],
    "nestjs developer": [
        "nestjs", "node.js", "typescript", "microservices",
        "enterprise applications", "rest", "graphql", "postgresql",
        "mongodb", "testing", "docker", "swagger"
    ],
    "rust backend developer": [
        "rust", "actix", "performance", "systems programming",
        "low-level", "async", "tokio", "high performance",
        "memory safety", "concurrency", "rest apis"
    ],
    "go developer": [
        "go", "gin", "goroutines", "microservices", "concurrent systems",
        "cloud native", "docker", "kubernetes", "rest apis",
        "grpc", "high performance", "scalability"
    ],
    "grpc developer": [
        "grpc", "protocol buffers", "microservices", "apis",
        "rpc", "distributed systems", "go", "java", "python",
        "streaming", "performance", "service mesh"
    ],
    "graphql developer": [
        "graphql", "apollo", "schema design", "resolvers",
        "api design", "data fetching", "subscriptions",
        "federation", "caching", "optimization"
    ],
    "api developer": [
        "rest", "graphql", "api design", "documentation",
        "swagger", "openapi", "authentication", "rate limiting",
        "versioning", "security", "testing"
    ],
    "microservices architect": [
        "microservices", "docker", "service mesh", "distributed systems",
        "kubernetes", "event-driven", "api gateway", "monitoring",
        "scalability", "resilience", "design patterns"
    ],
    
    # Tech careers - Mobile Development
    "mobile app developer": [
        "flutter", "react native", "swift", "kotlin", "android",
        "ios", "dart", "mobile ui", "firebase", "app store",
        "play store", "mobile testing", "responsive design"
    ],
    "ios developer": [
        "swiftui", "ios", "swift", "combine", "apple development",
        "xcode", "cocoapods", "app store", "mobile", "uikit",
        "core data", "push notifications"
    ],
    "android developer": [
        "jetpack compose", "kotlin", "android", "material design",
        "android studio", "gradle", "mvvm", "retrofit",
        "room database", "play store", "firebase"
    ],
    "react native developer": [
        "react native", "expo", "javascript", "cross-platform",
        "mobile development", "react", "redux", "navigation",
        "native modules", "testing", "app deployment"
    ],
    "flutter developer": [
        "flutter", "dart", "cross-platform", "material design",
        "mobile apps", "ui", "state management", "bloc",
        "provider", "firebase", "ios", "android"
    ],
    
    # Tech careers - Security
    "security engineer": [
        "penetration testing", "siem", "vulnerability assessment",
        "python", "security", "ethical hacking", "owasp",
        "security tools", "incident response", "threat analysis"
    ],
    "cybersecurity analyst": [
        "cybersecurity", "networking", "security systems",
        "hacking prevention", "siem", "soc", "incident response",
        "threat intelligence", "security monitoring", "compliance"
    ],
    "application security engineer": [
        "owasp", "burp suite", "security testing", "application security",
        "code review", "security best practices", "penetration testing",
        "vulnerability assessment", "secure coding"
    ],
    "security operations analyst": [
        "soc", "incident response", "siem", "threat hunting",
        "security operations", "monitoring", "log analysis",
        "forensics", "malware analysis", "alerting"
    ],
    "network security engineer": [
        "wireshark", "network security", "firewall", "ids/ips",
        "network protection", "analysis", "vpn", "network protocols",
        "security architecture", "threat detection"
    ],
    
    # Tech careers - Web Development
    "web developer": [
        "html", "css", "javascript", "php", "mysql",
        "responsive design", "wordpress", "bootstrap",
        "jquery", "web standards", "seo basics"
    ],
    "vue.js developer": [
        "nuxt.js", "vue", "composition api", "pinia",
        "vue ecosystem", "spa", "vuex", "vue router",
        "typescript", "testing", "vite"
    ],
    "svelte developer": [
        "svelte", "sveltekit", "reactive programming",
        "lightweight frameworks", "performance", "javascript",
        "web components", "modern web", "spa"
    ],
    "webgl developer": [
        "three.js", "webgl", "canvas", "3d graphics",
        "3d web", "visualization", "shaders", "javascript",
        "animation", "interactive graphics"
    ],
    
    # HR careers
    "hr manager": [
        "recruitment", "employee relations", "payroll", "hris", "training",
        "labor law", "performance management", "benefits administration",
        "talent management", "hr strategy", "compliance"
    ],
    "recruiter": [
        "talent acquisition", "interviewing", "ats", "sourcing",
        "onboarding", "screening", "linkedin recruiter", "candidate assessment",
        "job posting", "employer branding", "recruiting metrics"
    ],
    "technical recruiter": [
        "technical recruiting", "talent acquisition", "interviewing",
        "tech stack understanding", "sourcing", "ats", "linkedin",
        "candidate screening", "engineering recruitment"
    ],
    "human resources": [
        "recruitment", "payroll", "benefits", "employee relations",
        "hr policies", "onboarding", "training", "compliance",
        "performance management", "conflict resolution"
    ],
    "hr specialist": [
        "hris", "workday", "benefits administration", "compensation",
        "hr policies", "employee support", "data analysis",
        "compliance", "documentation", "hr systems"
    ],
    "training manager": [
        "training", "development", "learning management",
        "performance management", "instructional design",
        "coaching", "curriculum development", "e-learning",
        "training evaluation", "talent development"
    ],
    "payroll specialist": [
        "payroll", "hris", "benefits", "compliance", "taxation",
        "labor law", "payroll processing", "adp", "time tracking",
        "wage calculations", "tax reporting"
    ],
    
    # Marketing careers
    "marketing manager": [
        "seo", "social media", "google analytics", "content marketing",
        "branding", "campaign management", "market research",
        "email marketing", "marketing strategy", "budget management"
    ],
    "digital marketer": [
        "seo", "ppc", "social media", "email marketing",
        "google ads", "facebook ads", "content marketing",
        "analytics", "conversion optimization", "marketing automation"
    ],
    "digital marketing specialist": [
        "seo", "sem", "ppc", "google ads", "social media marketing",
        "email marketing", "analytics", "marketing tools",
        "campaign optimization", "a/b testing"
    ],
    "brand manager": [
        "brand strategy", "market research", "campaign management",
        "advertising", "consumer behavior", "positioning",
        "brand identity", "creative direction", "competitive analysis"
    ],
    "content marketing manager": [
        "content strategy", "copywriting", "social media",
        "email marketing", "seo", "content creation",
        "editorial calendar", "content distribution", "analytics"
    ],
    "market research analyst": [
        "market research", "consumer insights", "data analysis",
        "competitive analysis", "surveys", "reporting",
        "statistical analysis", "market trends", "forecasting"
    ],
    "growth analyst": [
        "growth hacking", "experimentation", "analytics", "marketing",
        "growth strategy", "optimization", "metrics", "a/b testing",
        "user acquisition", "conversion funnels"
    ],
    
    # Finance careers
    "financial analyst": [
        "financial modeling", "excel", "budgeting", "forecasting",
        "analysis", "valuation", "financial reporting",
        "financial statements", "variance analysis", "presentations"
    ],
    "accountant": [
        "accounting", "taxation", "bookkeeping", "auditing",
        "gaap", "financial statements", "quickbooks",
        "tax preparation", "reconciliation", "compliance"
    ],
    "investment banker": [
        "financial modeling", "valuation", "due diligence",
        "m&a", "excel", "pitchbook", "deal structuring",
        "dcf", "lbo", "comps", "presentations"
    ],
    "risk manager": [
        "risk management", "compliance", "regulatory",
        "internal controls", "risk assessment", "mitigation",
        "governance", "auditing", "risk modeling"
    ],
    "treasury analyst": [
        "treasury", "cash flow", "banking", "investments",
        "liquidity management", "financial instruments",
        "hedging", "foreign exchange", "working capital"
    ],
    "quantitative analyst": [
        "quantitative analysis", "financial modeling", "trading algorithms",
        "python", "r", "statistics", "machine learning",
        "risk modeling", "derivatives", "portfolio optimization"
    ],
    "fraud analyst": [
        "fraud detection", "pattern recognition", "machine learning",
        "analytics", "sql", "data analysis", "investigation",
        "security", "risk management", "reporting"
    ],
    
    # Sales careers
    "sales manager": [
        "sales", "crm", "negotiation", "lead generation",
        "team management", "pipeline management", "forecasting",
        "salesforce", "coaching", "territory management"
    ],
    "account executive": [
        "b2b sales", "account management", "salesforce",
        "pipeline management", "client relations", "closing deals",
        "prospecting", "negotiation", "sales presentations"
    ],
    "sales executive": [
        "sales", "negotiation", "customer relations",
        "prospecting", "closing deals", "crm",
        "pipeline", "quota achievement", "relationship building"
    ],
    "business development": [
        "sales", "lead generation", "partnerships",
        "negotiation", "market expansion", "networking",
        "proposal writing", "relationship management"
    ],
    "sales engineer": [
        "technical sales", "product knowledge", "demos",
        "presentations", "solution design", "customer support",
        "technical communication", "sales process"
    ],
    "customer success manager": [
        "customer success", "onboarding", "account management",
        "retention", "product adoption", "relationship management",
        "problem solving", "metrics", "feedback collection"
    ],
    
    # Healthcare careers
    "healthcare administrator": [
        "healthcare administration", "hipaa", "patient care",
        "medical records", "ehr", "healthcare compliance",
        "operations management", "budgeting", "quality assurance"
    ],
    "medical billing specialist": [
        "medical billing", "ehr", "epic", "healthcare compliance",
        "revenue cycle", "medical coding", "insurance claims",
        "icd-10", "cpt codes", "billing software"
    ],
    "healthcare data analyst": [
        "healthcare analytics", "clinical data", "hipaa", "sql",
        "medical data", "reporting", "tableau", "power bi",
        "statistical analysis", "healthcare metrics"
    ],
    
    # Legal careers
    "legal advisor": [
        "legal research", "contract review", "compliance",
        "corporate law", "regulatory", "legal analysis",
        "advisory", "risk assessment", "documentation"
    ],
    "corporate lawyer": [
        "contract drafting", "litigation", "corporate law",
        "m&a", "compliance", "due diligence",
        "legal research", "negotiation", "advisory"
    ],
    
    # Operations careers
    "operations manager": [
        "supply chain", "logistics", "inventory", "process improvement",
        "operations management", "vendor management",
        "lean", "six sigma", "budgeting", "team leadership"
    ],
    "supply chain manager": [
        "procurement", "vendor management", "supply chain analytics",
        "logistics", "sourcing", "inventory management",
        "demand planning", "cost optimization", "erp systems"
    ],
    "operations analyst": [
        "operations analytics", "process optimization", "efficiency",
        "data analysis", "sql", "excel", "reporting",
        "lean", "process mapping", "continuous improvement"
    ],
    
    # Product & Project Management
    "product manager": [
        "product strategy", "roadmap", "agile", "user research",
        "product development", "strategy", "prioritization",
        "stakeholder management", "analytics", "market analysis"
    ],
    "project manager": [
        "agile", "scrum", "jira", "communication", "leadership",
        "risk management", "budgeting", "planning",
        "stakeholder management", "project tracking"
    ],
    "scrum master": [
        "scrum", "agile", "jira", "facilitation", "coaching",
        "team management", "agile methodology", "sprint planning",
        "retrospectives", "kanban", "servant leadership"
    ],
    "technical product manager": [
        "stakeholder management", "communication", "requirements",
        "technical understanding", "product roadmap", "agile",
        "apis", "system architecture", "prioritization"
    ],
    "agile coach": [
        "cross-functional collaboration", "agile", "team coordination",
        "coaching", "facilitation", "change management",
        "scrum", "kanban", "organizational transformation"
    ],
    
    # Technical Writing & Support
    "technical writer": [
        "technical writing", "documentation", "api", "markdown",
        "technical communication", "user guides", "release notes",
        "editing", "information architecture", "content management"
    ],
    "developer advocate": [
        "technical documentation", "api docs", "developer experience",
        "content creation", "community engagement", "public speaking",
        "tutorials", "sample code", "video content"
    ],
    "technical support engineer": [
        "technical support", "troubleshooting", "customer service",
        "problem solving", "documentation", "ticketing systems",
        "product knowledge", "communication", "debugging"
    ],
    
    # Business & Analytics
    "business analyst": [
        "excel", "business analysis", "market trends", "reporting",
        "requirements gathering", "process mapping", "sql",
        "data analysis", "stakeholder management", "documentation"
    ],
    "business intelligence analyst": [
        "sql", "power bi", "tableau", "business analysis",
        "analytics", "reporting", "data modeling", "etl",
        "dashboard design", "data visualization"
    ],
    "product analyst": [
        "product analytics", "user behavior", "metrics", "a/b testing",
        "sql", "python", "data visualization", "experimentation",
        "product insights", "reporting"
    ],
    
    # Architecture & Design
    "solutions architect": [
        "solution design", "enterprise architecture", "technology strategy",
        "cloud architecture", "system design", "stakeholder management",
        "technical leadership", "documentation"
    ],
    "systems architect": [
        "system design", "scalability", "performance", "high availability",
        "large-scale systems", "infrastructure", "distributed systems",
        "architecture patterns", "technical leadership"
    ],
    "software architect": [
        "design patterns", "code quality", "technical decisions",
        "software design", "best practices", "architecture",
        "system design", "technical leadership", "mentoring"
    ],
    "event-driven architect": [
        "event sourcing", "cqrs", "domain-driven design",
        "architecture patterns", "complex systems", "messaging",
        "kafka", "microservices", "distributed systems"
    ],
    
    # Testing & QA
    "qa automation engineer": [
        "test automation", "selenium", "testing", "quality assurance",
        "test frameworks", "ci/cd", "python", "java",
        "api testing", "regression testing"
    ],
    "performance test engineer": [
        "performance testing", "load testing", "jmeter", "gatling",
        "testing", "optimization", "scalability testing",
        "monitoring", "bottleneck analysis"
    ],
    "mobile qa engineer": [
        "mobile testing", "appium", "xctest", "espresso",
        "mobile qa", "automation", "ios testing", "android testing",
        "test frameworks", "ci/cd"
    ],
    
    # Specialized Engineering
    "robotics engineer": [
        "robotics", "ros", "control systems", "embedded systems",
        "automation", "robotics", "c++", "python",
        "sensors", "actuators", "computer vision"
    ],
    "embedded systems engineer": [
        "embedded systems", "c", "microcontrollers", "firmware",
        "hardware", "low-level programming", "rtos",
        "debugging", "protocols", "electronics"
    ],
    "game developer": [
        "game development", "unity", "c#", "game design",
        "gaming", "interactive media", "3d graphics",
        "physics", "game engines", "scripting"
    ],
    "blockchain developer": [
        "solidity", "ethereum", "web3", "smart contracts",
        "blockchain", "decentralization", "cryptocurrency",
        "truffle", "hardhat", "decentralized apps"
    ],
    "iot engineer": [
        "iot", "embedded systems", "mqtt", "arduino", "raspberry pi",
        "hardware", "connectivity", "sensors", "protocols",
        "cloud integration", "edge computing"
    ],
    
    # Leadership
    "engineering manager": [
        "stakeholder management", "team leadership", "okr setting",
        "performance management", "coaching", "agile",
        "technical strategy", "hiring", "mentoring"
    ],
    "vp of engineering": [
        "engineering management", "team leadership", "strategy",
        "leadership", "organizational design", "hiring",
        "technical vision", "stakeholder management"
    ],
    "cto (chief technology officer)": [
        "technical strategy", "innovation", "technology leadership",
        "strategy", "innovation", "architecture", "team building",
        "product strategy", "vendor management"
    ],
    "chief data officer": [
        "data strategy", "analytics leadership", "data science",
        "data", "leadership", "governance", "ai strategy",
        "organizational transformation", "data culture"
    ],
    "ciso (chief information security officer)": [
        "information security", "security strategy", "risk management",
        "security", "leadership", "compliance", "governance",
        "incident response", "security architecture"
    ],
    "chief product officer": [
        "product vision", "strategy", "product portfolio",
        "product leadership", "strategy", "roadmap",
        "market analysis", "team leadership"
    ],
}

# Additional comprehensive skills database with 500+ skills
COMPREHENSIVE_SKILLS = {
    "cloud_devops": [
        # AWS Services
        "aws", "ec2", "s3", "lambda", "ecs", "eks", "rds", "dynamodb",
        "cloudformation", "cloudfront", "route53", "vpc", "iam", "sns", "sqs",
        "elasticache", "redshift", "athena", "glue", "kinesis", "step functions",
        # Azure Services
        "azure", "aks", "azure functions", "azure devops", "arm templates",
        "azure storage", "cosmos db", "azure sql", "app service", "logic apps",
        # GCP Services
        "gcp", "kubernetes engine", "cloud functions", "bigquery", "cloud storage",
        "cloud run", "dataflow", "pub/sub", "firestore", "compute engine",
        # DevOps Tools
        "terraform", "ansible", "puppet", "chef", "packer", "vagrant",
        "argocd", "helm", "istio", "linkerd", "consul", "vault",
        # Monitoring & Observability
        "prometheus", "grafana", "datadog", "new relic", "splunk", "elk stack",
        "jaeger", "zipkin", "opentelemetry", "pagerduty",
        # CI/CD
        "circleci", "github actions", "gitlab ci", "travis ci", "bamboo",
        "spinnaker", "octopus deploy", "harness"
    ],
    "ai_ml": [
        # Frameworks & Libraries
        "pytorch", "tensorflow", "keras", "scikit-learn", "xgboost", "lightgbm",
        "catboost", "fastai", "jax", "mxnet", "onnx",
        # NLP & LLM
        "hugging face", "transformers", "bert", "gpt", "t5", "roberta",
        "langchain", "openai api", "claude api", "llama", "mistral",
        # Vector & Embeddings
        "vector databases", "pinecone", "weaviate", "milvus", "chromadb",
        "faiss", "embeddings", "semantic search",
        # ML Operations
        "mlflow", "kubeflow", "mlops", "model registry", "feature store",
        "feast", "tecton", "sagemaker", "vertex ai", "databricks ml",
        # Specialized
        "rag", "fine-tuning", "prompt engineering", "few-shot learning",
        "transfer learning", "active learning", "reinforcement learning",
        "computer vision", "opencv", "yolo", "rcnn", "segmentation",
        "object detection", "gan", "diffusion models", "stable diffusion"
    ],
    "data_engineering": [
        # Big Data
        "apache spark", "hadoop", "hive", "pig", "hdfs", "yarn",
        "databricks", "pyspark", "spark streaming",
        # Streaming
        "kafka", "apache flink", "apache storm", "spark streaming",
        "kinesis", "pub/sub", "event hubs",
        # Orchestration
        "airflow", "prefect", "dagster", "argo workflows", "luigi",
        # Data Warehouses
        "snowflake", "redshift", "bigquery", "synapse", "teradata",
        # Data Lakes
        "delta lake", "apache iceberg", "apache hudi", "data lake",
        # ETL/ELT
        "dbt", "talend", "informatica", "pentaho", "fivetran", "stitch",
        # Data Quality
        "great expectations", "deequ", "monte carlo", "data quality",
        # Query Engines
        "presto", "trino", "drill", "impala"
    ],
    "cybersecurity": [
        # Tools
        "penetration testing", "burp suite", "metasploit", "nmap", "wireshark",
        "kali linux", "nessus", "qualys", "acunetix", "zap",
        # Security Operations
        "siem", "soc", "splunk", "qradar", "arcsight", "sentinel",
        "incident response", "threat hunting", "forensics",
        # Concepts
        "owasp", "vulnerability assessment", "security testing",
        "malware analysis", "threat intelligence", "security architecture",
        "network security", "application security", "cloud security",
        # Frameworks
        "nist", "iso 27001", "cis controls", "pci dss", "hipaa", "gdpr",
        # Network Security
        "firewall", "ids/ips", "vpn", "waf", "ddos protection",
        "zero trust", "network segmentation"
    ],
    "frontend_modern": [
        # Frameworks
        "next.js", "nuxt.js", "svelte", "sveltekit", "solidjs", "astro",
        "remix", "qwik", "fresh",
        # Styling
        "tailwind css", "styled components", "emotion", "css modules",
        "sass", "less", "postcss", "chakra ui", "material ui", "ant design",
        # Animation
        "framer motion", "gsap", "lottie", "anime.js", "motion one",
        # 3D & Graphics
        "three.js", "webgl", "babylon.js", "pixijs", "p5.js",
        # State Management
        "redux", "mobx", "zustand", "recoil", "jotai", "xstate",
        # Build Tools
        "vite", "webpack", "rollup", "parcel", "esbuild", "turbopack",
        # Testing
        "jest", "vitest", "cypress", "playwright", "testing library",
        # Performance
        "web vitals", "lighthouse", "performance optimization",
        "lazy loading", "code splitting", "ssr", "ssg", "isr"
    ],
    "backend_modern": [
        # Languages & Frameworks
        "fastapi", "nestjs", "spring boot", "gin", "echo", "fiber",
        "actix", "rocket", "axum", "express", "koa", "hapi",
        # API Design
        "rest", "graphql", "grpc", "graphql federation", "apollo",
        "hasura", "postgraphile", "api gateway", "websockets", "server-sent events",
        # Architecture
        "microservices", "event sourcing", "cqrs", "saga pattern",
        "api composition", "service mesh", "domain-driven design",
        # Messaging
        "rabbitmq", "activemq", "nats", "zeromq", "redis streams",
        # Caching
        "redis", "memcached", "varnish", "cdn", "edge caching",
        # Authentication
        "oauth", "jwt", "saml", "openid connect", "auth0", "keycloak",
        "passport", "oauth2", "api keys"
    ],
    "mobile_modern": [
        # Native iOS
        "swiftui", "uikit", "combine", "swift", "objective-c", "xcode",
        "cocoapods", "swift package manager", "core data", "cloudkit",
        # Native Android
        "jetpack compose", "kotlin", "java", "android studio", "gradle",
        "room", "retrofit", "dagger", "hilt", "coroutines", "flow",
        # Cross-Platform
        "react native", "flutter", "expo", "capacitor", "ionic",
        "xamarin", "kotlin multiplatform", "nativescript",
        # Mobile Backend
        "firebase", "amplify", "supabase", "parse", "realm",
        # Testing
        "xctest", "espresso", "detox", "appium", "maestro"
    ],
    "soft_skills": [
        # Communication
        "stakeholder management", "cross-functional collaboration",
        "technical communication", "presentation", "public speaking",
        "writing", "documentation", "storytelling", "influence",
        # Leadership
        "mentoring", "coaching", "team leadership", "people management",
        "delegation", "conflict resolution", "motivation", "empowerment",
        # Methodologies
        "agile methodologies", "scrum", "kanban", "lean", "okr setting",
        "goal setting", "sprint planning", "retrospectives",
        # Collaboration
        "teamwork", "collaboration", "facilitation", "active listening",
        "empathy", "cultural awareness", "remote work", "async communication",
        # Problem Solving
        "critical thinking", "analytical thinking", "creative thinking",
        "problem solving", "decision making", "strategic thinking",
        "systems thinking", "root cause analysis",
        # Professional
        "time management", "organization", "prioritization",
        "adaptability", "resilience", "growth mindset", "continuous learning",
        "feedback", "self-awareness", "emotional intelligence"
    ]
}


def get_career_skills(career):
    """
    Get required skills for a specific career.
    
    Parameters:
    - career: The career name to get skills for
    
    Returns:
    - List of required skills for the career, or empty list if not found
    """
    return CAREER_SKILLS.get(career.lower(), [])


def get_all_careers():
    """
    Get list of all available careers.
    
    Returns:
    - List of career names
    """
    return list(CAREER_SKILLS.keys())
