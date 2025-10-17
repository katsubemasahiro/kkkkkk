"""
温泉データ読み込み用モジュール
"""
import os
import json
import pandas as pd
from typing import Dict, List, Optional


class OnsenDataLoader:
    """温泉データ読み込みクラス"""

    def __init__(self, data_dir: str = "../data"):
        """
        初期化
        
        Args:
            data_dir: データディレクトリのパス
        """
        self.data_dir = data_dir
        self.data = None
    
    def load_from_csv(self, filename: str = "onsen_data.csv") -> pd.DataFrame:
        """
        CSVから温泉データを読み込む
        
        Args:
            filename: CSVファイル名
            
        Returns:
            読み込んだデータのDataFrame
        """
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"ファイルが見つかりません: {filepath}")
        
        df = pd.read_csv(filepath)
        self.data = df
        return df
    
    def load_from_json(self, filename: str = "onsen_data.json") -> List[Dict]:
        """
        JSONから温泉データを読み込む
        
        Args:
            filename: JSONファイル名
            
        Returns:
            読み込んだデータのリスト
        """
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"ファイルが見つかりません: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.data = pd.DataFrame(data)
        return data
    
    def get_dataframe(self) -> Optional[pd.DataFrame]:
        """
        読み込んだデータをDataFrame形式で取得
        
        Returns:
            データのDataFrame、データがない場合はNone
        """
        return self.data
    
    def filter_by_prefecture(self, prefecture: str) -> pd.DataFrame:
        """
        都道府県でデータをフィルタリング
        
        Args:
            prefecture: 都道府県名
            
        Returns:
            フィルタリングされたDataFrame
        """
        if self.data is None:
            raise ValueError("データが読み込まれていません")
        
        return self.data[self.data["都道府県"].str.contains(prefecture)]
    
    def get_location_data(self) -> pd.DataFrame:
        """
        マッピング用に位置情報のみを取得
        
        Returns:
            位置情報を含むDataFrame
        """
        if self.data is None:
            raise ValueError("データが読み込まれていません")
        
        # 緯度・経度がある行のみを抽出
        location_data = self.data.dropna(subset=["緯度", "経度"])
        
        return location_data
    
    def get_onsen_details(self, onsen_name: str) -> Optional[Dict]:
        """
        温泉名から詳細データを取得
        
        Args:
            onsen_name: 温泉名
            
        Returns:
            温泉の詳細データ辞書、見つからない場合はNone
        """
        if self.data is None:
            raise ValueError("データが読み込まれていません")
        
        filtered = self.data[self.data["名称"] == onsen_name]
        
        if len(filtered) == 0:
            return None
        
        return filtered.iloc[0].to_dict()
