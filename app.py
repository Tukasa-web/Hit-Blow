import streamlit as st
import pandas as pd
import random

#------タイトル-----
st.title("Hit & Blow")
st.write("数字を当てよう!!")

#-----ゲーム実装関数-----
# 4桁生成関数
def answer():
    ans = list(range(10))
    random.shuffle(ans)
    return ans[:4]

# 判定関数
def judge(guess, answer):
    hit = 0
    blow = 0

    for i in range(4):
        if guess[i] == answer[i]:
            hit += 1
        elif guess[i] in answer:
            blow += 1

    return hit, blow

# 結果メッセージ関数
def check(hit):
    if hit == 4:
        st.success("クリア!!")
        st.audio("clear.mp3")
    else:
        st.error("ハズレ！")
        st.audio("miss.mp3")

# guess判定関数
def valid(gue):
    if len(gue) != 4:
        st.write("4桁で入力してください")
        return False

    if not gue.isdigit():
        st.write("数字だけで入力してください")
        return False

    if len(set(gue)) != 4:
        st.write("数字は重複させないでください")
        return False

    return True

# 回数カウント関数
def show_turn():
    st.write(f"{st.session_state.count} 回目")

# ----ゲーム実装----
# session_state 初期化
if "ans" not in st.session_state:
    st.session_state.ans = answer()

if "hit" not in st.session_state:
    st.session_state.hit = 0

if "count" not in st.session_state:
    st.session_state.count = 0

if "playing" not in st.session_state:
    st.session_state.playing = True

if "history" not in st.session_state:
    st.session_state.history = []

# 入力
gue = st.text_input("予測を入れてください（4桁）")

# 判定ボタン
if st.button("判定"):

    if not valid(gue):
        st.stop()

    st.session_state.count += 1
    st.write(f"### {st.session_state.count} 回目")

    guess_list = [int(x) for x in gue]
    hit, blow = judge(guess_list, st.session_state.ans)
    st.session_state.hit = hit

    # 履歴
    count = len(st.session_state.history) + 1

    st.session_state.history.append({
    "回数": count,
    "予測": gue,
    "Hit": hit,
    "Blow": blow
    })

    st.write(f"hit : {hit}")
    st.write(f"blow : {blow}")

    # 判定
    check(hit)
    if hit == 4:
        st.session_state.playing = False

# クリア後のボタン
if not st.session_state.playing:
    if st.button("もう一度遊ぶ"):
        st.session_state.ans = answer()
        st.session_state.hit = 0
        st.session_state.count = 0
        st.session_state.playing = True
        st.session_state.history = []
        st.rerun()

#-----サイドバー-----
st.sidebar.title("プレイ履歴")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.sidebar.dataframe(df, use_container_width=True)
else:
    st.sidebar.write("まだ履歴はありません")
