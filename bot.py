st.title("Mimo - AI Assistant")

input_name = st.text_input("Hi, My name is mimo. What's your name?")
if input_name:
    st.write(f"Nice to meet you {input_name}")
    task_choice = st.selectbox("Do you want to check the tasks I can perform?", ["Yes", "No"])

    if task_choice == "Yes":
        task_type = st.selectbox("Choose a task:", ["Text-to-Speech", "Text-to-Image"])

        if task_type == "Text-to-Speech":
            st.write("speech task isn't available right now")
        elif task_type == "Text-to-Image":
            st.write("image generation isn't availabele right now")
    elif task_choice == "No":
        st.write(f"Nice to meet you {input_name}, see you soon!")
