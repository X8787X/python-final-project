import json
import os
import random

HISTORY_FILE = "game_history.txt"
STATE_FILE = "player_state.json"

# 歷史紀錄
def ensure_history_file_exists():# 確認有歷史紀錄的檔案
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def load_game_history():# 加載檔案
    ensure_history_file_exists()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_game_result(record):# 存檔
    ensure_history_file_exists()
    history = load_game_history()
    history.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# 籌碼計算
def ensure_state_file_exists():
    #如果找不到紀錄，就建立一個 chips=1000
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"chips": 1000}, f, ensure_ascii=False, indent=2)

def load_player_state():
    # 讀取玩家籌碼數
    ensure_state_file_exists()
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_player_state(state):
    # 存檔
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# 撲克牌庫
unicode_cards = {
    "♠": {1:"🂡", 2:"🂢", 3:"🂣", 4:"🂤", 5:"🂥", 6:"🂦", 7:"🂧", 8:"🂨", 9:"🂩", 10:"🂪", 11:"🂫", 12:"🂭", 13:"🂮"},
    "♥": {1:"🂱", 2:"🂲", 3:"🂳", 4:"🂴", 5:"🂵", 6:"🂶", 7:"🂷", 8:"🂸", 9:"🂹", 10:"🂺", 11:"🂻", 12:"🂽", 13:"🂾"},
    "♦": {1:"🃁", 2:"🃂", 3:"🃃", 4:"🃄", 5:"🃅", 6:"🃆", 7:"🃇", 8:"🃈", 9:"🃉", 10:"🃊", 11:"🃋", 12:"🃍", 13:"🃎"},
    "♣": {1:"🃑", 2:"🃒", 3:"🃓", 4:"🃔", 5:"🃕", 6:"🃖", 7:"🃗", 8:"🃘", 9:"🃙", 10:"🃚", 11:"🃛", 12:"🃝", 13:"🃞"}
}

suits = ["♠", "♥", "♦", "♣"]
card_back = "🂠"


# 發牌
def deal_card():
    suit = random.choice(suits)
    rank = random.randint(1, 13)

    if rank == 1:
        value = 11
    elif rank >= 11:
        value = 10
    else:
        value = rank

    return {
        "suit": suit,
        "rank": rank,
        "value": value,
        "symbol": unicode_cards[suit][rank]
    }

# 計分
def calculate_score(cards):
    values = [c["value"] for c in cards]

    # 21點直接勝利
    if sum(values) == 21 and len(values) == 2:
        return 0

    # ACE特殊規則
    if 11 in values and sum(values) > 21:
        ace = next(c for c in cards if c["value"] == 11)
        ace["value"] = 1

    return sum(c["value"] for c in cards)


def compare(user_score, dealer_score):
    if user_score == dealer_score:
        return "平手"
    elif dealer_score == 0:
        return "莊家勝"
    elif user_score == 0:
        return "玩家勝"
    elif user_score > 21:
        return "玩家爆牌，莊家勝"
    elif dealer_score > 21:
        return "莊家爆牌，玩家勝"
    elif user_score > dealer_score:
        return "玩家勝"
    else:
        return "莊家勝"


# 讓輸出好看一點、隱藏莊家手牌
def format_cards(cards, hide_second=False):
    symbols = []
    nums = []

    for i, c in enumerate(cards):
        if hide_second and i >= 1:
            symbols.append(card_back)
            nums.append("?")
        else:
            symbols.append(c["symbol"])
            nums.append(f'{c["suit"]}{c["value"]}')

    return f"{' '.join(symbols)}  [{', '.join(nums)}]"


def format_history_cards(cards):
    return " ".join([c["symbol"] for c in cards])


# 遊戲主程式

