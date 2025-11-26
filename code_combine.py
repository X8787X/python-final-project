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
    # 發一張牌：採用標準 21 點（A=11，JQK=10），一般牌值 2~10
    card = random.choice([
        11,  # A
        2,3,4,5,6,7,8,9,10,  # 數字牌
        10,10,10  # J Q K
    ])
    return card

def calculate_score(cards):
    score = sum(cards)

    # 若 A 當 11 爆掉（> 21），把 A 改成 1
    while score > 21 and 11 in cards:
        cards[cards.index(11)] = 1
        score = sum(cards)

    return score

def compare(player_score, dealer_score):
    if player_score > 21:
        return "玩家爆牌，莊家勝"
    if dealer_score > 21:
        return "莊家爆牌，玩家勝"
    if player_score > dealer_score:
        return "玩家勝"
    if dealer_score > player_score:
        return "莊家勝"
    return "平手"


# ===== 玩家流程操作 (A 同學負責) =====
# 增加多玩家機制

def play_game():
    print("\n=== 🎮 開始一輪 Blackjack ===")

    # 多玩家輸入
    num_players = int(input("請輸入玩家人數（1~4）："))
    players = []

    for i in range(num_players):
        name = input(f"玩家 {i+1} 名字：")
        players.append({
            "name": name,
            "cards": [],
            "score": 0,
            "result": ""
        })

    # 莊家
    dealer_cards = []

    # → 發初始兩張牌
    for p in players:
        p["cards"] = [deal_card(), deal_card()]
    dealer_cards = [deal_card(), deal_card()]

    # → 顯示初始牌
    print("\n===== 初始發牌 =====")
    for p in players:
        print(f"{p['name']} 的牌：{p['cards']}（合計：{calculate_score(p['cards'])}）")
    print(f"莊家的明牌：{dealer_cards[0]}")

    # → 每位玩家依序行動
    for p in players:
        print(f"\n--- {p['name']} 的回合 ---")
        while True:
            score = calculate_score(p["cards"])
            print(f"目前牌：{p['cards']}（{score} 分）")

            if score > 21:
                print("💥 你爆牌了！")
                break

            choice = input("是否要牌？(y/n): ")
            if choice.lower() == "y":
                p["cards"].append(deal_card())
            else:
                break

    # → 莊家回合
    print("\n===== 莊家回合 =====")
    print(f"莊家起始牌：{dealer_cards}（{calculate_score(dealer_cards)}）")

    while calculate_score(dealer_cards) < 17:
        dealer_cards.append(deal_card())
        print(f"莊家補牌 → {dealer_cards}（{calculate_score(dealer_cards)}）")

    dealer_score = calculate_score(dealer_cards)

    # → 最終判定
    print("\n===== 最終結果 =====")
    for p in players:
        p["score"] = calculate_score(p["cards"])
        p["result"] = compare(p["score"], dealer_score)

        print(f"\n玩家：{p['name']}")
        print(f"你的牌：{p['cards']}（{p['score']} 分）")
        print(f"莊家：{dealer_cards}（{dealer_score} 分）")
        print(f"結果：{p['result']}")

        # 儲存紀錄
        save_game_result({
            "player": p["name"],
            "player_cards": p["cards"],
            "player_score": p["score"],
            "dealer_cards": dealer_cards,
            "dealer_score": dealer_score,
            "result": p["result"]
        })


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
