import statetransition as st
import configure as conf
#Main program handler, system starts in welcome_msg state.
""" All preferences are initiated as 'nongiven', all unsure booleans are 'false, options list empty. System uses these global variables as a way of
retaining information between states. """
msg = "Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?"
current_state = 'welcome_msg'
st.locPreference, st.foodPreference, st.pricePreference, st.name = "nongiven", "nongiven", "nongiven", "nongiven"
st.unsureloc, st.unsureprice, st.unsurefood = False, False, False
st.options = []
counter = 0
print("\n To configure the system with optional features, please type 'editconfig' \n NOTE: WILL RESTART SYSTEM AFTER EDITING \n ------------------------------------------------------")
#System loop: with catches for exit and restart, loops calls for 'state_transition' function, which calls all other functions

while True:
    if conf.output_in_caps:
        msg = msg.upper()
    user = input(msg + "\n")
    current_state, msg = st.state_transition(user, current_state)
    counter = counter + 1
    if current_state == 'exit_program':
        break
    if current_state == 'restart':
        current_state = 'welcome_msg'
        msg = "Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?"
        st.locPreference, st.foodPreference, st.pricePreference, st.name = "nongiven", "nongiven", "nongiven", "nongiven"
        st.unsurefood, st.unsureloc, st.unsureprice = False, False, False
        counter = 0
    if conf.limit_the_dialogue:
        if counter > 4:
            current_state = 'exit_program'
            break
            