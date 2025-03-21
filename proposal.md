# Team: Revamping Course Catalog

**Team Members**:  
Natalia Juarez, Janelle Lin, Jonathan Lu, Vikramsingh Rathod, Edvard Soerby

---

## Project Proposal

Our proposal is to build an API that offers a more intuitive and personalized way for students to search for and discover UC Berkeley courses. The current course catalog is functional only if students know what they’re looking for. It’s slow, cluttered with popups, and isn’t optimized for discovery. As a result, students often rely on Reddit threads, word-of-mouth, RateMyProfessors, or Google Sheets passed around by friends to find interesting or manageable classes.

### Our Solution

We aim to improve this experience by building a semantic search API that allows users to express natural, contextual queries like “easy 4-unit classes for a senior’s busy semester” or “classes that talk about AI ethics and social responsibility.” Our project will use an embedding provider like Voyage AI for natural language understanding and retrieval augmentation, working on top of Berkeley SIS Course API to obtain data on course descriptions, schedules, and metadata. That being said, we plan to start the project with a snapshot of the Berkeley Course API data since access to actual data is restricted by the university, and we don’t need live data to build a proof-of-concept. Our API will persist course metadata and user search logs in a NoSQL database like MongoDB or DynamoDB, and everything will run in containerized Docker environments for deployment.

### System Overview

- **Database**: NoSQL (e.g., MongoDB or DynamoDB) for persisting course metadata and user search logs  
- **Deployment**: Containerized using Docker

---

## External APIs & Tools
To obtain and store embeddings of course information, we plan to use an embedding service and a hosted vector database like Voyage AI and Pinecone to simplify the system. Additionally, to set up the agentic course recommender, we plan to use OpenAI API and GPT-4o-mini for cost effectiveness. Ideally, we’d be able to use the Berkeley SIS Course API directly to get course information; however, it has specific permission requirements which would make it difficult so we will start with using a snapshot from the BerkeleyTime team instead.

- **Embeddings & Vector Storage**:  
  - [Voyage AI](https://voyageai.com) (for embedding services)  
  - [Pinecone](https://www.pinecone.io) (for hosted vector database)

- **LLM & Agentic Recommender**:  
  - [OpenAI API](https://openai.com/api)  
  - **GPT-4o-mini** (for cost-effective reasoning)

- **Course Data Source**:  
  - Primary: Berkeley SIS Course API (if access is possible)  
  - Alternative: Data snapshot from [BerkeleyTime](https://berkeleytime.com)

