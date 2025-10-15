# ===== 資料處理相關 (B 同學負責) =====

def save_game_result(result):
    # TODO: B 同學在這裡實作儲存遊戲結果（如勝負、玩家分數）
    print("功能開發中：儲存遊戲結果...")
    pass

def load_game_history():
    # TODO: B 同學在這裡實作讀取歷史紀錄
    print("功能開發中：讀取遊戲歷史...")
    return []

# ===== 遊戲邏輯核心 (A, C 同學負責) =====

import random

def deal_card():
    # TODO: A 同學負責，隨機發一張牌 (1-11)，代表 A 到 K
    print("功能開發中：發一張牌...")
    return random.randint(1, 11)

def calculate_score(cards):
    # TODO: C 同學負責，計算牌組分數（處理 A 的彈性為 1 或 11）
    print("功能開發中：計算手牌分數...")
    return sum(cards)

def compare(player_score, dealer_score):
    # TODO: C 同學負責，比較玩家與莊家的分數，回傳結果
    print("功能開發中：比較玩家與莊家的分數...")
    return "功能開發中"

# ===== 玩家流程操作 (A 同學負責) =====

def play_game():
    # TODO: A 同學實作完整一輪遊戲邏輯（玩家回合、莊家回合、勝負判定）
    print("功能開發中：遊戲流程開始...")
    player_cards = []
    dealer_cards = []

    # 發兩張牌
    for _ in range(2):
        player_cards.append(deal_card())
        dealer_cards.append(deal_card())

    print(f"你的牌: {player_cards}")
    print(f"莊家其中一張牌: {dealer_cards[0]}")

    # 玩家決定是否要牌 (Hit or Stand)
    game_over = False
    while not game_over:
        choice = input("要再拿一張牌嗎？(y/n): ")
        if choice.lower() == 'y':
            player_cards.append(deal_card())
            print(f"你現在的牌: {player_cards}")
            # 可加判斷是否爆牌
        else:
            game_over = True

    # 莊家回合邏輯
    # 可補上莊家必須補牌至 17 以上等邏輯

    # 計算分數與勝負
    player_score = calculate_score(player_cards)
    dealer_score = calculate_score(dealer_cards)

    result = compare(player_score, dealer_score)
    print(f"結果：{result}")

    # 儲存遊戲結果
    save_game_result({
        "player_cards": player_cards,
        "dealer_cards": dealer_cards,
        "result": result
    })

# ===== 主程式流程 (大家一起討論決定) =====

def main():
    while True:
        print("\n🎲 Blackjack 21 點遊戲")
        print("1. 開始遊戲")
        print("2. 查看歷史紀錄")
        print("3. 離開遊戲")

        choice = input("請選擇操作項目：")
        if choice == "1":
            play_game()
        elif choice == "2":
            history = load_game_history()
            print("（這裡顯示歷史紀錄...）")
            for game in history:
                print(game)
        elif choice == "3":
            print("感謝遊玩！再見 👋")
            break
        else:
            print("請輸入有效選項。")

# 程式執行入口
if __name__ == "__main__":
    main()
