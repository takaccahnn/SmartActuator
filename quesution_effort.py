import hebi
# HEBI RoboticsのPython APIをインポートします
from time import sleep
# sleep関数をインポートします
'''
APIの接続がなされているか確認します。もしせつぞくされていない場合はそこでプログラム
を終了します。
'''
lookup = hebi.Lookup()
 # ネットワーク上のHEBIモジュールを検索するためのLookupオブジェクトを作成します
sleep(2)
 # モジュールがネットワークに登録されるのを待つために2秒間スリープします
group = lookup.get_group_from_names(["X8-9"], ["X-81102"])
# 特定のファミリ名と名前を持つモジュールからなるグループを取得します
command = hebi.GroupCommand(group.size) 
# グループのサイズに基づいてGroupCommandオブジェクトを作成します
# GroupCommandオブジェクトはposition, velocity, effortに対して命令を出すことができる
feedback = hebi.GroupFeedback(group.size)
# グループのサイズに基づいてGroupFeedbackオブジェクトを作成します
# GroupFeedbackオブジェクトはposition, velocity, effortの値を読み取ることができる

if group is None:
# グループが見つからない場合、エラーメッセージを表示してプログラムを終了します
  print('モジュールが見つかりません')
  exit(1)
else:
  print('モジュールは見つかりました')

for i in range(5):
  if group.get_next_feedback(reuse_fbk=feedback) is not None:
    print('Motor effort: ', feedback.effort)
    # get_next_feedbackはモジュールから最新のフィードバックを取得する
    # フィードバックが利用可能な場合、モーターの現在位置（回転値）が表示されます
  else:
    print("次の信号が得られませんでした")
    exit(1)  
#  command.effort = [10.0] 
  for i in range(1): command.effort[i] += 5.0
  group.send_command(command)
  sleep(0.3)
