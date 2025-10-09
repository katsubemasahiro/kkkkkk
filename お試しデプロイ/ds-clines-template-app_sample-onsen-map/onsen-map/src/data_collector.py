"""
日本の100名泉データを収集するスクリプト
"""
import csv
import json
import os
import time
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
import geocoder

class OnsenDataCollector:
    """温泉データ収集クラス"""
    
    def __init__(self, output_dir: str = "../data"):
        """
        初期化
        
        Args:
            output_dir: 出力ディレクトリパス
        """
        self.output_dir = output_dir
        self.ensure_output_dir()
        
    def ensure_output_dir(self) -> None:
        """出力ディレクトリが存在することを確認"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def collect_from_wikipedia(self) -> List[Dict]:
        """
        Wikipediaから日本の温泉地一覧を取得
        
        Returns:
            温泉情報のリスト
        """
        print("Wikipediaからデータを収集中...")
        url = "https://ja.wikipedia.org/wiki/日本の温泉地一覧"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        onsen_list = []
        
        # デバッグ: HTML構造を確認
        print(f"ページタイトル: {soup.title.text}")
        print(f"見出し数: {len(soup.find_all('h2'))}")
        
        # 都道府県ごとの表を取得
        prefecture_sections = soup.find_all("span", class_="mw-headline")
        print(f"見つかったmw-headlineクラスのspan要素: {len(prefecture_sections)}")
        
        for section in prefecture_sections:
            prefecture_name = section.text.strip()
            print(f"セクション名: {prefecture_name}")
            
            # 都道府県名のみを対象とする (「脚注」などは除外)
            if not prefecture_name.endswith("県") and not prefecture_name.endswith("都") and \
               not prefecture_name.endswith("府") and not prefecture_name.endswith("道"):
                print(f"  スキップ: 都道府県名ではない")
                continue
            
            # その都道府県の表を取得
            table = section.find_next("table")
            if not table:
                print(f"  {prefecture_name}の表が見つかりません")
                continue
            
            print(f"  {prefecture_name}の表を発見: {len(table.find_all('tr'))}行")
            
            rows = table.find_all("tr")
            # ヘッダー行をスキップ
            for row in rows[1:]:
                cells = row.find_all("td")
                if len(cells) >= 2:
                    onsen_name = cells[0].text.strip()
                    location = cells[1].text.strip() if len(cells) > 1 else ""
                    
                    onsen_info = {
                        "名称": onsen_name,
                        "都道府県": prefecture_name,
                        "所在地": location,
                        "出典": "Wikipedia"
                    }
                    onsen_list.append(onsen_info)
        
        print(f"Wikipediaから{len(onsen_list)}件の温泉データを収集しました")
        return onsen_list
    
    def get_coordinates(self, location: str, prefecture: str) -> Tuple[Optional[float], Optional[float]]:
        """
        住所から緯度・経度を取得
        
        Args:
            location: 住所
            prefecture: 都道府県
        
        Returns:
            (緯度, 経度)のタプル、取得できない場合はNone
        """
        search_query = f"{prefecture} {location}"
        g = geocoder.osm(search_query)
        
        if g.ok:
            return g.lat, g.lng
        
        # 検索結果が見つからない場合は少し待ってから再試行
        time.sleep(1)
        search_query = location  # 都道府県名を除いて再試行
        g = geocoder.osm(search_query)
        
        if g.ok:
            return g.lat, g.lng
        
        return None, None
    
    def add_coordinates_to_data(self, onsen_list: List[Dict]) -> List[Dict]:
        """
        温泉データに位置情報を追加
        
        Args:
            onsen_list: 温泉情報のリスト
        
        Returns:
            位置情報を追加した温泉情報のリスト
        """
        print("位置情報を取得中...")
        updated_list = []
        
        for i, onsen in enumerate(onsen_list):
            location = onsen.get("所在地", "")
            prefecture = onsen.get("都道府県", "")
            
            # API制限を避けるため一時停止
            if i > 0 and i % 5 == 0:
                print(f"{i}/{len(onsen_list)}件処理済み...")
                time.sleep(1)
            
            lat, lng = self.get_coordinates(location, prefecture)
            onsen["緯度"] = lat
            onsen["経度"] = lng
            
            updated_list.append(onsen)
        
        print(f"位置情報の取得が完了しました。{len(updated_list)}件の温泉データに位置情報を追加しました。")
        return updated_list
    
    def save_to_csv(self, onsen_list: List[Dict], filename: str = "onsen_data.csv") -> None:
        """
        温泉データをCSVファイルに保存
        
        Args:
            onsen_list: 温泉情報のリスト
            filename: 出力ファイル名
        """
        filepath = os.path.join(self.output_dir, filename)
        
        if not onsen_list:
            print("保存するデータがありません")
            return
            
        fieldnames = onsen_list[0].keys()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(onsen_list)
            
        print(f"データを {filepath} に保存しました")
    
    def save_to_json(self, onsen_list: List[Dict], filename: str = "onsen_data.json") -> None:
        """
        温泉データをJSONファイルに保存
        
        Args:
            onsen_list: 温泉情報のリスト
            filename: 出力ファイル名
        """
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(onsen_list, jsonfile, ensure_ascii=False, indent=4)
            
        print(f"データを {filepath} に保存しました")
    
    def run_collection(self) -> List[Dict]:
        """
        データ収集プロセス全体を実行
        
        Returns:
            収集した温泉データのリスト
        """
        # Wikipediaからデータを収集
        onsen_data = self.collect_from_wikipedia()
        
        # 位置情報を追加
        onsen_data = self.add_coordinates_to_data(onsen_data)
        
        # データを保存
        self.save_to_csv(onsen_data)
        self.save_to_json(onsen_data)
        
        return onsen_data

if __name__ == "__main__":
    collector = OnsenDataCollector()
    collector.run_collection()
