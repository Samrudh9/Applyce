# Career Roadmaps Data Module
# Contains learning roadmaps and career path information

CAREER_ROADMAPS = {
    "data scientist": {
        "phases": [
            {
                "name": "Foundation",
                "duration": "3-4 months",
                "skills": ["Python Programming", "Statistics & Probability", "SQL & Databases", "Data Manipulation with Pandas", "NumPy for Numerical Computing"],
                "resources": [
                    {"name": "Python for Everybody", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/specializations/python"},
                    {"name": "Statistics with Python", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/specializations/statistics-with-python"},
                    {"name": "SQL for Data Science", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/sql-for-data-science"},
                    {"name": "Kaggle Python Course", "platform": "Kaggle", "type": "free", "url": "https://www.kaggle.com/learn/python"},
                    {"name": "Pandas Documentation", "platform": "Official Docs", "type": "free", "url": "https://pandas.pydata.org/docs/getting_started/"}
                ]
            },
            {
                "name": "Machine Learning",
                "duration": "4-6 months",
                "skills": ["Supervised Learning", "Unsupervised Learning", "Feature Engineering", "Model Evaluation", "Scikit-learn", "Data Visualization"],
                "resources": [
                    {"name": "Machine Learning by Andrew Ng", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/machine-learning"},
                    {"name": "Kaggle Machine Learning", "platform": "Kaggle", "type": "free", "url": "https://www.kaggle.com/learn/intro-to-machine-learning"},
                    {"name": "Scikit-learn Tutorials", "platform": "Official Docs", "type": "free", "url": "https://scikit-learn.org/stable/tutorial/"},
                    {"name": "Data Visualization with Python", "platform": "Kaggle", "type": "free", "url": "https://www.kaggle.com/learn/data-visualization"},
                    {"name": "Hands-On ML Book", "platform": "O'Reilly", "type": "paid", "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/"}
                ]
            },
            {
                "name": "Advanced & Specialization",
                "duration": "6+ months",
                "skills": ["Deep Learning", "TensorFlow/PyTorch", "NLP", "Computer Vision", "MLOps", "Big Data (Spark)"],
                "resources": [
                    {"name": "Deep Learning Specialization", "platform": "Coursera", "type": "paid", "url": "https://www.coursera.org/specializations/deep-learning"},
                    {"name": "Fast.ai Practical Deep Learning", "platform": "Fast.ai", "type": "free", "url": "https://course.fast.ai/"},
                    {"name": "Hugging Face NLP Course", "platform": "Hugging Face", "type": "free", "url": "https://huggingface.co/learn/nlp-course"},
                    {"name": "TensorFlow Developer Certificate", "platform": "Google", "type": "paid", "url": "https://www.tensorflow.org/certificate"},
                    {"name": "MLOps Specialization", "platform": "Coursera", "type": "paid", "url": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops"}
                ]
            }
        ]
    },
    "frontend developer": {
        "phases": [
            {
                "name": "Web Fundamentals",
                "duration": "2-3 months",
                "skills": ["HTML5", "CSS3", "JavaScript ES6+", "Responsive Design", "Git & GitHub", "Browser DevTools"],
                "resources": [
                    {"name": "freeCodeCamp Responsive Web Design", "platform": "freeCodeCamp", "type": "free", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/"},
                    {"name": "JavaScript.info", "platform": "Web", "type": "free", "url": "https://javascript.info/"},
                    {"name": "CSS Grid & Flexbox", "platform": "Wes Bos", "type": "free", "url": "https://cssgrid.io/"},
                    {"name": "MDN Web Docs", "platform": "Mozilla", "type": "free", "url": "https://developer.mozilla.org/en-US/docs/Learn"},
                    {"name": "Git & GitHub Crash Course", "platform": "YouTube", "type": "free", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk"}
                ]
            },
            {
                "name": "JavaScript Frameworks",
                "duration": "3-4 months",
                "skills": ["React.js", "State Management (Redux/Context)", "REST APIs & Fetch", "React Router", "Component Architecture", "Testing (Jest)"],
                "resources": [
                    {"name": "React Official Tutorial", "platform": "React", "type": "free", "url": "https://react.dev/learn"},
                    {"name": "The Complete React Developer", "platform": "Udemy", "type": "paid", "url": "https://www.udemy.com/course/complete-react-developer-zero-to-mastery/"},
                    {"name": "Redux Toolkit Documentation", "platform": "Redux", "type": "free", "url": "https://redux-toolkit.js.org/tutorials/overview"},
                    {"name": "React Testing Library", "platform": "Testing Library", "type": "free", "url": "https://testing-library.com/docs/react-testing-library/intro/"},
                    {"name": "Scrimba React Course", "platform": "Scrimba", "type": "free", "url": "https://scrimba.com/learn/learnreact"}
                ]
            },
            {
                "name": "Advanced Frontend",
                "duration": "4+ months",
                "skills": ["TypeScript", "Next.js/Nuxt.js", "Performance Optimization", "PWA", "CI/CD", "Design Systems"],
                "resources": [
                    {"name": "TypeScript Handbook", "platform": "TypeScript", "type": "free", "url": "https://www.typescriptlang.org/docs/handbook/"},
                    {"name": "Next.js Documentation", "platform": "Vercel", "type": "free", "url": "https://nextjs.org/learn"},
                    {"name": "Web.dev Performance", "platform": "Google", "type": "free", "url": "https://web.dev/learn/performance"},
                    {"name": "Frontend Masters", "platform": "Frontend Masters", "type": "paid", "url": "https://frontendmasters.com/"},
                    {"name": "Storybook Documentation", "platform": "Storybook", "type": "free", "url": "https://storybook.js.org/tutorials/"}
                ]
            }
        ]
    },
    "backend developer": {
        "phases": [
            {
                "name": "Programming Fundamentals",
                "duration": "3-4 months",
                "skills": ["Python/Node.js/Java", "Data Structures", "Algorithms", "SQL Databases", "REST API Design", "Git Version Control"],
                "resources": [
                    {"name": "Python for Beginners", "platform": "Codecademy", "type": "free", "url": "https://www.codecademy.com/learn/learn-python-3"},
                    {"name": "Node.js Tutorial", "platform": "Node.js", "type": "free", "url": "https://nodejs.dev/en/learn/"},
                    {"name": "CS50 Introduction to Computer Science", "platform": "Harvard", "type": "free", "url": "https://cs50.harvard.edu/x/"},
                    {"name": "PostgreSQL Tutorial", "platform": "PostgreSQL", "type": "free", "url": "https://www.postgresqltutorial.com/"},
                    {"name": "REST API Design Best Practices", "platform": "Microsoft", "type": "free", "url": "https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design"}
                ]
            },
            {
                "name": "Backend Frameworks",
                "duration": "4-5 months",
                "skills": ["Express.js/Django/Spring Boot", "Authentication & Authorization", "Database Design", "Caching (Redis)", "API Security", "Testing"],
                "resources": [
                    {"name": "Express.js Guide", "platform": "Express", "type": "free", "url": "https://expressjs.com/en/guide/routing.html"},
                    {"name": "Django for Beginners", "platform": "Django", "type": "free", "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/"},
                    {"name": "JWT Authentication Tutorial", "platform": "Auth0", "type": "free", "url": "https://auth0.com/learn/json-web-tokens"},
                    {"name": "Redis University", "platform": "Redis", "type": "free", "url": "https://university.redis.com/"},
                    {"name": "Spring Boot Tutorial", "platform": "Spring", "type": "free", "url": "https://spring.io/guides/gs/spring-boot/"}
                ]
            },
            {
                "name": "DevOps & Architecture",
                "duration": "5+ months",
                "skills": ["Docker", "Kubernetes", "CI/CD Pipelines", "Cloud Services (AWS/GCP)", "Microservices", "System Design"],
                "resources": [
                    {"name": "Docker Getting Started", "platform": "Docker", "type": "free", "url": "https://docs.docker.com/get-started/"},
                    {"name": "Kubernetes Basics", "platform": "Kubernetes", "type": "free", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/"},
                    {"name": "AWS Free Tier Training", "platform": "AWS", "type": "free", "url": "https://aws.amazon.com/training/digital/"},
                    {"name": "System Design Primer", "platform": "GitHub", "type": "free", "url": "https://github.com/donnemartin/system-design-primer"},
                    {"name": "GitHub Actions CI/CD", "platform": "GitHub", "type": "free", "url": "https://docs.github.com/en/actions"}
                ]
            }
        ]
    },
    "mobile app developer": {
        "phases": [
            {
                "name": "Mobile Fundamentals",
                "duration": "2-3 months",
                "skills": ["Dart/JavaScript Basics", "Mobile UI/UX Principles", "Git & Version Control", "Basic App Architecture", "IDE Setup (VS Code/Android Studio)"],
                "resources": [
                    {"name": "Dart Language Tour", "platform": "Dart", "type": "free", "url": "https://dart.dev/language"},
                    {"name": "Flutter Official Documentation", "platform": "Flutter", "type": "free", "url": "https://docs.flutter.dev/get-started/codelab"},
                    {"name": "React Native Getting Started", "platform": "React Native", "type": "free", "url": "https://reactnative.dev/docs/getting-started"},
                    {"name": "Mobile App UI Design", "platform": "Figma", "type": "free", "url": "https://www.figma.com/resources/learn-design/"},
                    {"name": "Android Basics in Kotlin", "platform": "Google", "type": "free", "url": "https://developer.android.com/courses/android-basics-kotlin/course"}
                ]
            },
            {
                "name": "Cross-Platform Development",
                "duration": "3-4 months",
                "skills": ["Flutter/React Native", "State Management", "API Integration", "Local Storage", "Navigation", "Responsive Layouts"],
                "resources": [
                    {"name": "Flutter Complete Course", "platform": "Udemy", "type": "paid", "url": "https://www.udemy.com/course/learn-flutter-dart-to-build-ios-android-apps/"},
                    {"name": "Flutter State Management", "platform": "Flutter", "type": "free", "url": "https://docs.flutter.dev/data-and-backend/state-mgmt"},
                    {"name": "React Native Express", "platform": "Web", "type": "free", "url": "https://www.reactnative.express/"},
                    {"name": "Firebase for Flutter", "platform": "Firebase", "type": "free", "url": "https://firebase.google.com/docs/flutter/setup"},
                    {"name": "Expo Documentation", "platform": "Expo", "type": "free", "url": "https://docs.expo.dev/"}
                ]
            },
            {
                "name": "Native & Advanced",
                "duration": "4+ months",
                "skills": ["Swift (iOS)", "Kotlin (Android)", "App Store Deployment", "Push Notifications", "Performance Optimization", "Testing"],
                "resources": [
                    {"name": "iOS App Development with Swift", "platform": "Stanford", "type": "free", "url": "https://cs193p.sites.stanford.edu/"},
                    {"name": "Kotlin for Android", "platform": "Google", "type": "free", "url": "https://developer.android.com/kotlin"},
                    {"name": "App Store Connect Guide", "platform": "Apple", "type": "free", "url": "https://developer.apple.com/app-store-connect/"},
                    {"name": "Google Play Console", "platform": "Google", "type": "free", "url": "https://play.google.com/console/about/"},
                    {"name": "Flutter Testing", "platform": "Flutter", "type": "free", "url": "https://docs.flutter.dev/testing"}
                ]
            }
        ]
    },
    "devops engineer": {
        "phases": [
            {
                "name": "Linux & Scripting",
                "duration": "2-3 months",
                "skills": ["Linux Administration", "Bash Scripting", "Python Scripting", "Networking Basics", "Git & Version Control"],
                "resources": [
                    {"name": "Linux Journey", "platform": "Web", "type": "free", "url": "https://linuxjourney.com/"},
                    {"name": "Bash Scripting Tutorial", "platform": "Ryan's Tutorials", "type": "free", "url": "https://ryanstutorials.net/bash-scripting-tutorial/"},
                    {"name": "Python for DevOps", "platform": "Real Python", "type": "free", "url": "https://realpython.com/tutorials/devops/"},
                    {"name": "Computer Networking Course", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/computer-networking"},
                    {"name": "Git Branching", "platform": "Learn Git Branching", "type": "free", "url": "https://learngitbranching.js.org/"}
                ]
            },
            {
                "name": "Containers & CI/CD",
                "duration": "3-4 months",
                "skills": ["Docker", "Docker Compose", "GitHub Actions", "Jenkins", "GitLab CI", "Container Security"],
                "resources": [
                    {"name": "Docker Curriculum", "platform": "Docker", "type": "free", "url": "https://docker-curriculum.com/"},
                    {"name": "GitHub Actions Tutorial", "platform": "GitHub", "type": "free", "url": "https://docs.github.com/en/actions/learn-github-actions"},
                    {"name": "Jenkins Tutorial", "platform": "Jenkins", "type": "free", "url": "https://www.jenkins.io/doc/tutorials/"},
                    {"name": "Docker Mastery", "platform": "Udemy", "type": "paid", "url": "https://www.udemy.com/course/docker-mastery/"},
                    {"name": "GitLab CI/CD", "platform": "GitLab", "type": "free", "url": "https://docs.gitlab.com/ee/ci/quick_start/"}
                ]
            },
            {
                "name": "Cloud & Orchestration",
                "duration": "5+ months",
                "skills": ["Kubernetes", "AWS/Azure/GCP", "Terraform", "Ansible", "Monitoring (Prometheus/Grafana)", "Security"],
                "resources": [
                    {"name": "Kubernetes the Hard Way", "platform": "GitHub", "type": "free", "url": "https://github.com/kelseyhightower/kubernetes-the-hard-way"},
                    {"name": "AWS Certified Cloud Practitioner", "platform": "AWS", "type": "free", "url": "https://aws.amazon.com/training/learn-about/cloud-practitioner/"},
                    {"name": "Terraform Getting Started", "platform": "HashiCorp", "type": "free", "url": "https://developer.hashicorp.com/terraform/tutorials/aws-get-started"},
                    {"name": "Ansible Documentation", "platform": "Ansible", "type": "free", "url": "https://docs.ansible.com/ansible/latest/getting_started/"},
                    {"name": "Prometheus & Grafana", "platform": "Prometheus", "type": "free", "url": "https://prometheus.io/docs/tutorials/getting_started/"}
                ]
            }
        ]
    },
    "full stack developer": {
        "phases": [
            {
                "name": "Frontend Basics",
                "duration": "2-3 months",
                "skills": ["HTML5 & CSS3", "JavaScript ES6+", "React/Vue.js", "Responsive Design", "Git"],
                "resources": [
                    {"name": "The Odin Project", "platform": "The Odin Project", "type": "free", "url": "https://www.theodinproject.com/"},
                    {"name": "freeCodeCamp Full Stack", "platform": "freeCodeCamp", "type": "free", "url": "https://www.freecodecamp.org/"},
                    {"name": "React Official Tutorial", "platform": "React", "type": "free", "url": "https://react.dev/learn"},
                    {"name": "CSS Tricks", "platform": "CSS Tricks", "type": "free", "url": "https://css-tricks.com/"},
                    {"name": "JavaScript30", "platform": "Wes Bos", "type": "free", "url": "https://javascript30.com/"}
                ]
            },
            {
                "name": "Backend & Databases",
                "duration": "3-4 months",
                "skills": ["Node.js/Express", "Python/Django", "PostgreSQL/MongoDB", "REST APIs", "Authentication"],
                "resources": [
                    {"name": "Node.js Complete Guide", "platform": "Udemy", "type": "paid", "url": "https://www.udemy.com/course/nodejs-the-complete-guide/"},
                    {"name": "MongoDB University", "platform": "MongoDB", "type": "free", "url": "https://university.mongodb.com/"},
                    {"name": "PostgreSQL Tutorial", "platform": "PostgreSQL", "type": "free", "url": "https://www.postgresqltutorial.com/"},
                    {"name": "Full Stack Open", "platform": "University of Helsinki", "type": "free", "url": "https://fullstackopen.com/en/"},
                    {"name": "Django REST Framework", "platform": "Django", "type": "free", "url": "https://www.django-rest-framework.org/tutorial/quickstart/"}
                ]
            },
            {
                "name": "DevOps & Deployment",
                "duration": "3+ months",
                "skills": ["Docker", "CI/CD", "Cloud Deployment (AWS/Vercel)", "Testing", "Performance"],
                "resources": [
                    {"name": "Docker for Developers", "platform": "Docker", "type": "free", "url": "https://docs.docker.com/get-started/"},
                    {"name": "Vercel Deployment", "platform": "Vercel", "type": "free", "url": "https://vercel.com/docs"},
                    {"name": "AWS Amplify", "platform": "AWS", "type": "free", "url": "https://docs.amplify.aws/"},
                    {"name": "Testing JavaScript", "platform": "Kent C. Dodds", "type": "paid", "url": "https://testingjavascript.com/"},
                    {"name": "Web Performance", "platform": "Google", "type": "free", "url": "https://web.dev/performance/"}
                ]
            }
        ]
    },
    "machine learning engineer": {
        "phases": [
            {
                "name": "ML Foundations",
                "duration": "3-4 months",
                "skills": ["Python Programming", "Linear Algebra", "Probability & Statistics", "NumPy & Pandas", "Data Visualization"],
                "resources": [
                    {"name": "Mathematics for Machine Learning", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/specializations/mathematics-machine-learning"},
                    {"name": "3Blue1Brown Linear Algebra", "platform": "YouTube", "type": "free", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab"},
                    {"name": "Python Data Science Handbook", "platform": "GitHub", "type": "free", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/"},
                    {"name": "Kaggle Learn", "platform": "Kaggle", "type": "free", "url": "https://www.kaggle.com/learn"},
                    {"name": "StatQuest with Josh Starmer", "platform": "YouTube", "type": "free", "url": "https://www.youtube.com/@statquest"}
                ]
            },
            {
                "name": "Deep Learning",
                "duration": "4-5 months",
                "skills": ["Neural Networks", "TensorFlow/PyTorch", "CNNs", "RNNs/LSTMs", "Transfer Learning"],
                "resources": [
                    {"name": "Deep Learning Specialization", "platform": "Coursera", "type": "paid", "url": "https://www.coursera.org/specializations/deep-learning"},
                    {"name": "PyTorch Tutorials", "platform": "PyTorch", "type": "free", "url": "https://pytorch.org/tutorials/"},
                    {"name": "TensorFlow Developer Certificate", "platform": "Google", "type": "paid", "url": "https://www.tensorflow.org/certificate"},
                    {"name": "Fast.ai Course", "platform": "Fast.ai", "type": "free", "url": "https://course.fast.ai/"},
                    {"name": "Dive into Deep Learning", "platform": "D2L", "type": "free", "url": "https://d2l.ai/"}
                ]
            },
            {
                "name": "MLOps & Production",
                "duration": "4+ months",
                "skills": ["Model Deployment", "MLflow", "Docker for ML", "Kubernetes", "Model Monitoring", "A/B Testing"],
                "resources": [
                    {"name": "MLOps Specialization", "platform": "Coursera", "type": "paid", "url": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops"},
                    {"name": "Made with ML", "platform": "Web", "type": "free", "url": "https://madewithml.com/"},
                    {"name": "MLflow Documentation", "platform": "MLflow", "type": "free", "url": "https://mlflow.org/docs/latest/index.html"},
                    {"name": "Weights & Biases", "platform": "W&B", "type": "free", "url": "https://docs.wandb.ai/tutorials"},
                    {"name": "Full Stack Deep Learning", "platform": "FSDL", "type": "free", "url": "https://fullstackdeeplearning.com/"}
                ]
            }
        ]
    },
    "data analyst": {
        "phases": [
            {
                "name": "Analytics Fundamentals",
                "duration": "2-3 months",
                "skills": ["Excel/Google Sheets", "SQL Basics", "Statistics", "Data Cleaning", "Critical Thinking"],
                "resources": [
                    {"name": "Google Data Analytics Certificate", "platform": "Coursera", "type": "paid", "url": "https://www.coursera.org/professional-certificates/google-data-analytics"},
                    {"name": "SQL for Data Analysis", "platform": "Mode", "type": "free", "url": "https://mode.com/sql-tutorial/"},
                    {"name": "Excel Skills for Business", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/specializations/excel"},
                    {"name": "Khan Academy Statistics", "platform": "Khan Academy", "type": "free", "url": "https://www.khanacademy.org/math/statistics-probability"},
                    {"name": "W3Schools SQL", "platform": "W3Schools", "type": "free", "url": "https://www.w3schools.com/sql/"}
                ]
            },
            {
                "name": "Data Visualization",
                "duration": "2-3 months",
                "skills": ["Tableau", "Power BI", "Python (Matplotlib/Seaborn)", "Dashboard Design", "Storytelling with Data"],
                "resources": [
                    {"name": "Tableau Public Training", "platform": "Tableau", "type": "free", "url": "https://public.tableau.com/app/learn/how-to-videos"},
                    {"name": "Power BI Learning Path", "platform": "Microsoft", "type": "free", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"},
                    {"name": "Data Visualization with Python", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/python-for-data-visualization"},
                    {"name": "Storytelling with Data Book", "platform": "Web", "type": "paid", "url": "https://www.storytellingwithdata.com/"},
                    {"name": "Kaggle Data Viz Course", "platform": "Kaggle", "type": "free", "url": "https://www.kaggle.com/learn/data-visualization"}
                ]
            },
            {
                "name": "Advanced Analytics",
                "duration": "3+ months",
                "skills": ["Python/R for Analysis", "A/B Testing", "Predictive Analytics", "Business Intelligence", "Reporting Automation"],
                "resources": [
                    {"name": "Python for Data Analysis Book", "platform": "O'Reilly", "type": "paid", "url": "https://wesmckinney.com/book/"},
                    {"name": "A/B Testing on Udacity", "platform": "Udacity", "type": "free", "url": "https://www.udacity.com/course/ab-testing--ud257"},
                    {"name": "R for Data Science", "platform": "Web", "type": "free", "url": "https://r4ds.had.co.nz/"},
                    {"name": "DataCamp Courses", "platform": "DataCamp", "type": "paid", "url": "https://www.datacamp.com/"},
                    {"name": "IBM Data Analyst Certificate", "platform": "Coursera", "type": "paid", "url": "https://www.coursera.org/professional-certificates/ibm-data-analyst"}
                ]
            }
        ]
    },
    "software engineer": {
        "phases": [
            {
                "name": "Programming Foundations",
                "duration": "3-4 months",
                "skills": ["Python/Java/JavaScript", "Data Structures", "Algorithms", "Object-Oriented Programming", "Version Control"],
                "resources": [
                    {"name": "CS50 Computer Science", "platform": "Harvard", "type": "free", "url": "https://cs50.harvard.edu/x/"},
                    {"name": "LeetCode", "platform": "LeetCode", "type": "free", "url": "https://leetcode.com/explore/"},
                    {"name": "Clean Code Book", "platform": "Amazon", "type": "paid", "url": "https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882"},
                    {"name": "Git & GitHub Bootcamp", "platform": "Udemy", "type": "paid", "url": "https://www.udemy.com/course/git-and-github-bootcamp/"},
                    {"name": "Design Patterns", "platform": "Refactoring Guru", "type": "free", "url": "https://refactoring.guru/design-patterns"}
                ]
            },
            {
                "name": "Software Development",
                "duration": "4-5 months",
                "skills": ["Web Frameworks", "Database Design", "API Development", "Testing (Unit/Integration)", "Agile/Scrum"],
                "resources": [
                    {"name": "The Odin Project", "platform": "Web", "type": "free", "url": "https://www.theodinproject.com/"},
                    {"name": "System Design Interview", "platform": "Amazon", "type": "paid", "url": "https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF"},
                    {"name": "REST API Design", "platform": "Microsoft", "type": "free", "url": "https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design"},
                    {"name": "Testing Best Practices", "platform": "Martin Fowler", "type": "free", "url": "https://martinfowler.com/testing/"},
                    {"name": "Scrum Guide", "platform": "Scrum.org", "type": "free", "url": "https://scrumguides.org/"}
                ]
            },
            {
                "name": "Senior Engineering",
                "duration": "6+ months",
                "skills": ["System Design", "Microservices", "Cloud Architecture", "Performance Optimization", "Technical Leadership"],
                "resources": [
                    {"name": "Designing Data-Intensive Applications", "platform": "O'Reilly", "type": "paid", "url": "https://dataintensive.net/"},
                    {"name": "System Design Primer", "platform": "GitHub", "type": "free", "url": "https://github.com/donnemartin/system-design-primer"},
                    {"name": "AWS Solutions Architect", "platform": "AWS", "type": "paid", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/"},
                    {"name": "High Scalability Blog", "platform": "Web", "type": "free", "url": "http://highscalability.com/"},
                    {"name": "Staff Engineer Book", "platform": "Web", "type": "paid", "url": "https://staffeng.com/book"}
                ]
            }
        ]
    },
    "hr manager": {
        "phases": [
            {
                "name": "HR Fundamentals",
                "duration": "2-3 months",
                "skills": ["Recruitment & Selection", "Onboarding", "HR Policies", "Employee Relations", "Labor Laws"],
                "resources": [
                    {"name": "SHRM Learning System", "platform": "SHRM", "type": "paid", "url": "https://www.shrm.org/certification/learning/"},
                    {"name": "HR Management Fundamentals", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/human-resources-management"},
                    {"name": "LinkedIn Talent Solutions", "platform": "LinkedIn", "type": "free", "url": "https://business.linkedin.com/talent-solutions/resources"},
                    {"name": "AIHR Academy", "platform": "AIHR", "type": "paid", "url": "https://www.aihr.com/"},
                    {"name": "People Analytics Course", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/wharton-people-analytics"}
                ]
            },
            {
                "name": "HR Technology & Operations",
                "duration": "3-4 months",
                "skills": ["HRIS Systems", "Payroll Management", "Benefits Administration", "Performance Management", "HR Analytics"],
                "resources": [
                    {"name": "Workday Training", "platform": "Workday", "type": "paid", "url": "https://www.workday.com/en-us/customer-experience/education.html"},
                    {"name": "BambooHR Resources", "platform": "BambooHR", "type": "free", "url": "https://www.bamboohr.com/resources/"},
                    {"name": "Compensation & Benefits", "platform": "SHRM", "type": "paid", "url": "https://www.shrm.org/certification/"},
                    {"name": "HR Metrics & Analytics", "platform": "AIHR", "type": "paid", "url": "https://www.aihr.com/courses/hr-metrics-reporting/"},
                    {"name": "ADP Workforce Now", "platform": "ADP", "type": "free", "url": "https://www.adp.com/resources/articles-and-insights.aspx"}
                ]
            },
            {
                "name": "Strategic HR Leadership",
                "duration": "4+ months",
                "skills": ["Talent Management", "Organizational Development", "Change Management", "DEI Initiatives", "HR Strategy"],
                "resources": [
                    {"name": "Strategic HR Management", "platform": "Cornell", "type": "paid", "url": "https://ecornell.cornell.edu/certificates/human-resources/strategic-human-resources-leadership/"},
                    {"name": "Change Management Certification", "platform": "Prosci", "type": "paid", "url": "https://www.prosci.com/solutions/training-programs/change-management-certification"},
                    {"name": "DEI in the Workplace", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/diversity-inclusion-workplace"},
                    {"name": "Josh Bersin Academy", "platform": "Josh Bersin", "type": "paid", "url": "https://joshbersin.com/academy/"},
                    {"name": "Harvard ManageMentor", "platform": "Harvard", "type": "paid", "url": "https://www.harvardbusiness.org/managementor/"}
                ]
            }
        ]
    },
    "digital marketer": {
        "phases": [
            {
                "name": "Marketing Fundamentals",
                "duration": "2-3 months",
                "skills": ["Marketing Principles", "Content Marketing", "Social Media Basics", "Email Marketing", "Analytics Basics"],
                "resources": [
                    {"name": "Google Digital Garage", "platform": "Google", "type": "free", "url": "https://learndigital.withgoogle.com/digitalgarage"},
                    {"name": "HubSpot Academy", "platform": "HubSpot", "type": "free", "url": "https://academy.hubspot.com/"},
                    {"name": "Meta Blueprint", "platform": "Meta", "type": "free", "url": "https://www.facebook.com/business/learn"},
                    {"name": "Mailchimp Email Marketing", "platform": "Mailchimp", "type": "free", "url": "https://mailchimp.com/resources/"},
                    {"name": "Google Analytics Academy", "platform": "Google", "type": "free", "url": "https://analytics.google.com/analytics/academy/"}
                ]
            },
            {
                "name": "Paid Advertising",
                "duration": "3-4 months",
                "skills": ["Google Ads", "Facebook/Instagram Ads", "LinkedIn Ads", "PPC Campaign Management", "Conversion Optimization"],
                "resources": [
                    {"name": "Google Ads Certification", "platform": "Google", "type": "free", "url": "https://skillshop.exceedlms.com/student/catalog/list?category_ids=53-google-ads-certifications"},
                    {"name": "Meta Ads Manager", "platform": "Meta", "type": "free", "url": "https://www.facebook.com/business/learn/courses"},
                    {"name": "LinkedIn Marketing Labs", "platform": "LinkedIn", "type": "free", "url": "https://www.linkedin.com/learning/topics/linkedin-marketing"},
                    {"name": "CXL Conversion Optimization", "platform": "CXL", "type": "paid", "url": "https://cxl.com/institute/"},
                    {"name": "WordStream PPC University", "platform": "WordStream", "type": "free", "url": "https://www.wordstream.com/learn"}
                ]
            },
            {
                "name": "SEO & Advanced Marketing",
                "duration": "4+ months",
                "skills": ["SEO Strategy", "Content Strategy", "Marketing Automation", "Data-Driven Marketing", "Growth Hacking"],
                "resources": [
                    {"name": "Moz SEO Learning Center", "platform": "Moz", "type": "free", "url": "https://moz.com/learn/seo"},
                    {"name": "Ahrefs Academy", "platform": "Ahrefs", "type": "free", "url": "https://ahrefs.com/academy"},
                    {"name": "Semrush Academy", "platform": "Semrush", "type": "free", "url": "https://www.semrush.com/academy/"},
                    {"name": "GrowthHackers", "platform": "GrowthHackers", "type": "free", "url": "https://growthhackers.com/"},
                    {"name": "Reforge Growth Series", "platform": "Reforge", "type": "paid", "url": "https://www.reforge.com/programs"}
                ]
            }
        ]
    },
    "financial analyst": {
        "phases": [
            {
                "name": "Finance Fundamentals",
                "duration": "3-4 months",
                "skills": ["Financial Accounting", "Excel Mastery", "Financial Statements Analysis", "Corporate Finance Basics", "Business Math"],
                "resources": [
                    {"name": "Financial Accounting Fundamentals", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/wharton-accounting"},
                    {"name": "Excel for Finance", "platform": "CFI", "type": "free", "url": "https://corporatefinanceinstitute.com/resources/excel/"},
                    {"name": "Investopedia Academy", "platform": "Investopedia", "type": "paid", "url": "https://academy.investopedia.com/"},
                    {"name": "Khan Academy Finance", "platform": "Khan Academy", "type": "free", "url": "https://www.khanacademy.org/economics-finance-domain/core-finance"},
                    {"name": "Wall Street Prep", "platform": "WSP", "type": "paid", "url": "https://www.wallstreetprep.com/"}
                ]
            },
            {
                "name": "Financial Modeling",
                "duration": "4-5 months",
                "skills": ["Financial Modeling", "Valuation Methods", "Budgeting & Forecasting", "Scenario Analysis", "Power BI/Tableau"],
                "resources": [
                    {"name": "Financial Modeling & Valuation Analyst", "platform": "CFI", "type": "paid", "url": "https://corporatefinanceinstitute.com/certifications/financial-modeling-valuation-analyst-fmva-program/"},
                    {"name": "Breaking Into Wall Street", "platform": "BIWS", "type": "paid", "url": "https://breakingintowallstreet.com/"},
                    {"name": "CFA Level 1 Prep", "platform": "CFA Institute", "type": "paid", "url": "https://www.cfainstitute.org/en/programs/cfa"},
                    {"name": "Power BI for Finance", "platform": "Microsoft", "type": "free", "url": "https://learn.microsoft.com/en-us/training/paths/create-use-analytics-reports-power-bi/"},
                    {"name": "Macabacus Excel Training", "platform": "Macabacus", "type": "free", "url": "https://macabacus.com/learn"}
                ]
            },
            {
                "name": "Advanced Analysis",
                "duration": "5+ months",
                "skills": ["Investment Analysis", "Risk Management", "Python for Finance", "M&A Analysis", "FP&A"],
                "resources": [
                    {"name": "CFA Program", "platform": "CFA Institute", "type": "paid", "url": "https://www.cfainstitute.org/en/programs/cfa/exam"},
                    {"name": "Python for Finance", "platform": "Udemy", "type": "paid", "url": "https://www.udemy.com/course/python-for-finance-and-trading-algorithms/"},
                    {"name": "FP&A Certification", "platform": "AFP", "type": "paid", "url": "https://www.afponline.org/publications-data-tools/tools/fp-a-certification"},
                    {"name": "M&A Modeling", "platform": "WSP", "type": "paid", "url": "https://www.wallstreetprep.com/self-study-programs/merger-model-training/"},
                    {"name": "Quantitative Finance", "platform": "Coursera", "type": "paid", "url": "https://www.coursera.org/specializations/investment-management"}
                ]
            }
        ]
    },
    "project manager": {
        "phases": [
            {
                "name": "PM Fundamentals",
                "duration": "2-3 months",
                "skills": ["Project Management Basics", "Agile & Scrum", "Communication Skills", "Stakeholder Management", "Risk Management"],
                "resources": [
                    {"name": "Google Project Management Certificate", "platform": "Coursera", "type": "paid", "url": "https://www.coursera.org/professional-certificates/google-project-management"},
                    {"name": "Scrum.org Learning Path", "platform": "Scrum.org", "type": "free", "url": "https://www.scrum.org/resources/what-is-scrum"},
                    {"name": "PMI Project Management Basics", "platform": "PMI", "type": "free", "url": "https://www.pmi.org/learning/library"},
                    {"name": "Agile Manifesto", "platform": "Web", "type": "free", "url": "https://agilemanifesto.org/"},
                    {"name": "Atlassian Agile Coach", "platform": "Atlassian", "type": "free", "url": "https://www.atlassian.com/agile"}
                ]
            },
            {
                "name": "Tools & Methodologies",
                "duration": "3-4 months",
                "skills": ["Jira/Asana/Monday", "Gantt Charts", "Kanban", "Sprint Planning", "Budget Management"],
                "resources": [
                    {"name": "Jira Software Training", "platform": "Atlassian", "type": "free", "url": "https://university.atlassian.com/student/collection/850385-jira-software"},
                    {"name": "Asana Academy", "platform": "Asana", "type": "free", "url": "https://academy.asana.com/"},
                    {"name": "Monday.com Learning Center", "platform": "Monday.com", "type": "free", "url": "https://monday.com/blog/"},
                    {"name": "Microsoft Project Training", "platform": "Microsoft", "type": "free", "url": "https://support.microsoft.com/en-us/project"},
                    {"name": "Lean Six Sigma Yellow Belt", "platform": "Various", "type": "paid", "url": "https://www.sixsigmaonline.org/"}
                ]
            },
            {
                "name": "Certifications & Leadership",
                "duration": "4+ months",
                "skills": ["PMP Certification", "Scrum Master Certification", "Program Management", "Change Management", "Leadership"],
                "resources": [
                    {"name": "PMP Certification Prep", "platform": "PMI", "type": "paid", "url": "https://www.pmi.org/certifications/project-management-pmp"},
                    {"name": "Professional Scrum Master", "platform": "Scrum.org", "type": "paid", "url": "https://www.scrum.org/assessments/professional-scrum-master-i-certification"},
                    {"name": "SAFe Agilist", "platform": "Scaled Agile", "type": "paid", "url": "https://scaledagile.com/training/leading-safe/"},
                    {"name": "PMI-ACP Certification", "platform": "PMI", "type": "paid", "url": "https://www.pmi.org/certifications/agile-acp"},
                    {"name": "PRINCE2 Foundation", "platform": "AXELOS", "type": "paid", "url": "https://www.axelos.com/certifications/prince2"}
                ]
            }
        ]
    }
}

# Default roadmap for careers not in the dictionary
DEFAULT_ROADMAP = {
    "phases": [
        {
            "name": "Foundation",
            "duration": "2-3 months",
            "skills": ["Industry fundamentals", "Core tools & software", "Basic concepts", "Communication skills", "Time management"],
            "resources": [
                {"name": "LinkedIn Learning", "platform": "LinkedIn", "type": "paid", "url": "https://www.linkedin.com/learning/"},
                {"name": "Coursera Professional Certificates", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/"},
                {"name": "edX Courses", "platform": "edX", "type": "free", "url": "https://www.edx.org/"},
                {"name": "Udemy Courses", "platform": "Udemy", "type": "paid", "url": "https://www.udemy.com/"},
                {"name": "YouTube Tutorials", "platform": "YouTube", "type": "free", "url": "https://www.youtube.com/"}
            ]
        },
        {
            "name": "Intermediate",
            "duration": "3-4 months",
            "skills": ["Advanced techniques", "Project building", "Industry best practices", "Collaboration tools", "Problem-solving"],
            "resources": [
                {"name": "Skillshare", "platform": "Skillshare", "type": "paid", "url": "https://www.skillshare.com/"},
                {"name": "Pluralsight", "platform": "Pluralsight", "type": "paid", "url": "https://www.pluralsight.com/"},
                {"name": "Industry Certifications", "platform": "Various", "type": "paid", "url": "https://www.coursera.org/professional-certificates"},
                {"name": "Meetup Groups", "platform": "Meetup", "type": "free", "url": "https://www.meetup.com/"},
                {"name": "Reddit Communities", "platform": "Reddit", "type": "free", "url": "https://www.reddit.com/"}
            ]
        },
        {
            "name": "Advanced",
            "duration": "4+ months",
            "skills": ["Specialization", "Leadership skills", "Strategic thinking", "Mentoring others", "Industry expertise"],
            "resources": [
                {"name": "Professional Certifications", "platform": "Industry-specific", "type": "paid", "url": "https://www.coursera.org/professional-certificates"},
                {"name": "Conference Talks", "platform": "YouTube", "type": "free", "url": "https://www.youtube.com/"},
                {"name": "Industry Publications", "platform": "Medium", "type": "free", "url": "https://medium.com/"},
                {"name": "Networking Events", "platform": "Eventbrite", "type": "free", "url": "https://www.eventbrite.com/"},
                {"name": "Mentorship Programs", "platform": "Various", "type": "free", "url": "https://www.mentoring.org/"}
            ]
        }
    ]
}


def get_career_roadmap(career):
    """
    Generate a learning roadmap for a specific career with actual resource links.
    
    Parameters:
    - career: The career name to get roadmap for
    
    Returns:
    - Dictionary containing phases with skills and resources
    """
    return CAREER_ROADMAPS.get(career.lower(), DEFAULT_ROADMAP)
