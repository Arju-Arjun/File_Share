elif option == "Live Chat":
    st.sidebar.title("Live Chat Options")
    chat_action = st.sidebar.radio("Choose an action", ("Create a New Chat", "Join an Existing Chat"))

    if chat_action == "Create a New Chat":
        user_name = st.text_input("Enter your user name")

        if user_name:
            chat_code = str(random.randint(1000, 9999))
            chat_rooms[chat_code] = {"messages": []}
            save_chat_rooms(chat_rooms)

            st.header("New Chat Room Created")
            st.success(f"Chat Room Code: {chat_code}")
        else:
            st.error("Enter a user name.")

    elif chat_action == "Join an Existing Chat":
        user_name = st.text_input("Enter your user name")

        if user_name:
            chat_code = st.text_input("Enter Chat Room Code")

            if chat_code and chat_code in chat_rooms:
                st.header(f"Chat Room {chat_code}")

                if chat_code not in st.session_state:
                    st.session_state[chat_code] = chat_rooms[chat_code]["messages"]

                for msg in st.session_state[chat_code]:
                    st.markdown(f"**{msg['user']}**: {msg['message']}")

                # Initialize session state for chat input
                if f"chat_input_{chat_code}" not in st.session_state:
                    st.session_state[f"chat_input_{chat_code}"] = ""

                # Chat input field
                chat_input = st.text_input("Type your message", 
                                           key=f"chat_input_{chat_code}")

                if st.button("Send Message"):
                    if chat_input:
                        new_message = {"user": user_name, "message": chat_input}
                        st.session_state[chat_code].append(new_message)
                        chat_rooms[chat_code]["messages"].append(new_message)
                        save_chat_rooms(chat_rooms)

                        # ✅ Properly update session state before rerunning
                        st.session_state.update({f"chat_input_{chat_code}": ""})

                        # ✅ Force rerun safely
                        st.experimental_rerun()
            else:
                st.error("Invalid chat room code.")
        else:
            st.error("Enter a user name before joining.")
