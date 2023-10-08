# 入退場管理システム(TicketSystem)
<img src="https://repository-images.githubusercontent.com/702109092/0e80e24e-792b-44af-8815-0568e4ba3f90">  

## 目次

1. [概要](#概要)
2. [環境ファイル設定](#環境ファイル設定)
3. [モードの種類](#モードの種類)
4. [OSSについて](#OSSについて)
---

## 概要

### 入退場管理システム(TicketSystem)とはなにか

入退場管理システム（以下、当システム）は、高度なテクノロジーを活用して、ユーザーの生活を向上させるために設計された革新的なソリューションです。

このシステムはPythonとHTML、JavaScriptなどのプログラミング言語とWebテクノロジーを組み合わせて構築されており、多くの利点を提供します。

また、当システムは他のプログラミング言語と幅広い互換性を持っており、ユーザーのニーズに的確に対応することが可能です。

### 利用注意

このシステムは、柔軟性を持たせるためにセキュリティに関するプログラムが限定的な設計となっています。そのため、重要な個人情報を入力しないようにしてください。

セキュリティに関するプログラムが限定的であるため、他のプログラムに実装する場合はセキュリティ機構を実装してください。

---

## 環境ファイル設定

### デフォルト値

`settings.json`は、当システムの設定ファイルで、システムの動作をカスタマイズするために使用されます。  
この設定ファイルを変更することで、システムが異なる環境で正常に動作するように調整できます。

```json
{
  "Ticket_Name": "TEST-TICKET",
  "db_path": "db.db",
  "input_form_msg": "チケット発行システム",
  "max_ppl": 5,
  "no_name": "名無し",
  "no_ppl": 1,
  "qr_file_path": "qr",
  "qr_msg": "QRコードをかざしてください"
}
```

### keyの説明

環境ファイルの各設定項目の詳細な説明を提供します。 これらの設定項目は異なるデータ型（str型やint型など）を持っており、
システムの様々な側面をカスタマイズするために使用されます。  
これらの設定項目は、システムのカスタマイズや運用に関する重要な情報を含んでいます。  
異なるデータ型の混在に注意しながら、環境ファイルを適切に設定および管理することが大切です。

| 設定項目           | デフォルトの値        | 説明                  |
|----------------|----------------|---------------------|
| Ticket_Name    | TEST-TICKET    | チケットの名前             |
| db_path        | db.db          | データベースファイルのパス       |
| input_form_msg | チケット発行システム     | 入力フォームのメッセージ        |
| max_ppl        | 5              | 最大登録人数              |
| no_name        | 名無し            | 名前未入力時のデフォルト名       |
| no_ppl         | 1              | 人数未入力時のデフォルト値       |
| qr_file_path   | qr             | QRコードファイルの保存先ディレクトリ |
| qr_msg         | QRコードをかざしてください | QRコード表示時のメッセージ      |

---

## モードの種類

モードの選択では`入場中` `一時退場中` `退場済み`の3つから選択できます。  
これが、ステータスの値となります。  
　また、QRコード読み込みページにて数字キーボードの1~3は以下のように割り当てられています。  

これらのモード選択と数字キーボードの対応により、ユーザーは簡単かつ迅速に自身の入退場状態を更新できます。  
システムの操作は直感的でわかりやすく、ユーザーの利便性を向上させることができます。

| モード     | 割当key |
|---------|-------|
| 入場モード   | 1     |
| 一時退場モード | 2     |
| 退場モード   | 3     |

---
## OSSについて
### 実行確認環境
Max OS 14.0 Sonoma  
Python 3.11
### LICENCE
このプロジェクトにはMIT LICENCEを使用しています。
詳細は[LICENCE](https://github.com/MT472562/TicketSystem/blob/main/LICENSE)をご確認ください
### 問い合わせ
なにか不明点などがございましたら、[issues](https://github.com/MT472562/TicketSystem/issues)
または、[X(旧Twitter)](https://twitter.com/magirawashili)までお問い合わせください。  


最後に  
ここまで読んでいただいた方ありがとうございます。  
思いつきで適当に始めちゃったプロジェクトなのでコードはぐちゃぐちゃですし、ホンマに見にくいと思うので堪忍してください  
皆様の今後の発展をお祈り申し上げます。




