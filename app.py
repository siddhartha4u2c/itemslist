from typing import Dict, List

import streamlit as st


def get_demo_items() -> Dict[int, Dict[str, object]]:
    return {
        1: {"name": "Keyboard", "price": 49.99, "is_available": True},
        2: {"name": "Mouse", "price": 29.99, "is_available": True},
        3: {"name": "Laptop", "price": 999.99, "is_available": True},
    }


def get_inventory_insights(inventory: Dict[int, Dict[str, object]]) -> Dict[str, object]:
    available_items = [item for item in inventory.values() if item["is_available"]]
    unavailable_items = [item["name"] for item in inventory.values() if not item["is_available"]]
    available_value = sum(float(item["price"]) for item in available_items)
    budget_pick = min(available_items, key=lambda item: float(item["price"]), default=None)

    return {
        "total_count": len(inventory),
        "available_count": len(available_items),
        "available_value": available_value,
        "budget_pick": budget_pick,
        "unavailable_items": unavailable_items,
    }


st.set_page_config(page_title="Inventory Insights Demo", page_icon="📦", layout="wide")


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


st.title("Inventory Insights")
st.caption("A small inventory dashboard with transparent, rule-based recommendations. No LLM or AWS API calls.")

sidebar = st.sidebar
sidebar.title("Demo controls")

if sidebar.button("Reset demo data"):
    st.session_state["items"] = get_demo_items()

col_inventory, col_insights = st.columns([1.35, 1.0])

with col_inventory:
    st.subheader("Inventory")
    inventory = st.session_state.get("items", get_demo_items())
    items: List[Dict[str, object]] = [
        {"id": item_id, **item_data}
        for item_id, item_data in inventory.items()
    ]

    try:
        st.dataframe(items, width="stretch")
    except TypeError:
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

with col_insights:
    st.subheader("Local inventory insights")
    st.caption("Rule-based results calculated in this app; no model call is made.")

    insights = get_inventory_insights(inventory)
    st.metric("Available items", f"{insights['available_count']} / {insights['total_count']}")
    st.metric("Available inventory value", f"${insights['available_value']:.2f}")

    budget_pick = insights["budget_pick"]
    if budget_pick:
        st.success(
            f"Budget pick: {budget_pick['name']} (${float(budget_pick['price']):.2f})"
        )
    else:
        st.warning("No items are currently available.")

    unavailable_items = insights["unavailable_items"]
    if unavailable_items:
        st.warning("Restock: " + ", ".join(unavailable_items))


if __name__ == "__main__":
    st.write("")
