import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
import zipfile
import shutil
import concurrent.futures

# NinaPro のベース URL
BASE_URL_PREFIX = "https://ninapro.hevs.ch/instructions/"

# ダウンロード先のベースフォルダ
BASE_SAVE_DIR = Path.home() / "Desktop" / "NinaPro_Zips"

# DB1〜DB10を順番に処理
for db_index in range(1, 11):
    db_name = f"DB{db_index}"
    page_url = f"{BASE_URL_PREFIX}{db_name}.html"
    print(f"\n📄 {db_name} を処理中: {page_url}")

    db_dir = BASE_SAVE_DIR / db_name
    os.makedirs(db_dir, exist_ok=True)

    try:
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        zip_links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href']
            if href.endswith(".zip"):
                full_url = urljoin(page_url, href)
                zip_links.append(full_url)

        print(f"  🔗 {len(zip_links)} 個のZIPファイルが見つかりました。")

        # 並列でのZIPダウンロード関数
        def download_and_extract_zip(link):
            filename = os.path.basename(link)
            zip_path = db_dir / filename
            extract_dir = db_dir / filename.replace(".zip", "")

            try:
                print(f"    ⬇️ ダウンロード中: {filename}")
                with requests.get(link, stream=True) as r:
                    r.raise_for_status()
                    with open(zip_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"    ✅ ダウンロード完了: {zip_path}")

                print(f"    📦 解凍中...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                print(f"    📁 解凍完了: {extract_dir}")

            except Exception as e:
                print(f"    ❌ ダウンロード/解凍失敗: {link} エラー: {e}")

        # スレッドプールで並列実行
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.map(download_and_extract_zip, zip_links)

        # 以下は.mat統合処理はそのまま
        all_mat_dir = db_dir / "all_mat"
        os.makedirs(all_mat_dir, exist_ok=True)
        mat_count = 0

        for folder in db_dir.iterdir():
            if folder.is_dir() and folder.name.lower().startswith("s"):
                for file in folder.glob("*.mat"):
                    dest_file = all_mat_dir / file.name
                    try:
                        shutil.copy(file, dest_file)
                        mat_count += 1
                    except Exception as e:
                        print(f"    ⚠️ コピー失敗: {file} → {dest_file} エラー: {e}")

        print(f"  ✅ {mat_count} 個の .mat ファイルを {all_mat_dir} に統合しました。")

    except Exception as e:
        print(f"  ⚠️ ページ取得失敗: {page_url} エラー: {e}")
