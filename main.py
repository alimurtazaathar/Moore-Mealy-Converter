import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt

state_entries = []#array to store state name and output(moore) 
output_entries=[]#array to store outputs(mealy)
transition_entries = []#2d array to store transition to next state  
states_data = []#array to store data for each state as an object 
tkEntries=[] #array to store the entry widgets to clear out input(for backButtons)

global num_transitions

def goBack(prevPage,currPage):
    #hiding the current page
    currPage.pack_forget()
    #displaying the previous page
    prevPage.pack()
    #clearing all potentially previously used variables
    state_entries.clear()  
    output_entries.clear()
    transition_entries.clear()  
    states_data.clear()
    #clearing inputted data on current page
    for toremove in tkEntries:
        toremove.delete(0,tk.END)       
    

def mooreToMealy():
    menuPage.pack_forget()
    mooreToMealyPage.pack()

def mealyToMoore():
    menuPage.pack_forget()
    mealyToMoorePage.pack()

def proceedMealyToMoore():
    global num_transitions  
    num_states = int(states_entry_mealy_to_moore.get())
    num_transitions = int(transitions_entry_mealy_to_moore.get())
    inputFieldsMealy(num_states, num_transitions)

def proceedMooreToMealy():
    global num_transitions  
    num_states = int(states_entry_moore_to_mealy.get())
    num_transitions = int(transitions_entry_moore_to_mealy.get())
    inputFieldsMoore(num_states, num_transitions)

def generateMoore():
    global output_entries, transition_entries
    setStatesDataMealy()
    G = nx.DiGraph()    

    for i in range(len(output_entries)):
        output_entry_row = output_entries[i]
        transition_entry_row = transition_entries[i]

        for j in range(len(output_entry_row)):
            next_state = output_entries[i][j].get()
            transition_entry = transition_entries[i][j].get()
            node_label = f"q{next_state}/{transition_entry}"      
            if node_label not in G.nodes():
                G.add_node(node_label,label=f"{node_label}")
                print(f"{node_label}")
            
    for node_label in G.nodes():
        state_name = node_label.split('/')[0]
        print(f"working for {state_name}")
        for state_info in states_data:
            if state_info['name'] == state_name:
                for transition_obj in state_info['transitions']:
                    transition_name = transition_obj['transition_name']
                    next_state = transition_obj['next_state']
                    output = transition_obj['output']
                    next_node_label = f"q{next_state}/{output}"
                    if next_node_label in G:
                        G.add_edge(node_label, next_node_label, label=transition_name)

    pos = nx.circular_layout(G,scale=0.5)
    node_labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, node_size=700, node_color='lightgreen', with_labels=True, labels=node_labels, arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', connectionstyle='arc3,rad=0.1')
    plt.title("Moore from Mealy")
    plt.axis('off')
    plt.show()

def setStatesDataMealy():
    global states_data,num_transitions
    states_data.clear()
    for i in range(len(output_entries)):
        state_name = f"q{i+1}"
        state_transitions = []
        for j in range(num_transitions):
            transition_name = chr(97 + j)
            next_state = output_entries[i][j].get()  
            output = transition_entries[i][j].get()  
            transition_obj = {
                'transition_name': transition_name,
                'next_state': next_state,
                'output': output  
            }
            state_transitions.append(transition_obj)
        state = {
            'name': state_name,
            'transitions': state_transitions
        }
        states_data.append(state)

def displayMealy():
    setStatesDataMealy()
    G = nx.DiGraph()    
    for state_info in states_data:
       state_name = state_info['name']
       G.add_node(state_name, label=f"{state_name}")
    for state_info in states_data:
        state_name = state_info['name']
        state_transitions = state_info['transitions']
        for transition_obj in state_transitions:
            transition_name = transition_obj['transition_name']
            next_state = transition_obj['next_state']
            trans_output=transition_obj['output']
            next_state_with_q = f"q{next_state}"  
            G.add_edge(state_name, next_state_with_q, label=f"{transition_name}/{trans_output}")
    pos = nx.circular_layout(G)  
    node_labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, node_size=700, node_color='lightgreen', with_labels=True, labels=node_labels, arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', connectionstyle='arc3,rad=0.1')
    plt.title("Mealy Machine")
    plt.axis('off')
    plt.show()    
    
