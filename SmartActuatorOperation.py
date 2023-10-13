import hebi 
# HEBI RoboticsのPython APIをインポートします
from time import sleep 
# sleep関数をインポートします


lookup = hebi.Lookup()
 # ネットワーク上のHEBIモジュールを検索するためのLookupオブジェクトを作成します
sleep(2)
 # モジュールがネットワークに登録されるのを待つために2秒間スリープします

group = lookup.get_group_from_names(["Family"], ["Name"]) 
# 特定のファミリ名と名前を持つモジュールからなるグループを取得します

if group is None: 
# グループが見つからない場合、エラーメッセージを表示してプログラムを終了します
  print("モジュールが見つかりません")
  exit(1)

command = hebi.GroupCommand(group.size) 
# グループのサイズに基づいてGroupCommandオブジェクトを作成します

command.velocity = [1.0] 
# 回転数（rad/sec）を設定します。ここでは1.0 rad/secに設定しています