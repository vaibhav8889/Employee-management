import streamlit as st

INITIAL_EMPLOYEES = 4
RUPEES_PER_EMPLOYEE = 25
OLD_DEFAULTS = ["Engineering", "Design", "Sales", "Support"]

st.set_page_config(page_title="Employee Bucket Counter", page_icon="👥")
st.title("Employee Bucket Counter")
st.caption(
    "Rename an employee, edit a count, or press their button to add one. "
    "Add employee creates the next employee, and Remove employee drops the last one."
)

if "employee_count" not in st.session_state:
    st.session_state.employee_count = INITIAL_EMPLOYEES
if "last_pressed" not in st.session_state:
    st.session_state.last_pressed = None
if "rupees_per_employee" not in st.session_state:
    st.session_state.rupees_per_employee = RUPEES_PER_EMPLOYEE

for index in range(st.session_state.employee_count):
    name_key = f"name_{index}"
    count_key = f"count_{index}"
    default_name = f"employee{index + 1}"
    current_name = st.session_state.get(name_key)
    if current_name is None or (
        index < len(OLD_DEFAULTS) and current_name == OLD_DEFAULTS[index]
    ):
        st.session_state[name_key] = default_name
    if count_key not in st.session_state:
        st.session_state[count_key] = 0


def add_to_count(index: int) -> None:
    st.session_state[f"count_{index}"] += 1
    st.session_state.last_pressed = index


def add_employee() -> None:
    index = st.session_state.employee_count
    st.session_state[f"name_{index}"] = f"employee{index + 1}"
    st.session_state[f"count_{index}"] = 0
    st.session_state.employee_count += 1


def remove_employee() -> None:
    if st.session_state.employee_count <= 0:
        return
    index = st.session_state.employee_count - 1
    for key in (f"name_{index}", f"count_{index}", f"btn_{index}"):
        st.session_state.pop(key, None)
    if st.session_state.last_pressed == index:
        st.session_state.last_pressed = None
    st.session_state.employee_count -= 1


for index in range(st.session_state.employee_count):
    name_key = f"name_{index}"
    count_key = f"count_{index}"
    label = st.session_state[name_key].strip() or f"employee{index + 1}"

    name_col, count_col, button_col = st.columns([2, 1, 1.4], vertical_alignment="bottom")
    with name_col:
        st.text_input("Employee name", key=name_key)
    with count_col:
        st.number_input("Count", min_value=0, step=1, key=count_key)
    with button_col:
        st.button(
            label,
            key=f"btn_{index}",
            on_click=add_to_count,
            args=(index,),
            use_container_width=True,
        )

add_col, remove_col = st.columns(2)
with add_col:
    st.button("Add employee", on_click=add_employee, type="primary", use_container_width=True)
with remove_col:
    st.button(
        "Remove employee",
        on_click=remove_employee,
        disabled=st.session_state.employee_count == 0,
        use_container_width=True,
    )

if st.session_state.last_pressed is not None:
    pressed = st.session_state.last_pressed
    pressed_name = st.session_state[f"name_{pressed}"].strip() or f"employee{pressed + 1}"
    pressed_count = st.session_state[f"count_{pressed}"]
    st.success(f"{pressed_name}: {pressed_count}")

st.divider()
st.subheader("Counts")

total = 0
row_size = 4
employee_count = st.session_state.employee_count
for start in range(0, employee_count, row_size):
    end = min(start + row_size, employee_count)
    summary_cols = st.columns(end - start)
    for offset, column in enumerate(summary_cols):
        index = start + offset
        name = st.session_state[f"name_{index}"].strip() or f"employee{index + 1}"
        count = int(st.session_state[f"count_{index}"])
        total += count
        column.metric(name, count)

st.number_input(
    "Rupees per employee",
    min_value=0,
    step=1,
    key="rupees_per_employee",
)
total_rupees = total * int(st.session_state.rupees_per_employee)
total_cols = st.columns(2)
total_cols[0].metric("Total employees", total)
total_cols[1].metric("Total rupees", f"₹{total_rupees}")