def generateMealy():
    setStatesDataMoore()
    G = nx.DiGraph()
    for state_info in states_data:
       state_name = state_info['name']
       G.add_node(state_name, label=f"{state_name}")
    for state_info in states_data:
        state_name = state_info['name']
        state_transitions = state_info['transitions']
        state_output=state_info['output']
        for transition_obj in state_transitions:
            transition_name = transition_obj['transition_name']
            next_state = transition_obj['next_state']
            next_state_with_q = f"q{next_state}"  
            G.add_edge(state_name, next_state_with_q, label=f"{transition_name}/{state_output}")

    pos = nx.circular_layout(G)  
    node_labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, node_size=700, node_color='lightgreen', with_labels=True, labels=node_labels, arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', connectionstyle='arc3,rad=0.1')

    plt.title("Mealy from moore")
    plt.axis('off')
    plt.show()


def setStatesDataMoore():
    global states_data
    states_data.clear()
    for i in range(len(state_entries)):
        state_name = f"q{i+1}"
        state_output = state_entries[i].get()
        state_transitions = []
        for j in range(num_transitions):
            transition_name = chr(97 + j)
            next_state = transition_entries[i][j].get()
            transition_obj = {
                'transition_name': transition_name,
                'next_state': next_state
            }
            state_transitions.append(transition_obj)
        state = {
            'name': state_name,
            'output': state_output,
            'transitions': state_transitions
        }
        states_data.append(state)

def inputFieldsMealy(num_states, num_transitions):
    global  transition_entries,output_entries,tkEntries
    tkEntries.clear()
    mealyToMoorePage.pack_forget()
    input_page = tk.Frame(window)

    
    for i in range(num_states):
        state_label = tk.Label(input_page, text=f"State q{i+1}:")
        state_label.grid(row=i*(num_transitions+1), column=0, pady=5)
        output_entry_row = []  
        transition_entry_row = []  
        for j in range(num_transitions):
            transition_label = tk.Label(input_page, text=f"Transition {chr(97 + j)}:")
            transition_label.grid(row=i*(num_transitions+1)+j, column=1, pady=5)
        
            output_label = tk.Label(input_page, text="Output:")
            output_label.grid(row=i*(num_transitions+1)+j, column=2, pady=5)

            output_entry = tk.Entry(input_page, width=10)
            tkEntries.append(output_entry)
            output_entry.grid(row=i*(num_transitions+1)+j, column=3, pady=5)
            
            transition_entry_row.append(output_entry)  
            next_state_label = tk.Label(input_page, text="Next State:")
            next_state_label.grid(row=i*(num_transitions+1)+j, column=4, pady=5)

            next_state_entry = tk.Entry(input_page, width=10)
            tkEntries.append(next_state_entry)
            next_state_entry.grid(row=i*(num_transitions+1)+j, column=5, pady=5)
            
            output_entry_row.append(next_state_entry)  
        
        transition_entries.append(transition_entry_row)  
        output_entries.append(output_entry_row)  

    
    backButton=tk.Button(input_page,text="<- Back",command= lambda:goBack(mealyToMoorePage,input_page))
    backButton.grid(row=num_states*(num_transitions+1), column=0, pady=10)
    
    display_button = tk.Button(input_page, text="Display Mealy", command=displayMealy)
    display_button.grid(row=num_states*(num_transitions+1), column=3, pady=10)

    generate_mealy_button = tk.Button(input_page, text="Generate Moore", command=generateMoore)
    generate_mealy_button.grid(row=num_states*(num_transitions+1), column=5,pady=10)
    input_page.pack()

def inputFieldsMoore(num_states, num_transitions):
    global state_entries, transition_entries,tkEntries
    tkEntries.clear()
    mooreToMealyPage.pack_forget()
    input_page = tk.Frame(window)
  
    for i in range(num_states):
        state_label = tk.Label(input_page, text=f"State q{i+1} Output:")
        state_entry = tk.Entry(input_page, width=30)
        tkEntries.append(state_entry)
        state_label.grid(row=i*(num_transitions+1), column=0, pady=5)
        state_entry.grid(row=i*(num_transitions+1), column=1, pady=5)
        state_entries.append(state_entry)  
        
        transition_entry_row = []
        for j in range(num_transitions):
            transition_label = tk.Label(input_page, text=f"Transition {chr(97 + j)}")
            transition_label.grid(row=i*(num_transitions+1)+j+1, column=0, pady=5)
    
            next_state_label = tk.Label(input_page, text=f"Next State")
            next_state_label.grid(row=i*(num_transitions+1)+j+1, column=1, pady=5)
            
            next_state_entry = tk.Entry(input_page, width=10)
            next_state_entry.grid(row=i*(num_transitions+1)+j+1, column=2, pady=5)
            tkEntries.append(next_state_entry)

            transition_entry_row.append(next_state_entry)

        transition_entries.append(transition_entry_row)  

    backButton=tk.Button(input_page,text="<- Back",command= lambda:goBack(mooreToMealyPage,input_page))
    backButton.grid(row=num_states*(num_transitions+1), column=0, pady=10)
  
    display_button = tk.Button(input_page, text="Display Moore", command=displayMoore)
    display_button.grid(row=num_states*(num_transitions+1), column=1, pady=10)
    generate_mealy_button = tk.Button(input_page, text="Generate Mealy", command=generateMealy)
    generate_mealy_button.grid(row=num_states*(num_transitions+1), column=2, pady=10)
    input_page.pack()

