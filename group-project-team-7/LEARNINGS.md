Team Name: Team 7
Team Members: Edvard Soerby, Janelle Lin, Jonathan Lu, Natalia Juarez, Vikramsingh Rathod 

Original Goal
We initially aimed to help students discover UC Berkeley courses through a semantic search API, which would allow users to express natural, contextual queries such as “classes that discuss AI ethics and social responsibility.”

Actual Functionality
Our current implementation provides both a semantic course search and a conversational chat experience within a single API implemented using FastAPI, enabling students to discover relevant UC Berkeley courses based on natural language inputs. The API also handles administrative CRUD operations, with authorization requirements, to manage course data.

API Use Cases
Student Course Search: Students can input a string, and Search will return the most relevant 10 courses.
Student search: GET/courses/search
Connects to the external Voyage AI API to convert the search query into embeddings.

Student Course Chat: Students can interact with a conversational chat agent that recommends courses.
Student chat: POST/chat
Connects to the external OpenAI API with the search tool to pick course recommendations and craft chat responses.
Search tool uses mostly the same logic as the search API.

Course Admin CRUD Operations:
Create a new course: POST/courses
Get a specific course by ID: GET/courses/{id}
Update one or more course fields: PUT/courses/{id}
Delete a course: DELETE/courses/{id}

All endpoints are documented with Swagger:
https://drive.google.com/file/d/1bPen2hlYZ5KeUDWWYNxU5dTftY6BhoWn/view?usp=drive_link

Search & Chat Challenges & Learnings:
Vector Search outperforms Full-Text Search: We considered implementing a Full-Text Search, but after experiencing it on other course search tools, we decided to build a Vector Search system. We used VoyageAI’s voyage-large-3 to embed both course descriptions once and student queries. We didn’t experiment much with different embedding models or APIs since VoyageAI has a generous free tier and was state-of-the-art on MTEB a few months ago. MongoDB Atlas stores the course metadata and embedding vectors, enabling search. This approach resulted in better contextual matching between students' queries and the course description documents, surpassing word-based matching.
For chat, we use LangGraph to build the agent and use OpenAI’s GPT-4.1 as the main LLM to power the agent. We chose LangGraph since it has a simple agent abstraction and easy tracing/observability with LangSmith. Our agent is equipped with a system message describing its task and our course search API as a tool. We didn’t do much prompt engineering because the agent seemed good enough; however, in a real production application, we would create a set of evaluations with LangSmith to more reliably benchmark agent performance.
Chat Memory in MongoDB Atlas: We realized the chatbot’s user experience and utility without persistent conversational memory so we used MongoDB Atlas to store conversation histories. 
We used FastAPI instead of Flask because of its first-class asynchronous support, which seemed like it would be a good fit for high latency agent calls. Additionally, the robust data validation, typing, automatic documentation, and ease of development were big pluses as well. 

Authentication Challenges:
Implemented lightweight Token-Based Authentication: Since our API includes both public endpoints and more administrative ones, we wanted a way to secure selected endpoints. We realized that authentication can become complicated fast, especially without a frontend interface for login, etc. As a middle ground, we implemented a simplified JSON Web Token (JWT) authentication system for our API endpoints. This approach enabled us to manage access without overcomplicating the project.

Data Access Challenge:
Since access to the Berkeley Course API is restricted by the university, we initially relied on a snapshot of the Berkeley Course API data. However, this snapshot data was still limited. We implemented a one-time web-scraper to collect additional course information from the Fall 2024 - Spring 2025 course descriptions (e.g., https://classes.berkeley.edu/content/2025-spring-compsci-c267-001-lec-001).

CRUD Challenges:
Although the database data was retrieved from an existing database, we wanted to provide functionality to manually add, edit, and delete courses. One crucial detail was to allow for updating specific fields in the courses without needing the admin to type the entire JSON body of that course. We also limited which fields the user can update, as some are not intended to be edited by a person.

Development Opportunities:
Schedule a cron job for the Web-Scraper Worker: For the scope of this project, we used the scraper only once. For a real-world release, we should create a cron job to update the course data every six months using the Web-Scraper Worker.
Add CalNet SSO Authorization: A full-scale rollout would benefit from CalNet SSO authentication for better user session handling and security.
Subjective Search Improvements: One interesting challenge is interpreting and ranking subjective criteria such as “easy” or “fun,” especially when professors would likely exclude such adjectives in official course descriptions. A future enhancement could integrate RateMyProfessors data or sentiment analysis on past course reviews to capture more subjective criteria. These integrations would broaden our data sources, resulting in more accurate responses.
More Personalization: The course search could also be more personalized with a CalCentral/bCourses integration, which would provide more unique context on the student’s degree track, past courses, and academic goals.

System Diagram Link:
https://docs.google.com/drawings/d/1e7EubfxS5bmqZnAFP7vcri557C2r_IrOQl_AUjWzdDk/edit
