import numpy as np
import pandas as pd
import plotly.express as px


f = open("data/lichess_db_standard_rated_2018-01.pgn")
    
def main():
    a, m = get_two_dfs()
    
    
def get_next_analysed_game():
    # Пока не найдем игру с анализом
    while True:
        # Записываем строки игры
        buffer = []
        while True:
            line = f.readline()

            # Пустые строки не нужны
            if line == "\n":
                continue

            buffer.append(line)

            # Ходы идут последней строкой в игре
            # и всегда начинаются с "1."
            if line.startswith("1."):
                break
        
        if ("%eval" in line):
            return buffer
        

def params_to_dict(str_list):
    """
    Принимает строки в виде
    [key "value"]
    И переводит их в словарь
    https://en.wikipedia.org/wiki/Portable_Game_Notation
    """
    return {
        a: b.strip('"') 
        for a, b in [
            i.strip("\n").strip("[]").split(" ", 1) 
            for i in str_list
        ]
    }


def moves_to_dict(moves):
    s = moves.split(" ")
    s = s[:-1]
    
    # Если последний ход - мат, для него нет оценки позиции (игра окончена)
    # Поэтому слайсы сдвигаются, время не в той колонке
    # Чтобы исправить, чуть подправим в конце
    if len(s) % 8 != 0:
        s.append(s[-2])
        s[-3] = "Game Over"
    
    return {
        "WhiteMove": s[1::16],
        "WhiteEval": [i.strip("[]") for i in s[4::16]],
        "WhiteTime": [i.strip("[]") for i in s[6::16]],
        
        "BlackMove": s[9::16],
        "BlackEval": [i.strip("[]") for i in s[12::16]],
        "BlackTime": [i.strip("[]") for i in s[14::16]],
    }


def get_and_parse_next_analysed_game():
    game = get_next_analysed_game()
    return {
        **params_to_dict(game[:-1]),
        **moves_to_dict(game[-1])
    }
    
    
def get_moves_df(game):
    df = pd.DataFrame.from_dict({
        
        "WhiteMove": game["WhiteMove"],
        "WhiteEval": game["WhiteEval"],
        "WhiteTime": game["WhiteTime"],
        
        "BlackMove": game["BlackMove"],
        "BlackEval": game["BlackEval"],
        "BlackTime": game["BlackTime"],
    
    }, orient="index").transpose()
    
    df["MoveNumber"] = df.index + 1
    
    return df


def get_two_dfs():
    a = get_and_parse_next_analysed_game()
    m = get_moves_df(a)
    return a, m
    
    
if __name__ == "__main__":
    main()