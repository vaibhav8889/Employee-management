import streamlit as st

BUCKET_COUNT = 4
RUPEES_PER_EMPLOYEE = 25
DEFAULT_NAMES = ["Engineering", "Design", "Sales", "Support"]

st.set_page_config(page_title="Employee Bucket Counter", page_icon="👥")
st.title("Employee Bucket Counter")
st.caption(
    "Rename a bucket, type a count, or press its button to add one employee."
)

for index, default_name in enumerate(DEFAULT_NAMES):
    if f"name_{index}" not in st.session_state:
        st.session_state[f"name_{index}"] = default_name
    if f"count_{index}" not in st.session_state:
        st.session_state[f"count_{index}"] = 0
    if "last_pressed" not in st.session_state:
        st.session_state.last_pressed = None


def add_employee(index: int) -> None:
    st.session_state[f"count_{index}"] += 1
    st.session_state.last_pressed = index


for index in range(BUCKET_COUNT):
    name_key = f"name_{index}"
    count_key = f"count_{index}"
    label = st.session_state[name_key].strip() or f"Bucket {index + 1}"

    name_col, count_col, button_col = st.columns([2, 1, 1.4], vertical_alignment="bottom")
    with name_col:
        st.text_input("Bucket name", key=name_key)
    with count_col:
        st.number_input("Count", min_value=0, step=1, key=count_key)
    with button_col:
        st.button(
            label,
            key=f"btn_{index}",
            on_click=add_employee,
            args=(index,),
            use_container_width=True,
        )

if st.session_state.last_pressed is not None:
    pressed = st.session_state.last_pressed
    pressed_name = st.session_state[f"name_{pressed}"].strip() or f"Bucket {pressed + 1}"
    pressed_count = st.session_state[f"count_{pressed}"]
    st.success(f"{pressed_name}: {pressed_count}")

st.divider()
st.subheader("Counts")

summary_cols = st.columns(BUCKET_COUNT)
total = 0
for index, column in enumerate(summary_cols):
    name = st.session_state[f"name_{index}"].strip() or f"Bucket {index + 1}"
    count = int(st.session_state[f"count_{index}"])
    total += count
    column.metric(name, count)

total_rupees = total * RUPEES_PER_EMPLOYEE
total_cols = st.columns(2)
total_cols[0].metric("Total employees", total)
total_cols[1].metric("Total rupees", f"₹{total_rupees}")
