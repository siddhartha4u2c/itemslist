# Inventory Insights Demo

A small Streamlit inventory dashboard with local, rule-based recommendations. It does not call an LLM or any AWS API. The “budget pick” is the least expensive available item, and restock notes list unavailable items; these are transparent rules, not a trained AI model.

## Run locally

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Build the container

The Dockerfile runs Streamlit on port 8501 and binds to `0.0.0.0`, so the container can receive traffic from ECS and an Application Load Balancer.

```powershell
docker build -t inventory-insights .
docker run --rm -p 8501:8501 inventory-insights
```

## AWS deployment outline

1. Create an ECR repository and push the Docker image to it.
2. Create an ECS task definition using the ECR image, Fargate, and container port 8501.
3. Create an ECS service to keep the desired number of tasks running.
4. Optionally attach an Application Load Balancer and target group to expose the service.

This app does not need Bedrock credentials, a Bedrock model ID, or an application IAM task role. ECS still needs its task execution role to pull a private image from ECR.

Inventory edits are stored in Streamlit session state and are temporary; they are not saved to a database.