def displayMoore():
    setStatesDataMoore()
    G = nx.DiGraph()
    for state_info in states_data:
       state_name = state_info['name']
       state_output = state_info['output']
       if state_output:
        G.add_node(state_name, label=f"{state_name}/{state_output}")

    for state_info in states_data:
        state_name = state_info['name']
        state_transitions = state_info['transitions']
        for transition_obj in state_transitions:
            transition_name = transition_obj['transition_name']
            next_state = transition_obj['next_state']
            next_state_with_q = f"q{next_state}"  
            G.add_edge(state_name, next_state_with_q, label=transition_name)

    pos = nx.circular_layout(G)  
    node_labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, node_size=700, node_color='lightgreen', with_labels=True, labels=node_labels, arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', connectionstyle='arc3,rad=0.1')

    plt.title("Moore Machine")
    plt.axis('off')
    plt.show()

window = tk.Tk()
window.title("Moore & Mealy Converter")

width=420
height=100
window.minsize(width,height)

menuPage = tk.Frame(window)

moore_to_mealy_button = tk.Button(menuPage, text="Moore to Mealy", command=mooreToMealy)
mealy_to_moore_button = tk.Button(menuPage, text="Mealy to Moore", command=mealyToMoore)

moore_to_mealy_button.pack(pady=10,padx=20)
mealy_to_moore_button.pack(pady=10,padx=20)

menuPage.pack()

mooreToMealyPage = tk.Frame(window)

states_label_moore_to_mealy = tk.Label(mooreToMealyPage, text="Enter number of states:")
states_entry_moore_to_mealy = tk.Entry(mooreToMealyPage, width=20)
tkEntries.append(states_entry_moore_to_mealy)

transitions_label_moore_to_mealy = tk.Label(mooreToMealyPage, text="Enter number of transitions:")
transitions_entry_moore_to_mealy = tk.Entry(mooreToMealyPage, width=20)
tkEntries.append(transitions_entry_moore_to_mealy)

backButton=tk.Button(mooreToMealyPage,text="<- Back",command= lambda:goBack(menuPage,mooreToMealyPage))
proceedMooreToMealyButton = tk.Button(mooreToMealyPage, text="Proceed", command=proceedMooreToMealy)

states_label_moore_to_mealy.pack(pady=5)
states_entry_moore_to_mealy.pack(pady=5)
transitions_label_moore_to_mealy.pack(pady=5)
transitions_entry_moore_to_mealy.pack(pady=5)
backButton.pack(side=tk.LEFT,pady=10)
proceedMooreToMealyButton.pack(side=tk.RIGHT,pady=10)

mooreToMealyPage.pack_forget()


mealyToMoorePage = tk.Frame(window)
states_label_mealy_to_moore = tk.Label(mealyToMoorePage, text="Enter number of states:")
states_entry_mealy_to_moore = tk.Entry(mealyToMoorePage, width=20)
tkEntries.append(states_entry_mealy_to_moore)

transitions_label_mealy_to_moore = tk.Label(mealyToMoorePage, text="Enter number of transitions:")
transitions_entry_mealy_to_moore = tk.Entry(mealyToMoorePage, width=20)
tkEntries.append(transitions_entry_mealy_to_moore)

backButton=tk.Button(mealyToMoorePage,text="<- Back",command= lambda:goBack(menuPage,mealyToMoorePage))
proceedMealyToMooreButton= tk.Button(mealyToMoorePage, text="Proceed", command=proceedMealyToMoore)

mealyToMoorePage.pack_forget()

states_label_mealy_to_moore.pack(pady=5)
states_entry_mealy_to_moore.pack(pady=5)
transitions_label_mealy_to_moore.pack(pady=5)
transitions_entry_mealy_to_moore.pack(pady=5)
backButton.pack(side=tk.LEFT,pady=10,padx=5)
proceedMealyToMooreButton.pack(side=tk.RIGHT,pady=10)

window.mainloop()
