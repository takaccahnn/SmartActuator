import hebi 
# HEBI RoboticsのPython APIをインポートします
from time import sleep 
# sleep関数をインポートします

'''''
APIの接続がなされているか確認します。もしせつぞくされていない場合はそこでプログラム
を終了します。
'''''
'''
lookup = hebi.Lookup()
 # ネットワーク上のHEBIモジュールを検索するためのLookupオブジェクトを作成します
sleep(2)
 # モジュールがネットワークに登録されるのを待つために2秒間スリープします

group = lookup.get_group_from_names(["X8-9"], ["X-81102"]) 
# 特定のファミリ名と名前を持つモジュールからなるグループを取得します

if group is None: 
# グループが見つからない場合、エラーメッセージを表示してプログラムを終了します
  print("モジュールが見つかりません")
  exit(1)
'''
'''
ここに回転数を入力としてeffect(粘性)を出力するプログラム書きます。
内部の関数としては、回転数が大きければ大きいほど粘性が大きくなり、
回転数が小さければ小さいほど粘性が小さくなるようなあるとリズムを生成したい。
そうすることで、ハンドルが中央に自然と戻りやすくなるようにしたい。
'''
'''
command = hebi.GroupCommand(group.size) 
# グループのサイズに基づいてGroupCommandオブジェクトを作成します

command.velocity = [1.0] 
# 回転数（rad/sec）を設定します。ここでは1.0 rad/secに設定しています
'''