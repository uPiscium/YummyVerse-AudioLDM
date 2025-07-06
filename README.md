# YummyVerse-AudioLDM 実行環境

## 概要
YummyVerse-AudioLDMは, YummyVerseプロジェクトの一部であり, 音声データを用いたLDM（Latent Diffusion Model）を実行するための環境です. このREADMEでは, 使用方法について説明します.

## 必要な環境
- uv: Pythonの仮想環境管理ツールである`uv`を使用します.

## 起動方法
```bash
uv sync # 初回のみ実行してください
uv run src/entry.py
```
初回起動は環境構築とモデルのダウンロードが必要なため, 時間がかかる場合があります. その後は, `uv run src/entry.py` で起動できます.

## 使用方法
FastAPIを使用しており, サーバが起動すると, 以下のURLでAPIのドキュメントにアクセスできます:\

### `http://localhost:8000/docs`

APIを通じて音声データの生成やダウンロードを行うことができます. 詳細なAPIの使用方法は, ドキュメントを参照してください.
