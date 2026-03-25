import streamlit as st
from pawpal_system import Owner, Pet, Task, Priority, Scheduler
import uuid

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    # Replaced placeholders with the calls to the methods wrote in main.py
    if not st.session_state.tasks:
        st.error("Please add at least one task first!")
    else:
        current_owner = Owner(
            owner_id="O-001",
            name=owner_name,
            email="contact@example.com",
            phone="555-0199",
            preferred_schedule_time="morning",
            daily_time_available=120
        )

        current_pet = Pet(
            pet_id="P-001", 
            name=pet_name, 
            species=species, 
            breed="Mixed", 
            age=2
        )
        current_owner.add_pet(current_pet)

        for t in st.session_state.tasks:
            pri_enum = Priority[t["priority"].upper()]
            
            new_task = Task(
                task_id=str(uuid.uuid4())[:8],
                title=t["title"],
                description="User added task",
                duration=t["duration_minutes"],
                priority=pri_enum,
                frequency="daily",
                preferred_time="morning"
            )
            current_pet.add_task(new_task)
        
        planner = Scheduler(str(uuid.uuid4()), current_owner)
        daily_plan = planner.generate_schedule()

        st.success("🗓️ Schedule Successfully Generated!")

        st.text_area("Daily Summary", value=daily_plan.get_summary(), height=400)

        with st.expander("Why was this schedule chosen?"):
            st.markdown(planner.explain_reasoning())