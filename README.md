## Nexkey Spam Killer

### 注意
 - 必ずスパムに関係のない通報を全て処理してから使ってください。
 - かなり応急処置的なハイリスクで汚いやり方なので公開インスタンスでやるときは気をつけてください。

### 使い方
 1. main.pyのCHANGEMEの部分を変更して適切なトークンとホストを設定します。
 2. 実行すると通報されたユーザーのホストに対して以下の処理を行うか対象のホストごとに聞かれます。必ずFFが0または無視できる範囲であることを確認してください。
    - インスタンスへの配送停止とブロック
    - 該当インスタンスのデータの削除
 3. 全ての通報を処理すると`No unresolved abuse user reports`というメッセージが出ます。これで完了です。
