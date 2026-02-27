**Financial News Sentiment Analysis Pipeline**

An end-to-end MLOps pipeline that classifies financial news into Positive, Negative, or Neutral sentiments. This project demonstrates the transition from a research model (Fine-tuned DistilBERT) to a production-ready API.

**1.	Overview**
This repository contains a high-performance REST API designed to process financial text. Unlike general sentiment models, this pipeline is optimized for financial terminology (e.g., "bearish," "surged," "guidance").

**2.	Dataset & Model Details**
The underlying model is a DistilBERT-base-uncased transformer, fine-tuned on financial text to capture industry-specific nuances.

**Training Data (Financial PhraseBank)**

**Total Instances:** 4,840 labeled sentences.

**Content:** Sentences from financial news articles (e.g., earnings reports, mergers, market trends).

**Labels:**
**Positive:** Indicating growth, exceeding expectations, or market gains.
**Neutral:** Factual statements or scheduled corporate events.
**Negative:** Indicating losses, lawsuits, or economic downturns.

**Class Distribution:** The dataset contains a realistic mix, with a high volume of neutral statements to reflect real-world financial reporting.

**3.	Model Selection : Why DistilBert ?**
For this pipeline, DistilBERT was chosen over the standard BERT model for several production-related reasons:

**Latency:** DistilBERT is 60% faster than BERT-base, ensuring our /predict endpoint remains responsive under load.

**Resource Efficiency:** It has 40% fewer parameters and a smaller memory footprint, significantly reducing Docker image size and cloud hosting costs.

**Performance Retention:** It retains roughly 97% of BERT's language understanding capabilities, making it the "sweet spot" for financial sentiment tasks where millisecond speed matters.

**4.	Key Features**

**Core Model:** Fine-tuned DistilBERT (Transformer) specialized for financial sentiment.

**Backend:** Built with FastAPI for high-speed, asynchronous inference.

**Containerization:** Fully Dockerized to ensure environment consistency across any machine.

**Observability:** Integrated logging to track prediction history, confidence scores, and latency.

**5.	Architecture**

The pipeline follows a modular microservice pattern:

**Client Interface:** Uses FastAPI’s interactive Swagger UI for real-time testing.

**API Layer:** An asynchronous FastAPI web server handling request validation via Pydantic

**Inference Engine:** A fine-tuned DistilBERT transformer that processes text inputs on the CPU

**Logging System:** A multi-handler logger that captures metadata (sentiment, confidence, latency) into api_usage.log

**Response:** returned with sentiment and confidence

**Deployment:** The entire stack is encapsulated in a Docker container for environment parity. 

**6.	Technology Stack**

**Language:** Python 3.11

**AI/ML:** HuggingFace Transformers, PyTorch

**API Framework:** FastAPI, Uvicorn, Pydantic

**Infrastructure:** Docker

**Monitoring:** Python Logging Library (File & Stream handlers)

**7.	Getting Started**

**Prerequisites**
•	Docker Desktop installed
•	Git installed

**A . Build the Image**
Navigate to the project root and build the Docker container:
docker build -t financial-ai-api .

**B. Run the Service**
Run the container and map the port. Volume is used to persist logs from the container to the local machine:
docker run -p 8000:8000 -v "${PWD}:/app" financial-ai-api

**8.	API Usage**
Once the container is running, the home page looks like:
 <img width="940" height="512" alt="image" src="https://github.com/user-attachments/assets/18b13cae-3673-46ca-b942-5010754b0f11" />

The interactive documentation is available at: URL: http://127.0.0.1:8000/docs
 <img width="940" height="455" alt="image" src="https://github.com/user-attachments/assets/ccee4fac-6b76-4c48-8ed2-61f84088d491" />


To make prediction: click POST -> click Try it out -> then enter the string in Request Body
For the given input string:
**Request Body: **
{Trading remained relatively flat during the morning session as investors awaited the upcoming employment data from the Bureau of Labor Statistics}.
The model prediction:

**Response:**

{
  "sentiment": "Negative",
  "confidence": 0.7355,
  "status": "Success"
}

 <img width="940" height="421" alt="image" src="https://github.com/user-attachments/assets/840cb87b-2d5d-47f0-9798-65b8e1703b19" />

 <img width="940" height="369" alt="image" src="https://github.com/user-attachments/assets/194e6948-ad50-42db-8fa0-2a15cd094e2a" />


**9.	Logging and Monitoring**
The system automatically generates an api_usage.log file. The details I had logged are as follows:
•	**Timestamp:** When the prediction occurred.
•	**Input Metadata:** Snippet of the processed text.
•	**Model Output:** Predicted label and confidence level.
•	**Latency:** Time taken for the inference to complete.

**10.	Project Structure:**
app.py                        # FastAPI application & Logging logic 
Dockerfile                  # Container configuration 
requirements.txt      # Project dependencies 
model_final/             # Fine-tuned DistilBERT model weights 
api_usage.log            # (Auto-generated) Production logs

**11.	Performance Metrics**
Based on production logs, the model demonstrates high certainty on clear-cut financial signals:
**A.	Predictive Confidence**
•	Strong Positive/Neutral Signals: Achieved confidence scores of 97.9% (Revenue Surge) and 99.1% (Central Bank schedules).
•	Edge Case Handling: Identified complex "Airline Recovery" news with 95.7% confidence.
•	Observation: The model shows lower confidence (56%) on dense numerical earnings comparisons, highlighting an area for future fine-tuning with more quantitative financial reports.

**B.	Operational Latency**
The logging system tracked the time taken from the moment the API received the text to the moment the prediction was returned (Inference Latency):
•	Average Inference Speed: 105ms – 120ms per request.
•	Cold Start Latency: A one-time spike of 1.3s – 1.9s was observed during the initial model loading phase, which is standard for Transformer models on CPU-based containers.
•	Optimized Throughput: By utilizing FastAPI’s asynchronous architecture, the service remains non-blocking, allowing for high-frequency prediction requests.
Because I used FastAPI instead of Flask, the system is "Asynchronous." This means while the model is busy processing one news, the API can already start receiving the next one, preventing a traffic jam of data.

**12.	Challenges**
1. The Environment Consistency Problem
Challenge: The model worked in Google Colab but failed on my local machine due to library version mismatches (PyTorch/Transformers).
Solution: Implemented Docker to containerize the environment, ensuring the exact same versions of Python and torch are used regardless of where the app is deployed.

2. Port Mapping & Networking
Challenge: Encountered ERR_ADDRESS_INVALID when trying to access the API via the container's internal IP.
Solution: Configured explicit port forwarding (-p 8000:8000) and mapped the host's localhost to the container's 0.0.0.0 listener.

3. Data Persistence in Containers
Challenge: Log files (api_usage.log) were being deleted every time the container was stopped or rebuilt.
Solution: Used Docker Bind Mounts (Volumes) to link the container's log directory to the host machine, ensuring persistent monitoring data even after container restarts.
