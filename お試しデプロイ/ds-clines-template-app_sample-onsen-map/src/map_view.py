"""
温泉データをマップ表示するモジュール
"""
import folium
import pandas as pd
from folium.plugins import MarkerCluster
from typing import Dict, List, Optional, Tuple


class OnsenMapView:
    """温泉マップ表示クラス"""

    def __init__(self, center: Tuple[float, float] = (36.0, 138.0), zoom: int = 5):
        """
        初期化
        
        Args:
            center: 地図の中心座標 (緯度, 経度)
            zoom: ズームレベル
        """
        self.center = center
        self.zoom = zoom
        
    def create_base_map(self) -> folium.Map:
        """
        ベースとなる日本地図を作成
        
        Returns:
            Foliumマップオブジェクト
        """
        map_obj = folium.Map(
            location=self.center,
            zoom_start=self.zoom,
            tiles="OpenStreetMap",
            control_scale=True
        )
        
        return map_obj
    
    def add_onsen_markers(self, map_obj: folium.Map, onsen_data: pd.DataFrame, 
                          use_clustering: bool = True) -> folium.Map:
        """
        温泉のマーカーをマップに追加
        
        Args:
            map_obj: Foliumマップオブジェクト
            onsen_data: 温泉データを含むDataFrame
            use_clustering: クラスタリングを使用するかどうか
            
        Returns:
            マーカーを追加したマップオブジェクト
        """
        # マーカークラスタリング用レイヤーを作成
        if use_clustering:
            marker_cluster = MarkerCluster().add_to(map_obj)
        
        # 温泉データの各行に対してマーカーを作成
        for _, row in onsen_data.iterrows():
            # 緯度・経度がない場合はスキップ
            if pd.isnull(row.get("緯度")) or pd.isnull(row.get("経度")):
                continue
            
            # マーカーのポップアップ内容を作成
            popup_text = f"""
                <div style="font-family: sans-serif; width: 250px;">
                    <h4>{row.get("名称", "不明")}</h4>
                    <p><strong>所在地:</strong> {row.get("所在地", "不明")}</p>
                    <p><strong>都道府県:</strong> {row.get("都道府県", "不明")}</p>
                    <p><strong>泉質:</strong> {row.get("泉質", "不明")}</p>
                    <p><strong>効能:</strong> {row.get("効能", "不明")}</p>
                </div>
            """
            popup = folium.Popup(popup_text, max_width=300)
            
            # マーカーオブジェクトを作成
            icon = folium.Icon(
                color="red",
                icon="tint",  # 温泉を表す水滴のアイコン
                prefix="fa"
            )
            
            marker = folium.Marker(
                location=[row["緯度"], row["経度"]],
                popup=popup,
                tooltip=row.get("名称", "不明"),
                icon=icon
            )
            
            # マーカーをマップまたはクラスタに追加
            if use_clustering:
                marker.add_to(marker_cluster)
            else:
                marker.add_to(map_obj)
        
        return map_obj
    
    def create_choropleth(self, map_obj: folium.Map, onsen_data: pd.DataFrame) -> folium.Map:
        """
        都道府県ごとの温泉数を色分け表示するコロプレス図を追加
        
        Args:
            map_obj: Foliumマップオブジェクト
            onsen_data: 温泉データを含むDataFrame
            
        Returns:
            コロプレス図を追加したマップオブジェクト
        """
        # TODO: 都道府県のGeoJSONデータを取得し、温泉数でコロプレス図を作成
        # 現在は実装していませんが、将来的な拡張のために関数を用意
        return map_obj
    
    def add_prefecture_filter_control(self, map_obj: folium.Map, 
                                      prefectures: List[str]) -> folium.Map:
        """
        都道府県フィルターコントロールを追加
        
        Args:
            map_obj: Foliumマップオブジェクト
            prefectures: 都道府県リスト
            
        Returns:
            フィルターコントロールを追加したマップオブジェクト
        """
        # TODO: カスタムコントロールを実装
        # 現在のFoliumではStreamlitと連携して実装する予定
        return map_obj
    
    def generate_map_html(self, onsen_data: pd.DataFrame, 
                         output_file: str = "onsen_map.html") -> str:
        """
        温泉データからHTMLマップを生成
        
        Args:
            onsen_data: 温泉データを含むDataFrame
            output_file: 出力HTMLファイル名
            
        Returns:
            生成したHTMLファイルのパス
        """
        # ベースマップの作成
        map_obj = self.create_base_map()
        
        # マーカーの追加
        map_obj = self.add_onsen_markers(map_obj, onsen_data)
        
        # マップをHTMLとして保存
        map_obj.save(output_file)
        
        return output_file
