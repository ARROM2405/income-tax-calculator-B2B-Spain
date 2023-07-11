import tkinter as tk


def test_callback():
    children_result_label = tk.Label(
        master=result_frame, text=f"Children select: {children_number_variable.get()}"
    )
    children_result_label.grid(row=0, column=0)
    over_65_result_value = tk.Label(
        master=result_frame, text=f"Over 65 select: {over_65_variable.get()}"
    )
    over_65_result_value.grid(row=0, column=1)
    over_75_result_value = tk.Label(
        master=result_frame, text=f"Over 75 select: {over_75_variable.get()}"
    )
    over_75_result_value.grid(row=0, column=2)


DROPDOWN_LIST_OPTIONS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


def create_dropdown_list():
    dropdown_variable = tk.StringVar(master=window)
    dropdown_variable.set(DROPDOWN_LIST_OPTIONS[0])
    option_menu = tk.OptionMenu(
        inputs_frame,
        dropdown_variable,
        *DROPDOWN_LIST_OPTIONS,
    )
    return dropdown_variable, option_menu


window = tk.Tk()
window.title("Income tax calculator")
window.minsize(width=500, height=500)

inputs_frame = tk.Frame(
    master=window,
    borderwidth=1,
)
inputs_frame.pack()

label_children_dropdown = tk.Label(
    master=inputs_frame,
    # relief="solid",
    text="Children under 25 \nliving with you.",
)
label_children_dropdown.grid(row=0, column=0)


children_number_variable, children_number_dropdown_list = create_dropdown_list()
children_number_dropdown_list.grid(row=1, column=0)


label_parents_over_65_dropdown = tk.Label(
    master=inputs_frame,
    # relief="solid",
    text="Parents/grandparents \nover 65 living with you.",
)
label_parents_over_65_dropdown.grid(row=0, column=1)

over_65_variable, people_over_65_dropdown_list = create_dropdown_list()
people_over_65_dropdown_list.grid(row=1, column=1)

label_parents_over_65_dropdown = tk.Label(
    master=inputs_frame,
    # relief="solid",
    text="Parents/grandparents \nover 75 living with you.",
)
label_parents_over_65_dropdown.grid(row=0, column=2, pady=10)

over_75_variable, people_over_75_dropdown_list = create_dropdown_list()
people_over_75_dropdown_list.grid(row=1, column=2)

submit_button = tk.Button(
    master=inputs_frame,
    text="submit",
    command=test_callback,
)
submit_button.grid(row=2, column=1)

result_frame = tk.Frame(master=window)
result_frame.pack(pady=10)

result = tk.Label(
    result_frame,
    text="",
)
result.grid(row=0, sticky="ew")
