import graphviz


def make_seq_recognizer(user_input):
    # Create a Graphviz Digraph
    dot = graphviz.Digraph('CustomSequenceRecognizer', format='png',
                           graph_attr={'rankdir': 'LR', 'label': "State Diagram for code: " + user_input,
                                       'ranksep': '1', 'nodesep': '0.4'})

    # Add states to the graph with labels indicating the content
    for i, state in enumerate(states):
        content = user_input[:i]  # Get the content up to the current state
        dot.node(state, label=f'{state}\n{content}')

    # Backbone from S0 to S6 based on the custom input sequence
    for i in range(7):
        current_state = 'S{}'.format(i)
        content = user_input[:i]
        next_state = 'S{}'.format(i + 1)
        content_next_state = user_input[:(i + 1)]
        output = '1' if (content_next_state == user_input) else '0'  # No output
        dot.edge(current_state, next_state, label=f'{user_input[i]}/{output}')

    # Figure our where the last state (S7) can cycle back to
    x = user_input
    # Default index if there are no states to cycle back to
    index = 0
    while x != '':
        try:
            index = contents_array.index(x)
            print(f"The index of '{x}' is: {index}")
            break
        except ValueError:
            x = x[1:]
            print(f"MSB removed '{x}'")
    # Output to last state
    dot.edge('S7', 'S{}'.format(index), label=f'{user_input[7]}/1', color='green')

    # Mark the accepting state
    dot.node('S{}'.format(index), shape='doublecircle')
    # Current interation of where to cycle what back
    for i in range(8):
        current_state = 'S{}'.format(i)
        # Find next state given an error:
        next_state = 'S{}'.format(recycler(i))
        dot.edge(current_state, next_state, label=f'{alt_input[i]}/0', color='red')

    return dot


def recycler(i):
    next_state_index = 0
    x = user_input[:i] + alt_input[i]
    print(f"The current state S{i} that holds '{user_input[:i]}' with an input of '{alt_input[i]}' will now have '{x}'")
    # Default index if there are no states to cycle back to

    while x != '':
        try:
            next_state_index = contents_array[:i + 1].index(x)
            print(f"The next state's index of '{x}' can be recycled back to S{next_state_index}")
            break
        except ValueError:
            x = x[1:]

    return next_state_index


# Prompt the user to enter a custom binary sequence
user_input = input("Enter a custom binary sequence: ")
user_name = input("Enter an identifier: ")
print(user_input)
# Check if this is a binary sequence
if all(bit in '01' for bit in user_input):
    # Define the states
    states = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7']
    # Holds all contents recognized in each state
    # Ex: ['', '1', '11', '110', '1100', '11001', '110011', '1100110']
    contents_array = ['']  # Initialize the array with an empty string
    for iterator in range(len(user_input) - 1):
        contents_array.append(contents_array[-1] + user_input[iterator])
    print(contents_array)
    # Complemented user input for all the unideal situations
    alt_input = ''.join(['0' if bit == '1' else '1' for bit in user_input])
    print(alt_input)

    # Create the state diagram
    state_diagram = make_seq_recognizer(user_input)

    # Save the state diagram as an image
    file_id = user_name + "_" + user_input
    state_diagram.render(file_id, cleanup=True)
    print("State diagram created successfully. Check the '" + file_id + ".png' file.")
else:
    print("Invalid input. Please enter an 8-bit binary sequence containing only '0' and '1'.")