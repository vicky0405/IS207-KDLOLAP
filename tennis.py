import pandas as pd

# Đọc file CSV
df = pd.read_csv('atp_tennis.csv')

# 1. Loại bỏ các cột 'pts_1' và 'pts_2'
df_cleaned = df.drop(columns=['Pts_1', 'Pts_2'], errors='ignore')

# 2. Loại bỏ các dòng trong 2 cột 'odd_1' và 'odd_2' có giá trị là -1
df_cleaned = df_cleaned[(df_cleaned['Odd_1'] != -1) & (df_cleaned['Odd_2'] != -1)]

# 3. Tách cột 'score' thành 2 cột thể hiện số trận thắng của người chơi thứ 1 và thứ 2
def extract_set_wins(Score):
    if pd.isna(Score):  # Kiểm tra nếu giá trị là NaN
        return None, None

    # Tách tỉ số từng set
    sets = Score.split()

    player1_wins = 0
    player2_wins = 0

    for set_score in sets:
        try:
            player1_score, player2_score = map(int, set_score.split('-'))
        except ValueError:
            return None, None
        
        if player1_score > player2_score:
            player1_wins += 1
        else:
            player2_wins += 1

    return player1_wins, player2_wins

# Áp dụng hàm cho cột 'score' và tạo 2 cột mới 'player1_wins' và 'player2_wins'
df_cleaned[['player1_wins', 'player2_wins']] = df_cleaned['Score'].apply(lambda x: pd.Series(extract_set_wins(x)))

# Lưu lại dữ liệu vào file CSV mới
df_cleaned.to_csv('atp_tennis_cleaned.csv', index=False)
