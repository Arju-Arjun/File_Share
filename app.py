if chat_option == "Join a Chat Room":
    st.header("Join a Chat Room")
    room_code = st.text_input("Enter a chat room code to join")
    user_name = st.text_input("Enter your name to join the chat")
    
    if st.button("Join Chat Room"):
        if room_code in chat_rooms and user_name:
            # Add the user to the chat room's members list
            if user_name not in chat_rooms[room_code]["members"]:
                chat_rooms[room_code]["members"].append(user_name)
                save_chat_rooms(chat_rooms)
            
            # Display chat room info
            st.subheader(f"Chat Room: {chat_rooms[room_code]['name']}")
            
            # Show the list of members
            st.write("Members:")
            for member in chat_rooms[room_code]["members"]:
                st.write(member)
            
            # Initialize chat session for the room if not initialized
            if "messages" not in st.session_state:
                st.session_state.messages = chat_rooms[room_code]["messages"]
            
            # Display chat messages
            chat_display = st.empty()  # Empty element to update chat display dynamically
            with chat_display.container():
                for message in st.session_state.messages:
                    st.markdown(message)
            
            # Send new message
            chat_input_key = f"chat_input_{room_code}"  # Use the room code as part of the key for uniqueness
            chat_input = st.text_input("Type your message", key=chat_input_key)
            
            if st.button("Send Message"):
                if chat_input:
                    # Create a timestamp for the message
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = f"{user_name} [{timestamp}]: {chat_input}"
                    
                    # Append the new message
                    st.session_state.messages.append(message)
                    chat_rooms[room_code]["messages"] = st.session_state.messages  # Save the updated messages
                    save_chat_rooms(chat_rooms)
                    
                    # Re-render the chat messages (this part is key for immediate display)
                    with chat_display.container():
                        for message in st.session_state.messages:
                            st.markdown(message)
                    
                    # Clear the input box after sending
                    st.session_state.chat_input = ""  # Reset the chat input box

                # Display the input box with previous message cleared
                chat_input = st.text_input("Type your message", value="", key=chat_input_key)  # Reset using key

