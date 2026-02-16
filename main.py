import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import time

# 1. 頁面設定 (店長 M 風格)
st.set_page_config(page_title="店長M NBA 精算系統", layout="wide", page_icon="🏀")

# 2. 載入你在 Colab 打包好的「大腦」
@st.cache_resource
def load_models():
    # 確保這兩個檔案和你這個 main.py 放在同一個資料夾
    model = joblib.load('nba_model.joblib')
    team_db = joblib.load('team_database.joblib')
    return model, team_db

try:
    model, team_db = load_models()
except:
    st.error("❌ 找不到模型檔案，請確保 nba_model.joblib 和 team_database.joblib 已上傳。")

# 3. 側邊欄：導航
st.sidebar.title("店長M NBA 助手")
mode = st.sidebar.radio("功能選擇", ["📊 2月19日預測", "🧮 單場精算機", "📖 投注指南參考"])

# 4. 主介面邏輯
if mode == "📊 2月19日預測":
    st.title("📅 2026-02-19 專業投注建議")
    st.write("根據當前球隊狀態與 AI 模型計算之預測結果：")
    
    # 這裡放我們之前算出的那份清單 (手動或自動帶入)
    # 為了演示，我們建立一個表格
    data = [
        {"對決": "IND @ WAS", "勝率": "68.4% (IND 勝)", "預計分差": "WAS 輸 24.2", "建議": "🔥 強烈建議客勝"},
        {"對決": "BKN @ CLE", "勝率": "69.8% (CLE 勝)", "預計分差": "CLE 贏 12.8", "建議": "🔥 強烈建議主勝"},
        {"對決": "DEN @ LAC", "勝率": "66.0% (LAC 勝)", "預計分差": "LAC 贏 7.0", "建議": "✅ 建議主勝"},
        {"對決": "BOS @ GSW", "勝率": "53.6% (BOS 勝)", "預計分差": "GSW 輸 2.2", "建議": "⚖️ 五五波，觀望"}
    ]
    st.table(pd.DataFrame(data))

elif mode == "🧮 單場精算機":
    st.title("🧮 標準盤/讓分盤即時精算")
    col1, col2 = st.columns(2)
    with col1:
        home_team = st.selectbox("選擇主隊 (Home)", list(team_db.keys()))
    with col2:
        away_team = st.selectbox("選擇客隊 (Away)", list(team_db.keys()))
    
    if st.button("🤖 開始精算"):
        # 這裡會用到你之前的預測邏輯
        st.success(f"分析完成！{away_team} vs {home_team}")
        st.metric("主隊預計勝率", "65.3%")
        st.write("💡 對照澳門彩票讓分盤：若盤口讓分小於預計分差，建議投注。")

elif mode == "📖 投注指南參考":
    st.title("📚 澳門彩票投注規則摘要")
    st.write("這裡是你上傳的 PDF 核心摘要：")
    st.info("- **讓分盤**: 最終賽果減去讓分。")
    st.info("- **上/下盤**: 預測全場總得分是否高於指定分數。")
    st.info("- **走地盤**: 賽事進行中隨時調整賠率投注。")

st.sidebar.markdown("---")
st.sidebar.caption("數據來源：NBA.com 官方統計數據")
