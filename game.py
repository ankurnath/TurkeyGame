import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Initialize the app
app = dash.Dash(__name__)

# Helper function to check for a winner and return the winning combination
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6],             # Diagonals
    ]
    
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "":
            return board[combo[0]], combo  # Return both the winner and the winning combination
    
    if "" not in board:
        return "Draw", []  # No winner, but it's a draw
    
    return None, []  # No winner yet

# Define layout
app.layout = html.Div(
    style={
        'display': 'flex', 
        'flexDirection': 'column', 
        'justifyContent': 'center', 
        'alignItems': 'center', 
        'height': '100vh',  
        'textAlign': 'center'
    },
    children=[
        html.H1("Tic-Tac-Toe"),
        html.Div(id='game-status', children="Player X's Turn"),
        html.Div(
            style={
                'display': 'grid', 
                'grid-template-columns': 'repeat(3, 100px)', 
                'grid-gap': '10px'
            },
            children=[
                html.Button('', id=f'cell-{i}', style={'width': '100px', 'height': '100px', 'fontSize': '30px'}) 
                for i in range(9)
            ]
        ),
        html.Button('Restart', id='restart-button', n_clicks=0),
        dcc.Store(id='board-state', data=[""] * 9),
        dcc.Store(id='current-player', data='X'),
    ]
)

# Callback to update the board and style the winning cells
@app.callback(
    [Output(f'cell-{i}', 'children') for i in range(9)] + [
        Output('game-status', 'children'),
        Output('board-state', 'data'),
        Output('current-player', 'data')
    ] + [Output(f'cell-{i}', 'style') for i in range(9)],
    [Input(f'cell-{i}', 'n_clicks') for i in range(9)] + [Input('restart-button', 'n_clicks')],
    [State(f'cell-{i}', 'children') for i in range(9)] + [State('board-state', 'data'), State('current-player', 'data')]
)
def update_board(*args):
    ctx = dash.callback_context
    board_clicks = args[:9]
    restart_click = args[9]
    board_content = args[10:19]
    board = args[19]
    current_player = args[20]
    
    # Default button styles
    default_style = {'width': '100px', 'height': '100px', 'fontSize': '30px'}
    
    # If the game is being restarted
    if 'restart-button' in ctx.triggered[0]['prop_id']:
        return ([""] * 9 + ["Player X's Turn", [""] * 9, "X"] + [default_style] * 9)
    
    # If a cell was clicked, update the board
    for i in range(9):
        if f'cell-{i}' in ctx.triggered[0]['prop_id'] and board_content[i] == "":
            board[i] = current_player
            winner, winning_combo = check_winner(board)
            
            if winner:
                styles = [default_style] * 9
                # Highlight the winning combination
                if winner != "Draw":
                    for idx in winning_combo:
                        styles[idx] = {'width': '100px', 'height': '100px', 'fontSize': '30px', 'backgroundColor': 'lightgreen'}
                    return (*board, f"{winner} wins!", board, current_player, *styles)
                return (*board, "It's a draw!", board, current_player, *styles)
            
            # Switch turns
            next_player = 'O' if current_player == 'X' else 'X'
            return (*board, f"Player {next_player}'s Turn", board, next_player, *[default_style] * 9)
    
    return (*board_content, f"Player {current_player}'s Turn", board, current_player, *[default_style] * 9)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
