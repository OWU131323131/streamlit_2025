import streamlit as st
from datetime import datetime, time
import os  # osモジュールをインポート

# カスタムCSSを適用
st.markdown(
    """
    <style>
    /* 背景色を変更 */
    .stApp {
        background-color: #f0f8ff; /* アリスブルー */
    }

    /* フォントを変更（全体適用） */適用） */
    html, body, [class*="css"]  {
        font-family: 'Comic Sans MS', cursive, sans-serif; /* Comic Sans MSを適用 */ MSを適用 */
        color: #333333; /* テキストの色 */
    }

    /* 見出しのデザイン */
    .stMarkdown h1, h2, h3 {
        color: #4CAF50; /* 緑色 */
        font-weight: bold;
    }

    /* ボタンのデザイン */
    button {
        background-color: #4CAF50; /* 緑色 */
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }

    /* アップロードセクションのデザイン */
    .stFileUploader {
        border: 2px dashed #4CAF50;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("日記アプリ")
#日付選択
date = st.date_input(
    label = "日付を選択してください",
    value = datetime.now(),
    help = "カレンダーから日付を選択"
)

st.write(f"選択した日付：{date}")
#テキス入力で日記を書く

if "text_history" not in st.session_state:
    st.session_state.text_history = []

text = st.text_input(
    label = "今日の出来事を記入してください",
    value = ""
)

st.write(f"今日の出来事:{text}")
if  st.session_state.text_history:
    for i, mood in enumerate(reversed(st.session_state.text_history)):
        st.write(f"{len(st.session_state.text_history) - i}. {text}")

st.markdown("---")
#保存ボタンでローカルファイルに保存
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []  # mood_historyを初期化

st.write("今日の気分を選んでください")

# 気分を選択するボタン
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("😊 嬉しい"):
        st.session_state.mood_history.append("😊 嬉しい")

with col2:
    if st.button("😢 悲しい"):
        st.session_state.mood_history.append("😢 悲しい")

with col3:
    if st.button("😴 眠い"):
        st.session_state.mood_history.append("😴 眠い")

with col4:
    if st.button("🍕 お腹すいた"):
        st.session_state.mood_history.append("🍕 お腹すいた")



# 気分履歴の表示
if st.session_state.mood_history:
    st.markdown("---")
    st.subheader("気分の履歴")
    for i, mood in enumerate(reversed(st.session_state.mood_history)):
        st.write(f"{len(st.session_state.mood_history) - i}. {mood}")
else:
    st.write("気分が選択されていません。")

SAVE_DIR = "diary_data/photos"
os.makedirs(SAVE_DIR, exist_ok=True)  # ディレクトリが存在しない場合は作成

# ユーザー識別情報を取得（例: ユーザー名を入力）
user_id = st.text_input("ユーザー名を入力してください", value="default_user")

# 写真アップロードセクション
st.markdown("---")
st.subheader("写真をアップロード")

uploaded_file = st.file_uploader("写真をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 保存するファイル名に日付を含める
    current_date = datetime.now().strftime('%Y-%m-%d')  # 現在の日付を取得
    photo_path = os.path.join(SAVE_DIR, f"{user_id}_{current_date}.jpg")
    
    # ファイルを保存
    with open(photo_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"写真を保存しました: {photo_path}")
    st.image(photo_path, caption="アップロードされた写真", use_column_width=True)
else:
    st.write("写真がアップロードされていません。")

# 写真の保存
if uploaded_file is not None:
    photo_dir = os.path.join(SAVE_DIR, "photos")
    os.makedirs(photo_dir, exist_ok=True)
    photo_path = os.path.join(photo_dir, f"{user_id}_{date.strftime('%Y-%m-%d')}.jpg")
    with open(photo_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"写真を保存しました: {photo_path}")
    st.image(photo_path, caption="アップロードされた写真", use_column_width=True)
else:
    st.write("写真がアップロードされていません。")

# 今日の出来事と気分を保存するボタン
if st.button("今日の出来事と気分を保存"):
    if text.strip() and st.session_state.mood_history:
        # 保存するファイルパスを設定
        diary_file = os.path.join(SAVE_DIR, f"{user_id}_diary.txt")
        mood_file = os.path.join(SAVE_DIR, f"{user_id}_mood_diary.txt")
        
        # 今日の出来事を保存
        with open(diary_file, "a", encoding="utf-8") as f:
            f.write(f"{date}: {text}\n")
            if photo_path:
                f.write(f"写真: {photo_path}\n")  # 写真のパスを記録
        st.session_state.text_history.append(text)
        
        # 今日の気分を保存
        with open(mood_file, "a", encoding="utf-8") as f:
            f.write(f"{date}: {st.session_state.mood_history[-1]}\n")
        
        st.success(f"{user_id} の今日の出来事、気分、写真を保存しました！")
    elif not text.strip():
        st.error("今日の出来事が空です。記入してください。")
    elif not st.session_state.mood_history:
        st.error("気分が選択されていません。選択してください。")

# 今日の出来事と気分を確認して保存する機能
st.markdown("---")
st.subheader("保存内容の確認")

# 今日の出来事と気分を表示
if text.strip():
    st.write(f"今日の出来事: {text}")
else:
    st.write("今日の出来事が記入されていません。")

if st.session_state.mood_history:
    st.write(f"選んだ気分: {st.session_state.mood_history[-1]}")
else:
    st.write("気分が選択されていません。")

# 保存先の確認
diary_file = os.path.join(SAVE_DIR, f"{user_id}_diary.txt")
mood_file = os.path.join(SAVE_DIR, f"{user_id}_mood_diary.txt")
st.write(f"保存先: {diary_file}")
st.write(f"保存先: {mood_file}")

# 保存しますかという言葉とボタン
if st.button("保存しますか"):
    if text.strip() and st.session_state.mood_history:
        # 今日の出来事を保存
        with open(diary_file, "a", encoding="utf-8") as f:
            f.write(f"{date}: {text}\n")
        st.session_state.text_history.append(text)
        
        # 今日の気分を保存
        with open(mood_file, "a", encoding="utf-8") as f:
            f.write(f"写真: {photo_path}\n")  # 写真のパスを記録
            f.write(f"{date}: {st.session_state.mood_history[-1]}\n")
        
        st.success(f"{user_id} の今日の出来事と気分を保存しました！")
    elif not text.strip():
        st.error("今日の出来事が空です。記入してください。")
    elif not st.session_state.mood_history:
        st.error("気分が選択されていません。選択してください。")

# 過去の日記を読み込んで表示
st.markdown("---")
st.subheader("過去の日記を表示")

selected_date = st.date_input(
    label="過去の日付を選択してください",
    value=datetime.now(),
    help="日付を選択して過去の日記を表示"
)

# 過去の日記を表示
try:
    diary_file = os.path.join(SAVE_DIR, f"{user_id}_diary.txt")
    with open(diary_file, "r", encoding="utf-8") as f:
        diary_entries = f.readlines()
        filtered_entries = [entry for entry in diary_entries if entry.startswith(str(selected_date))]
        if filtered_entries:
            st.write("過去の日記:")            
        else:
            st.write("選択した日付の日記はありません。")
except FileNotFoundError:
    st.error(f"{user_id} の日記ファイルが見つかりません。")

# 選択した日付の気分を表示
try:
    mood_file = os.path.join(SAVE_DIR, f"{user_id}_mood_diary.txt")  # ユーザーごとのファイルパス
    with open(mood_file, "r", encoding="utf-8") as f:
        mood_entries = f.readlines()
        filtered_moods = [entry for entry in mood_entries if entry.startswith(str(selected_date))]
        if filtered_moods:
            st.write("過去の気分:")
            for mood in filtered_moods:
                st.write(mood.strip())
        else:
            st.write("選択した日付の気分はありません。")
except FileNotFoundError:
    st.error(f"{user_id} の気分ファイルが見つかりません。")

try:
    # 保存ディレクトリ内のファイルを検索
    photos = [f for f in os.listdir(SAVE_DIR) if f.startswith(f"{user_id}_{selected_date.strftime('%Y-%m-%d')}")]
    if photos:
        st.write(f"選択した日付 ({selected_date.strftime('%Y-%m-%d')}) の写真:")
        for photo in photos:
            photo_path = os.path.join(SAVE_DIR, photo)
            st.image(photo_path, caption=f"保存された写真: {photo}", use_column_width=True)
    else:
        st.write("選択した日付の写真はありません。")
except Exception as e:
    st.error(f"エラーが発生しました: {e}")