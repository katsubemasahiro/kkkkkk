"""
日本100名泉マップアプリケーション
"""
import os
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium

from data_collector import OnsenDataCollector
from data_loader import OnsenDataLoader
from map_view import OnsenMapView

# ページ設定
st.set_page_config(
    page_title="日本100名泉マップ!!",
    page_icon="♨️",
    layout="wide"
)

# データパス
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CSV_PATH = os.path.join(DATA_DIR, "onsen_data.csv")

def collect_onsen_data():
    """温泉データを収集する"""
    with st.spinner("温泉データを収集しています..."):
        collector = OnsenDataCollector(output_dir=DATA_DIR)
        collector.run_collection()
    st.success("温泉データの収集が完了しました！")

def load_onsen_data():
    """温泉データをロードする"""
    try:
        # JSONファイルからデータをロード
        loader = OnsenDataLoader(data_dir=DATA_DIR)
        try:
            df = pd.DataFrame(loader.load_from_json())
            return df
        except:
            # 例外が発生した場合はCSVを試す
            df = loader.load_from_csv()
            return df
    except FileNotFoundError:
        st.warning("温泉データが見つかりません。")
        return None

def display_map(df):
    """温泉マップを表示する"""
    if df is None or len(df) == 0:
        st.warning("表示できるデータがありません。")
        return
    
    # 位置情報があるデータのみを抽出
    map_data = df.dropna(subset=["緯度", "経度"])
    
    if len(map_data) == 0:
        st.warning("位置情報が含まれているデータがありません。")
        return
    
    # マップの作成
    map_view = OnsenMapView()
    map_obj = map_view.create_base_map()
    map_obj = map_view.add_onsen_markers(map_obj, map_data)
    
    # マップの表示
    folium_static(map_obj, width=1000, height=600)

def display_onsen_info(df):
    """温泉情報を表示する"""
    if df is None or len(df) == 0:
        return
    
    st.write(f"**全{len(df)}件の温泉データ**")
    
    # 都道府県での絞り込み
    prefectures = sorted(df["都道府県"].unique())
    selected_prefecture = st.selectbox(
        "都道府県で絞り込み", 
        ["すべて"] + list(prefectures)
    )
    
    if selected_prefecture != "すべて":
        filtered_df = df[df["都道府県"] == selected_prefecture]
    else:
        filtered_df = df
    
    # 温泉名での検索
    search_query = st.text_input("温泉名で検索")
    if search_query:
        filtered_df = filtered_df[filtered_df["名称"].str.contains(search_query)]
    
    # 結果の表示
    st.write(f"**{len(filtered_df)}件の温泉が見つかりました**")
    
    # データテーブルの表示
    if not filtered_df.empty:
        st.dataframe(
            filtered_df[["名称", "都道府県", "所在地", "泉質", "効能"]],
            use_container_width=True,
            hide_index=True
        )
    
def main():
    """メイン関数"""
    # ヘッダー
    st.title("♨️ 日本100名泉マップ!!!")
    st.markdown("""
    日本全国の名湯をインタラクティブなマップで探索できるアプリケーションです。
    温泉の場所や詳細情報を簡単に確認できます。
    """)
    
    # サイドバー
    with st.sidebar:
        st.header("操作パネル")
        
        # 手動データ使用に関する注釈
        st.info("日本の名湯データは手動で作成されています!!!")
        
        st.divider()
        
        # 表示設定
        st.subheader("表示設定")
        show_map = st.checkbox("マップを表示", value=True)
        show_data = st.checkbox("データ一覧を表示", value=True)
        
        st.divider()
        
        # アプリ情報
        st.markdown("### このアプリについて")
        st.markdown("""
        - データソース: Wikipedia
        - 地図: OpenStreetMap
        - 作成者: Cline
        """)
    
    # メインコンテンツ
    # データの読み込み
    df = load_onsen_data()
    
    # マップ表示
    if show_map:
        st.header("温泉マップ")
        display_map(df)
    
    # データ表示
    if show_data:
        st.header("温泉データ一覧")
        display_onsen_info(df)

if __name__ == "__main__":
    main()
