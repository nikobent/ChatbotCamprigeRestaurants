# ChatbotCamprigeRestaurants
Chatbot implementation for the Cambridge restaurant system <br>

In this report, the implementation of the Cambridge
Restaurant System chatbot is described and evaluated.
The chatbot has the goal of suggesting a restaurant to the
user, using the food, area and price preference of the user.
A dataset of dialogs between a user and a chatbot is used
to make a state transition diagram representing the user's
utterance and the response given by the chatbot. The
user's utterances are classified by type of dialog act. The
state transition diagram is implemented in a chatbot, in
which the type of dialog act of the user's utterance is
classified by a RandomForest and a suitable response is
given by the system. The chatbot works fairly well due to
the F1 score of 0.98 of the algorithm on the test data.
However, the implementation of the state transition
diagram and the use of word patterns to find the user
preferences limits the chatbot. Another limitation is the
implementation of the spellcheck. The chatbot could be
mainly improved by focussing more on the framework
