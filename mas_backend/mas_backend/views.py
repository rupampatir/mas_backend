from django.shortcuts import render
import os
import numpy as np
import random as random
import pickle
from django.http import JsonResponse


policy_1_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'policy_Q_1')
policy_1 = pickle.load(open(policy_1_path, "rb"))
policy_2_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'policy_Q_2')
policy_2 = pickle.load(open(policy_2_path, "rb"))


def home(request):    
    return render(request, 'index.html')

def get_available_squares(board):
    available_squares = []
    for row in range(3):
      for column in range(3):
        if board[row][column] == 0:
          available_squares.append((row,column))
    return available_squares

def get_hash(board):
    board_hash = str(board.astype(int).reshape(3 * 3))
    return board_hash

def chooseAction_QTable(current_board, start_player):
        policy = None
        if (start_player=='2'):
            print('computer starts')
            policy = policy_1
        else:
            print('human starts')
            policy = policy_2
        exp_rate = 0.3
        positions = get_available_squares(current_board)
        current_state = get_hash(current_board)
        best_action = []
        best_action_value = -np.Inf
        for action in positions:
            Q_s_a = policy[current_state][action]
            if Q_s_a == best_action_value:
                best_action.append(action)
            elif Q_s_a > best_action_value:
                best_action = [action]
                best_action_value = Q_s_a
        best_action = random.choice(best_action)
        
        n_actions =len(positions)
        p = np.full(n_actions,exp_rate/n_actions)
        p[positions.index(best_action)]+= 1 - exp_rate
      
        return positions[np.random.choice(len(positions),p=p)]
        

# our result page view
def get_tic_tac_toe_action(request):
    print(request)
    observation = request.GET.get('board')
    start_player = request.GET.get('start_player')
    observation = observation[1:-1]
    parsed = [-1 if ob=='2' else int(ob) for ob in observation]
    optimalAction = chooseAction_QTable(np.array(parsed).reshape((3,3)), start_player)
    print(optimalAction)
    return JsonResponse({"action":optimalAction}, safe=False)