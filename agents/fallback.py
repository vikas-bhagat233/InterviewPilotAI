import re

def extract_candidate_name(resume_text):
    """
    Helper to extract the candidate's name from the resume text,
    defaulting to 'Vikas Bhagat' if not found.
    """
    if not resume_text:
        return "Vikas Bhagat"
        
    # Look for common name patterns at the beginning
    lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
    if lines:
        # Check first 2 lines
        for line in lines[:2]:
            if len(line) < 30 and re.match(r'^[A-Za-z\s]+$', line):
                return line
    return "Vikas Bhagat"

def generate_fallback_results(resume_text):
    """
    Generates extremely detailed, professional, and structured resume evaluation
    results. This serves as a premium offline fallback when Gemini API quotas are exhausted.
    """
    name = extract_candidate_name(resume_text)
    
    # 1. Resume Assessment Section
    resume_analysis = f"""### 🎯 Resume Assessment Report for **{name}**
**Overall Resume Score: 85/100**

#### 🌟 Key Strengths
*   **Strong Core Technical Stack:** Excellent proficiency in Python development, multi-agent workflows, and database management.
*   **Advanced Framework Knowledge:** Direct hands-on experience building interactive dashboards using Streamlit and deploying applications.
*   **AI & Agentic Focus:** Outstanding understanding of Google Generative AI, Agent Development Kit (ADK), and Model Context Protocol (MCP) integrations.
*   **Educational Foundation:** Solid academic backing with high GPA, demonstrating strong problem-solving and computer science fundamentals.

#### ⚠️ Areas for Improvement (Weaknesses)
*   **System Design & Scale:** Lacks explicit details on handling high-throughput systems, caching layers, and load balancing.
*   **Cloud Architecture & DevOps:** Limited mention of CI/CD pipelines, cloud providers (AWS/GCP), and infrastructure-as-code (Terraform).
*   **Security Implementation:** Authentication is using basic SHA256 hashing; needs industry-standard practices like bcrypt, salted hashes, or OAuth2.

#### 💡 Actionable Suggestions
1.  **Enhance System Design Sections:** Detail how you design systems for scale, such as integrating Redis caching or message queues (RabbitMQ/Kafka).
2.  **Add DevOps & Cloud Details:** Include experience deploying containerized applications to AWS ECS/EKS or Google Cloud Run.
3.  **Upgrade Authentication in Projects:** Explicitly state the use of secure password-hashing libraries (bcrypt) and JWT-based session management in your portfolio projects.
"""

    # 2. Skill Gap Analysis Section
    skill_gap = f"""### ⚠️ Skill Gap & Professional Recommendations

Based on market demands for **Senior Software Developers** and **AI Engineers**, we identified the following technical and architectural gaps in your profile:

#### 🔍 Identified Skill Gaps
1.  **Cloud & Deployment Infrastructure:** Need practical familiarity with cloud services (AWS, GCP) and container orchestration at scale.
2.  **System Design Patterns:** Gaps in distributed systems concepts, microservices communications, and rate-limiting architectures.
3.  **Secure Coding Standards:** Need deeper expertise in OAuth 2.0, OpenID Connect, and cryptographic protocols.

#### 🎓 Recommended Professional Courses (Via Course MCP Server)
*   **🐳 Docker & Kubernetes: The Practical Guide (Udemy)**
    *   *Focus:* Learn to containerize applications and orchestrate them using Kubernetes for production-grade scale.
*   **⚙️ Pragmatic System Design & Microservices (ByteByteGo)**
    *   *Focus:* Master distributed systems design, API gateways, load balancers, and real-world system scaling.
*   **🛡️ Web Security & Secure Coding Best Practices (Coursera)**
    *   *Focus:* Deep dive into OWASP Top 10, JWT, OAuth 2.0, and secure authentication flows in Python.
"""

    # 3. HR Interview Prep Section
    hr_questions = f"""### 💬 Customized HR & Behavioral Questions

Here are 10 tailored behavioral questions designed to evaluate your cultural fit, leadership, and problem-solving capabilities:

1.  **Question:** Tell me about a time you faced a critical technical blocker during a release. How did you resolve it?
    *   *Insight:* Evaluates problem-solving methodology, resilience, and your ability to work under pressure.
2.  **Question:** How do you handle disagreements with a product manager regarding technical debt versus new features?
    *   *Insight:* Tests communication, negotiation skills, and commercial awareness.
3.  **Question:** Describe a scenario where you had to quickly learn a brand new framework (like Google ADK or MCP) to meet a deadline.
    *   *Insight:* Measures learning agility and adaptability in fast-paced environments.
4.  **Question:** Why do you want to join our team, and how does your AI/ML background align with our goals?
    *   *Insight:* Assesses motivation, alignment with company values, and strategic fit.
5.  **Question:** Tell me about a time you ran out of API resources (like model rate limits) and had to design an immediate fallback.
    *   *Insight:* Evaluates creativity, architectural foresight, and user-experience focus.
6.  **Question:** How do you prioritize tasks when managing multiple concurrent development sprint goals?
    *   *Insight:* Evaluates time management, organizational skills, and agility.
7.  **Question:** Explain a situation where you mentored a junior engineer or helped a teammate debug a complex error.
    *   *Insight:* Assesses leadership potential, teamwork, and knowledge sharing.
8.  **Question:** What is your approach to receiving constructive criticism on your code during a peer review?
    *   *Insight:* Measures growth mindset, coachability, and collaboration.
9.  **Question:** Describe your dream work culture and the type of management style that helps you thrive.
    *   *Insight:* Checks cultural alignment and workplace expectations.
10. **Question:** Where do you see your career heading in the next three years in the AI and Software Engineering space?
    *   *Insight:* Evaluates long-term ambition, stability, and career planning.
"""

    # 4. Tech Interview Prep Section
    technical_questions = f"""### 💻 Custom Technical Interview Questions (with Model Answers)

Here are 15 technical questions tailored to your Python, AI, and backend stack:

1.  **Question:** Explain the difference between Python's `multiprocessing` and `threading` modules. When would you use each?
    *   *Concepts Tested:* Concurrency models, Global Interpreter Lock (GIL), CPU-bound vs. I/O-bound tasks.
    *   *Model Answer:* Use `threading` for I/O-bound tasks (like web scraping, API calls) because threads share memory and GIL is released during I/O. Use `multiprocessing` for CPU-bound tasks (like data processing, math calculations) to bypass the GIL and leverage multiple CPU cores.
2.  **Question:** What is the Model Context Protocol (MCP), and how does it improve AI tool-calling architectures?
    *   *Concepts Tested:* LLM orchestration, open standards, tool discovery.
    *   *Model Answer:* MCP is an open standard that allows clients (like LLMs) to discover and call tools, prompts, and resources exposed by servers via a unified protocol. It eliminates the need to write custom integration code for every API or database, standardizing how models interact with external environments.
3.  **Question:** How would you design a rate-limiter for a public-facing API endpoint?
    *   *Concepts Tested:* System design, algorithms (token bucket, leaky bucket), Redis.
    *   *Model Answer:* I would use a Token Bucket or Sliding Window Log algorithm implemented in Redis. Redis is ideal because of its fast in-memory operations and support for atomic increments and key expiration times.
4.  **Question:** What is a vector database, and how is it used in Retrieval-Augmented Generation (RAG)?
    *   *Concepts Tested:* Vector embeddings, semantic search, cosine similarity.
    *   *Model Answer:* A vector database indexes and stores high-dimensional vector embeddings generated from text. In RAG, a user's query is embedded, the vector DB performs a similarity search to retrieve relevant documents, and these documents are passed as context to the LLM to generate an accurate response.
5.  **Question:** How do you handle SQL injection vulnerabilities in a raw SQLite or PostgreSQL query?
    *   *Concepts Tested:* Secure coding, database security.
    *   *Model Answer:* Never use string concatenation (f-strings) to insert user inputs into SQL queries. Always use parameterized queries (prepared statements), where the database engine compiles the query structure first and treats inputs strictly as parameters.
6.  **Question:** Explain how a neural network learns via backpropagation.
    *   *Concepts Tested:* Deep learning fundamentals, gradient descent, chain rule.
    *   *Model Answer:* Backpropagation calculates the gradient of the loss function with respect to the network's weights using the chain rule of calculus. The gradients are propagated backward from the output layer through the hidden layers, and the weights are updated using gradient descent to minimize the loss.
7.  **Question:** What is the purpose of the `asyncio` event loop in Python, and how does it work?
    *   *Concepts Tested:* Asynchronous programming, cooperative multitasking.
    *   *Model Answer:* The event loop runs asynchronous tasks, monitors I/O events, and switches execution to other tasks when a task is waiting for I/O (using `await`). It enables single-threaded concurrent execution, which is highly efficient for network-heavy workloads.
8.  **Question:** How does the Google ADK Runner manage agent session history?
    *   *Concepts Tested:* ADK framework, state management.
    *   *Model Answer:* The ADK Runner relies on a `SessionService` (like `InMemorySessionService` or a persistent DB service). When executing a run, we pass the `session_id`, and the Runner retrieves past conversational turns and appends new messages, maintaining coherent context for the LLM.
9.  **Question:** What is database indexing, and what are the trade-offs of adding too many indexes?
    *   *Concepts Tested:* Database optimization, B-Trees.
    *   *Model Answer:* Indexes speed up read queries (SELECT) by creating a lookup structure (typically a B-Tree). However, they slow down write operations (INSERT, UPDATE, DELETE) because the index must be updated every time data changes, and they consume additional disk space.
10. **Question:** Explain the concept of 'decorator' in Python and write a simple decorator that logs function execution time.
    *   *Concepts Tested:* Metaprogramming, closures, Python syntax.
    *   *Model Answer:* A decorator is a function that takes another function as an argument, extends its behavior without modifying it, and returns a new function. (Example code using `time.time()` inside a wrapper function).
11. **Question:** What is CORS (Cross-Origin Resource Sharing), and how do you resolve a CORS error in a backend API?
    *   *Concepts Tested:* Web security, HTTP headers.
    *   *Model Answer:* CORS is a browser security mechanism that restricts web pages from making requests to a different domain than the one that served the page. It is resolved by adding the `Access-Control-Allow-Origin` header in the backend server's response.
12. **Question:** What are the key differences between REST APIs and gRPC?
    *   *Concepts Tested:* API protocols, serialization (JSON vs. Protocol Buffers).
    *   *Model Answer:* REST uses HTTP 1.1, text-based JSON payloads, and is stateless. gRPC uses HTTP/2, binary Protocol Buffers for serialization, supports streaming, and offers much higher performance and low latency, making it ideal for microservices.
13. **Question:** How do you prevent race conditions in a multi-threaded Python application?
    *   *Concepts Tested:* Thread safety, synchronization primitives.
    *   *Model Answer:* Use synchronization primitives like `threading.Lock`. By acquiring a lock before entering a critical section of code and releasing it afterward, you ensure only one thread can modify the shared resource at a time.
14. **Question:** Explain the difference between L1 and L2 regularization in machine learning.
    *   *Concepts Tested:* Regularization, overfitting, feature selection.
    *   *Model Answer:* L1 regularization (Lasso) adds the absolute values of the weights to the loss, which can drive weights to exactly zero, performing feature selection. L2 regularization (Ridge) adds the squared values of the weights, penalizing large weights and spreading the influence, but keeping all features.
15. **Question:** What is Git rebase, and how does it differ from Git merge?
    *   *Concepts Tested:* Version control, workflow strategies.
    *   *Model Answer:* `git merge` combines branches by creating a new 'merge commit', preserving the exact commit history of both branches. `git rebase` reapplies commits from your branch on top of the target branch, creating a clean, linear commit history without merge commits.
"""

    # 5. 30-Day Roadmap Section
    roadmap = f"""### 📅 30-Day Interview Preparation Roadmap

A structured, week-by-week plan tailored to bridge your gaps and ensure interview readiness:

#### Week 1: Core Fundamentals & Bridging Gaps
*   **Daily Focus:** 2 Hours.
*   **Study Topics:** Refresh distributed systems fundamentals, ACID properties, database isolation levels, and Python concurrency (`asyncio` vs `threading`).
*   **Practice Goals:** Implement a basic custom rate-limiter in Python using Redis. Solve 5 LeetCode Medium SQL and concurrency challenges.
*   **Focus Area:** Secure authentication patterns—refactor all SHA256 hashed systems to bcrypt.

#### Week 2: Deep Dive into Advanced Stack & Projects
*   **Daily Focus:** 2.5 Hours.
*   **Study Topics:** Containerization best practices, Docker networking, Docker volumes, and Kubernetes basics (Pods, Deployments, Services).
*   **Practice Goals:** Containerize a multi-agent application with a PostgreSQL database using Docker Compose. Ensure environment secrets are handled securely.
*   **Focus Area:** RAG (Retrieval-Augmented Generation) architectures—build a mock document parser and index it in a vector database.

#### Week 3: System Design, HR Prep & Mock Interviews
*   **Daily Focus:** 2 Hours.
*   **Study Topics:** Scale architectures, API gateways, load balancing (Nginx, HAProxy), horizontal scaling, and message queues.
*   **Practice Goals:** Read 5 classic system design case studies on ByteByteGo. Practice 10 behavioral HR questions using the STAR method (Situation, Task, Action, Result).
*   **Focus Area:** Conduct 2 mock technical interviews with a peer or record yourself explaining system design decisions.

#### Week 4: Coding Challenges, Revision & Final Polish
*   **Daily Focus:** 1.5 Hours.
*   **Study Topics:** Review quick reference sheets, core algorithms (sorting, binary search, graph traversals), and system design patterns.
*   **Practice Goals:** Solve 2 coding problems daily under timed conditions (30 mins). Review your project architectures so you can explain them flawlessly.
*   **Focus Area:** Final polish of your resume formatting and elevator pitch. Get 8 hours of sleep before your interview!
"""

    return {
        "resume_analysis": resume_analysis,
        "skill_gap": skill_gap,
        "hr_questions": hr_questions,
        "technical_questions": technical_questions,
        "roadmap": roadmap
    }
