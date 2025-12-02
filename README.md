# St.E.P. Web

## 📌 概要

St.E.P. Web (Starlight Echoes Portal Web) とは、Starlight☆Echoes運営に向け開発された**スタッフ用ポータルサイト**です。出演者情報の管理、タイムテーブル確認、運営連絡など、当日の業務をスムーズに進めるための機能をまとめています。

フロント〜バックエンドを **Django** を用いて構築し、**nginx + Gunicorn** による本番環境サーバー構成を **Docker** 上にコンテナ化しています。最終的なデプロイ環境は **AWS EC2** です。

本 README は **サイトを利用するスタッフ** と **今後の開発を引き継ぐエンジニア** の両方を対象としています。

---

## 🧑‍💼 スタッフ向け：基本の使い方

### 1. アカウント作成・ログイン

1. トップページ右上のメニューバーから、新規登録を行ってください。
2. 登録後、システム管理者にアカウント作成の旨を通告してください。
3. システム管理者から権限について通知されるので、確認してください。
4. トップページ右上のメニューバーから、ログインしてください。

### 2. 主な機能

#### ✔ 出演団体情報の表示

* 出演団体情報の概要表示（非スタッフ向け）
* 出演団体情報の詳細表示（スタッフ専用）

#### ✔ 進行状況の表示

* ステージにおけるステータスバーの表示
* 受付、控室等のスケジュール表示

#### ✔ 出演団体情報の入力・修正

* 初期登録
* 情報修正
* 実際の出演時刻等の打刻

#### ✔ スピークス

* 全ユーザー、またはスタッフ向けのアナウンス作成と表示
* 運営上の報告事項やスタッフのつぶやきのレコード作成

### 3. 推奨環境

* PC / タブレット / スマートフォン対応
* 未SSL化サイトを閲覧できるクライアント必須

---

## 👨‍💻 開発者向け：技術構成

### 🧩 バージョン情報

* **Python**: 3.7.3
* **Django**: 3.2.25
* **HTML / JavaScript**
* **Bootstrap**: 5.3.3（CDN）
* **開発DB**: SQLite3
* **本番DB**: PostgreSQL 15
* **Docker**: 28.5.1
* **nginx**: 1.25-alpine
* **Gunicorn**:（バージョンは `pip freeze` に依存）

### 🏗 技術スタック

* **Backend**: Django
* **WSGI サーバー**: Gunicorn
* **Web サーバー**: nginx
* **コンテナ管理**: Docker / Docker Compose
* **デプロイ環境**: AWS EC2 (Amazon Linux / Ubuntu)

### 📁 ディレクトリ構成（抜粋）

```
epp_project
├── accounts                  # アカウントに関するアプリ
├── epp_project               # プロジェクトディレクトリ
│   └── formats               # 自作の日付フォーマット
├── media
│   └── website_app
│        ├── art_pictures     # アー写ディレクトリ
│        ├── form_files       # フォームディレクトリ
│        └── stage_files      # ステージ情報ディレクトリ
├── nginx                     # nginxに関するディレクトリ
├── report                    # スピークスアプリ
├── static
├── staticfiles
├── status                    # ステータスアプリ
├── templates
│   ├── accounts
│   ├── base
│   ├── echoes
│   ├── report
│   ├── status
│   └── 403.html
├── website_app               # メインアプリ
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── requirements.txt
```

### 🐳 Docker 実行方法

```
docker-compose build
docker-compose up -d
```

### 🌐 nginx / Gunicorn 構成（概要）

* nginx が 80 番ポートで待受
* `/static/` `/media/` を nginx から直接配信
* アプリケーションは `gunicorn app.wsgi:application` を介して提供

### 🚀 デプロイの流れ

1. GitHub に push
2. EC2へSSH接続
3. pull して docker-compose を再起動

```
git pull
sudo docker-compose down
sudo docker-compose up -d --build
```

---

## 🧪 開発環境の設定

### 1. 仮想環境の作成（Dockerを使わない場合）

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Django 起動

```
python manage.py runserver
```

---

## 🔒 環境変数

以下の環境変数を `.env` に設定してください。

```
DJANGO_SECRET_KEY=xxxx
POSTGRES_DB=xxxx
POSTGRES_USER=xxxx
POSTGRES_PASSWORD=xxxx
```

---

## ✨ 今後の開発者へのメモ

* 管理者画面から権限管理が可能
* 本番環境は nginx 経由のため、静的ファイルは必ず `collectstatic` が必要
* 追加ステージへの対応や、出演者のインポート機能など拡張性あり

---

## 📝 ライセンス

本プロジェクトは社内専用として扱われます。外部公開は禁止されています。

---

## 📞 問い合わせ

開発・運営担当までお問い合わせください。
