# ===== 資料+籌碼處理相關 (B 同學負責) =====
# 有餘裕:最後印出勝負局數，贏錢數、賠錢數

import json
import os
import random

HISTORY_FILE = "game_history.txt"

def save_game_result(result):
    # 儲存遊戲結果到本地檔案
    history = load_game_history()
    history.append(result)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_game_history():
    # 讀取遊戲歷史
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ===== 遊戲邏輯核心 ( C 同學負責) =====

def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    card = random.choice(cards)
    return card

def calculate_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0

    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)

    return sum(cards)

def compare(u_score, c_score):
    if u_score == c_score:
        return "平手"
    elif c_score == 0:
        return "莊家勝"
    elif u_score == 0:
        return "玩家勝"
    elif u_score > 21:
        return "玩家爆牌，莊家勝"
    elif c_score > 21:
        return "莊家爆牌，玩家勝"
    elif u_score > c_score:
        return "玩家勝"
    else:
        return "莊家勝"


# ===== 玩家流程操作 (A 同學負責) =====
# 增加多玩家機制

def play_game():
    print(logo)
    user_cards = []
    computer_cards = []
    computer_score = -1
    user_score = -1
    is_game_over = False

    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())

    while not is_game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
        print(f"Your cards: {user_cards}, current score: {user_score}")
        print(f"Computer's first card: {computer_cards[0]}")

        if user_score == 0 or computer_score == 0 or user_score > 21:
            is_game_over = True
        else:
            user_should_deal = input("Type 'y' to get another card, type 'n' to pass: ")
            if user_should_deal == "y":
                user_cards.append(deal_card())
            else:
                is_game_over = True

    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    print(f"Your final hand: {user_cards}, final score: {user_score}")
    print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
    print(compare(user_score, computer_score))


while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ") == "y":
    print("\n" * 20)
    play_game()


# ===== 主程式流程 =====

def main():
    while True:
        print("\n🎲 Blackjack 21 點遊戲")
        print("1. 開始遊戲")
        print("2. 查看歷史紀錄")
        print("3. 統計勝負")
        print("4. 離開遊戲")

        choice = input("請選擇操作項目：")
        if choice == "1":
            play_game()
        elif choice == "2":
            history = load_game_history()
            print("\n=== 📜 歷史紀錄 ===")
            for game in history:
                print(game)
        elif choice == "3":
            history = load_game_history()
            print("\n=== 📊 勝負統計 ===")
            count_win = sum(1 for h in history if "玩家勝" in h["result"])
            count_lose = sum(1 for h in history if "莊家勝" in h["result"])
            count_tie = sum(1 for h in history if "平手" in h["result"])
            print(f"玩家勝：{count_win}")
            print(f"莊家勝：{count_lose}")
            print(f"平手：{count_tie}")
        elif choice == "4":
            print("感謝遊玩！再見 👋")
            break
        else:
            print("請輸入有效選項。")


if __name__ == "__main__":
    main()