def play_game(chips):

    print(f"🂡 新的一局開始！目前籌碼：{chips}")

    # 下注
    while True:
        try:
            bet = int(input("請輸入下注金額："))
            if bet <= 0:
                print("下注金額要大於 0")
            elif bet > chips:
                print("你沒有那麼多籌碼！")
            else:
                break
        except:
            print("請輸入有效數字！")

    user_cards = [deal_card(), deal_card()]
    dealer_cards = [deal_card(), deal_card()]

    game_over = False

    while not game_over:
        user_score = calculate_score(user_cards)
        dealer_score = calculate_score(dealer_cards)

        print(f"\n你的牌: {format_cards(user_cards)}, 分數: {user_score}")
        print(f"莊家的牌: {format_cards(dealer_cards, hide_second=True)}")

        if user_score == 0 or dealer_score == 0 or user_score > 21:
            game_over = True
        else:
            choice = input("要不要補牌? 輸入'是'或'否'：")
            if choice == "是":
                user_cards.append(deal_card())
            else:
                game_over = True

    # 莊家補牌
    while dealer_score != 0 and dealer_score < 17:
        dealer_cards.append(deal_card())
        dealer_score = calculate_score(dealer_cards)

    print("\n===== 最終結果 =====")
    print(f"你的牌: {format_cards(user_cards)}, 分數: {user_score}")
    print(f"莊家的牌: {format_cards(dealer_cards)}, 分數: {dealer_score}")

    result = compare(user_score, dealer_score)
    print("結果：", result)

    chips_before = chips

    if "玩家勝" in result:
        chips += bet
    elif "莊家勝" in result:
        chips -= bet

    print(f"籌碼：{chips_before} → {chips}")

    record = {
        "user_cards": user_cards,
        "dealer_cards": dealer_cards,
        "user_score": user_score,
        "dealer_score": dealer_score,
        "result": result,
        "chips_before": chips_before,
        "bet": bet,
        "chips_after": chips
    }

    save_game_result(record)

    # 回傳更新後的籌碼給 main()
    return chips


# 主函式
def main():
    ensure_history_file_exists()
    # 讀取玩家狀態（包含籌碼）
    state = load_player_state()
    chips = state.get("chips", 1000)

    while True:
        print("\n Blackjack 21 點遊戲")
        print(f"目前籌碼：{chips}")
        print("1. 開始遊戲")
        print("2. 查看歷史紀錄")
        print("3. 統計勝負")
        print("4. 離開遊戲")

        choice = input("請選擇功能：")

        if choice == "1":
            if chips <= 0:
                print("你已經沒有籌碼了，按4來查看戰績和數據...")
                continue

            chips = play_game(chips)
            # 每玩完一局就把籌碼寫回檔案
            save_player_state({"chips": chips})

        elif choice == "2":
            history = load_game_history()
            print("\n=====  歷史紀錄 =====")
            for h in history:
                print(
                    f"玩家: {format_history_cards(h['user_cards'])} "
                    f"莊家: {format_history_cards(h['dealer_cards'])} "
                    f"結果: {h['result']}  "
                    f"籌碼: {h['chips_before']} → {h['chips_after']}"
                )

        elif choice == "3":
            history = load_game_history()
            print("\n=====  勝負統計 =====")
            win = sum(1 for h in history if "玩家勝" in h["result"])
            lose = sum(1 for h in history if "莊家勝" in h["result"])
            tie = sum(1 for h in history if "平手" in h["result"])
            print(f"玩家勝：{win}")
            print(f"莊家勝：{lose}")
            print(f"平手：{tie}")

        elif choice == "4":
            # 離開前存一次目前籌碼
            save_player_state({"chips": chips})

            history = load_game_history()
            print("\n=====  本次遊玩總結（依歷史紀錄） =====")
            total = len(history)

            if total > 0:
                win = sum(1 for h in history if "玩家勝" in h["result"])
                rate = win / total * 100
                print(f"總局數：{total}")
                print(f"玩家勝：{win}")
                print(f"勝率：{rate:.2f}%")
            else:
                print("沒有紀錄，無法計算勝率")

            print(f"\n離開時籌碼餘額：{chips}")
            print("\n感謝遊玩！再見 ")
            break

        else:
            print("請輸入有效選項！")


if __name__ == "__main__":

    main()



