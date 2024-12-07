# SBERT-Based Search Relevance Enhancement

## 🌟 Project Overview  
This project aims to improve search relevance by utilizing **Sentence-BERT (SBERT)** for generating semantic embeddings and the **ANNOY** library for quick approximate nearest neighbor searches. The solution is deployed on **AWS** with **Docker** containers, providing an accessible **FastAPI** for easy interaction and retrieval of highly relevant news articles.

---

## 🎯 Objective  
The primary goal is to refine the user search experience for news articles by implementing:  
1. **SBERT** to create contextual embeddings that capture the meaning behind article content.  
2. **ANNOY** to efficiently perform similarity searches with embeddings.  
3. **AWS** for scalable, cloud-based deployment of the application.

---

## 📚 Dataset Overview  
The dataset contains 13,320 articles, each with the following attributes:  
- **article_id**: Unique identifier for each news piece.  
- **category**/**subcategory**: High-level and detailed topic classifications.  
- **title**: A brief headline summarizing the article.  
- **published_date**: The date the article was released.  
- **text**: The full text of the article.  
- **source**: The originating publication or source.
  ![Alt text](images/search_relevancy.png)

---

## 🧰 Technology Stack  
- **Programming Language**: Python  
- **Key Libraries**: `pandas`, `numpy`, `spacy`, `sentence-transformers`, `annoy`, `flask`, `AWS`  
- **Cloud Deployment**: AWS EC2  
- **Containerization**: Docker  

---

## 🛠️ Methodology  
1. **Data Preparation**:  
   - Cleanse and preprocess articles through tokenization, stopword removal, and normalization.

2. **Embedding Generation**:  
   - Use the **SBERT** model to generate dense, semantically meaningful embeddings for each article.

3. **Indexing with ANNOY**:  
   - Create an index of embeddings using **ANNOY** for fast similarity searches, optimized by cosine similarity.

4. **Cloud Deployment**:  
   - Containerize all components (Flask API, SBERT model, ANNOY index) and deploy them on AWS EC2 instances using Docker, ensuring scalability and ease of access.

---

## 🗂️ Project Directory Structure  
- **`data/`**: Contains the dataset and supporting files.  
- **`notebooks/`**: Jupyter notebooks for experimentation and reference.  
- **`src/`**: Source code including functions and modules.  
- **`server.py`**: Flask application to serve API requests.  
- **`requirements.txt`**: Required Python dependencies.  
- **`Dockerfile` & `docker-compose.yml`**: Configuration files for Docker-based deployment.  
- **`demo-notes.md` & `tutorial.md`**: Documentation with instructions to run the project.

---

## 🚢 Deployment Instructions  
1. **Build the Docker Image**:  
   To create the project container, run the following command:  
   ```bash
   docker build -t search-relevance .  
