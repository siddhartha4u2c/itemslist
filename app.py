import json
import os
from typing import Dict, List

import boto3
import streamlit as st


DEFAULT_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")


def get_demo_items() -> Dict[int, Dict[str, object]]:
    return {
        1: {"name": "Keyboard", "price": 49.99, "is_available": True},
        2: {"name": "Mouse", "price": 29.99, "is_available": True},
        3: {"name": "Laptop", "price": 999.99, "is_available": True},
    }


def call_bedrock(prompt: str, model_id: str = MODEL_ID) -> str:
    """Basic Bedrock invocation using the AWS SDK."""
    try:
        session = boto3.session.Session(region_name=DEFAULT_REGION)
        client = session.client("bedrock-runtime")

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ],
                }
            ],
        }

        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )

        payload = json.loads(response["body"].read())
        output = payload["content"][0]["text"]
        return output.strip()
    except Exception as exc:  # pragma: no cover - runtime integration error
        return (
            "Bedrock is not yet configured. Add AWS credentials and permissions, "
            f"or set BEDROCK_MODEL_ID/AWS_REGION. Error: {exc}"
        )


st.set_page_config(page_title="Inventory + Bedrock Demo", page_icon="☁️", layout="wide")


if "items" not in st.session_state:
    st.session_state["items"] = get_demo_items()


def add_item(name: str, price: float, is_available: bool):
    if not name.strip():
        st.warning("Item name cannot be empty.")
        return
    inventory = st.session_state["items"]
    next_id = max(inventory.keys(), default=0) + 1
    inventory[next_id] = {
        "name": name.strip(),
        "price": float(price),
        "is_available": bool(is_available),
    }
    st.session_state["items"] = inventory


st.title("AWS + Streamlit Demo")
st.caption("Inventory dashboard powered by Streamlit, with an optional AWS Bedrock integration.")

sidebar = st.sidebar
sidebar.title("Configuration")
sidebar.text_input("AWS Region", value=DEFAULT_REGION, key="aws_region")
sidebar.text_input("Bedrock Model ID", value=MODEL_ID, key="bedrock_model_id")

if sidebar.button("Reset demo data"):
    st.session_state["items"] = get_demo_items()

col_inventory, col_ai = st.columns([1.35, 1.0])

with col_inventory:
    st.subheader("Inventory")
    inventory = st.session_state.get("items", get_demo_items())
    items: List[Dict[str, object]] = [
        {"id": item_id, **item_data}
        for item_id, item_data in inventory.items()
    ]
    st.dataframe(items, use_container_width=True)

    with st.form("add_item_form"):
        st.write("Add a new item")
        name = st.text_input("Name")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        available = st.checkbox("Available", value=True)
        submitted = st.form_submit_button("Add item")

        if submitted:
            add_item(name, price, available)
            st.rerun()

with col_ai:
    st.subheader("Ask AWS Bedrock")
    prompt = st.text_area(
        "Prompt",
        value="Summarize the current inventory and suggest the most popular product.",
        height=150,
    )

    if st.button("Generate response"):
        with st.spinner("Calling Bedrock..."):
            answer = call_bedrock(prompt, st.session_state.bedrock_model_id)
        st.markdown("### Response")
        st.write(answer)

    st.markdown("### Notes")
    st.info(
        "This app is a starter pattern for learning AWS Bedrock, ECS, ECR, and ELB. "
        "In production, place credentials in IAM roles and run the container through ECS "
        "behind an Elastic Load Balancer."
    )

    with st.expander("Example AWS deployment flow"):
        st.markdown(
            """
            1. Push app code to GitHub.
            2. Build Docker image and push to ECR.
            3. Create an ECS task definition and service.
            4. Place the service behind an Application Load Balancer.
            5. Use IAM roles for Bedrock access.
            """
        )


if __name__ == "__main__":
    st.write("")
