# Search Relevance Algorithm with SBERT  

## 🚀 Project Overview  
Search relevance measures how effectively search results align with user intent, playing a critical role in industries like e-commerce, content platforms, and news outlets. This project demonstrates an efficient solution for enhancing search relevance by leveraging **Sentence-BERT (SBERT)** for semantic embeddings and the **ANNOY** library for fast approximate nearest neighbor search.  

Deployed on AWS with **Docker** and a **Flask API**, the solution provides an intuitive interface for querying and retrieving relevant news articles.  

---

## 🏆 Aim  
To improve the search experience for news articles using:  
1. **SBERT** for semantically meaningful embeddings.  
2. **ANNOY** for efficient similarity-based search.  
3. **AWS** for scalable deployment.  

---

## 📊 Dataset Description  
The dataset consists of 22,399 articles with the following attributes:  
- **article_id**: Unique identifier for each article.  
- **category/subcategory**: Classification for topic granularity.  
- **title**: Article headline.  
- **published_date**: Publication date.  
- **text**: Full article body.  
- **source**: Originating source or publication.  

---

## 🛠️ Tech Stack  
- **Language**: Python  
- **Libraries**: `pandas`, `numpy`, `spacy`, `sentence-transformers`, `annoy`, `flask`, `AWS`  
- **Deployment**: Docker, AWS EC2  

---

## 📝 Approach  
1. **Data Preprocessing**:  
   - Tokenization, stopword removal, and normalization.  

2. **SBERT Training**:  
   - Generate semantically meaningful embeddings for articles.  

3. **ANNOY Indexing**:  
   - Create a fast, efficient approximate nearest neighbor index.  

4. **Deployment**:  
   - Containerized components (Flask API, SBERT model, ANNOY index) deployed on AWS using Docker.  

---

## 📁 Project Structure  
- **`data/`**: Contains datasets and related files.  
- **`notebooks/`**: Reference Jupyter notebooks for experimentation.  
- **`src/`**: Core Python functions and modules.  
- **`server.py`**: Script for running the Flask API.  
- **`requirements.txt`**: List of dependencies.  
- **`Dockerfile` & `docker-compose.yml`**: Configuration files for Docker deployment.  
- **`demo-notes.md`** & **`tutorial.md`**: Step-by-step instructions for running the project.  

---

## 🐳 Deployment  
1. Build the Docker image:  
   ```bash
   docker build -t search-relevance .  
