import numpy as np
import pandas as pd
import plotly.express as px


f = open("data/lichess_db_standard_rated_2018-01.pgn")
    
def main():
    a, m = get_and_parse_next_analysed_game()
    
    
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
   
    
def moves_to_df(moves):
    s = moves.replace("[", "").replace("]", "")
    s = s.split(" ")
    s = s[:-1]
    
    # Если последний ход - мат, для него нет оценки позиции (игра окончена)
    # Поэтому слайсы сдвигаются, время не в той колонке
    # Чтобы исправить, чуть подправим в конце
    if len(s) % 8 != 0:
        s.append(s[-2])
        s[-3] = "Checkmate"

    df = pd.DataFrame.from_dict({
                
        "WhiteMove": s[1::16],
        "WhiteEval": s[4::16],
        "WhiteTime": s[6::16],
        
        "BlackMove": s[9::16],
        "BlackEval": s[12::16],
        "BlackTime": s[14::16],
    
    }, orient="index").transpose()
    
    df["MoveNumber"] = df.index + 1
    
    # Анализ доступен только для первых 100 ходов
    # Строчки без него не нужны
    df = df.head(100)

    return df


def get_and_parse_next_analysed_game():
    game = get_next_analysed_game()
    return (
        params_to_dict(game[:-1]), 
        moves_to_df(game[-1])
    )
    
    
if __name__ == "__main__":
    main()