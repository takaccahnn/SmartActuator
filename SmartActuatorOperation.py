import hebi 
# HEBI RoboticsのPython APIをインポートします
from time import sleep 
# sleep関数をインポートします


'''''
APIの接続がなされているか確認します。もしせつぞくされていない場合はそこでプログラム
を終了します。
'''''
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
else:
  print("モジュールは見つかりました")
  exit(0)
'''

'''
ここに回転数を入力としてeffect(粘性)を出力するプログラム書きます。
内部の関数としては、回転数が大きければ大きいほど粘性が大きくなり、
回転数が小さければ小さいほど粘性が小さくなるようなあるとリズムを生成したい。
そうすることで、ハンドルが中央に自然と戻りやすくなるようにしたい。
[注意すること]
○フィードバック制御をする時に、group.send_command(command)を実行するまである程度の時間が必要、
sleep()関数でその時間を稼いでやらないとスマートアクチュエーターが出す命令よりも先にプログラムが走ってしまう
sleep(0.2)もしくはsleep(0.25)あたりがinfな気がする
(if(group.send_command(command):continueでも先にプログラムが走ってしまった)
○effort変数についての中身だが、effortの値を-1にするようなプログラムを作成すると、値が-1で一定にならずに-1付近でずっと変化した
effort変数はアクチュエーターに作用する力もしくはトルクを表している

'''
command = hebi.GroupCommand(group.size) 
# グループのサイズに基づいてGroupCommandオブジェクトを作成します
# GroupCommandオブジェクトはposition, velocity, effortに対して命令を出すことができる
feedback = hebi.GroupFeedback(group.size)
# グループのサイズに基づいてGroupFeedbackオブジェクトを作成します
# GroupFeedbackオブジェクトはposition, velocity, effortの値を読み取ることができる
'''
command.position = [10] 
# 回転数（rad/sec）を設定します。ここでは1.0 rad/secに設定しています
# GroupFeedbackオブジェクトはposition, velocity, effortの値を受け取り、その値を配列に格納する
'''
init_position = feedback.position
# この時点ではまだfeedbackオブジェクトにスマートアクチュエータの初期値の値が入っていないため、0が返される
# 下にあるgroup.get_next_feedbackメソットを用いることで初めて須磨ートアクチュエーターの初期値が入る
# スマートアクチュエータの値を知りたければgroup.get_next_feedbackメソットを前に走らせること
init_effect = [0.0]
# 位置及び粘性の初期値の設定
effect_max = [20.0]
effect_min = [-20.0]
# 粘性の境界値
print("Motor position init", init_position)
test = 0
command.position = [3.0]
group.send_command(command)
while True:
  if group.get_next_feedback(reuse_fbk=feedback) is not None:
    print('Motor position: ', feedback.position)
    # get_next_feedbackはモジュールから最新のフィードバックを取得する
    # フィードバックが利用可能な場合、モーターの現在位置（回転値）が表示されます
  else:
    print("次の信号が得られませんでした")
    exit(1)
  if(test==0): before_position = [0]
  # 一個前の位置を表す
  now_position = feedback.position
  # 現在の位置
  print("今と過去を引いた差: ", now_position[0]-before_position[0])
  while(True):
    if(now_position[0] >= 1.0 and (now_position[0] - before_position[0])>=0):
      command.effort = feedback.effort + [effect_min[0]]
      group.send_command(command)
      print("Motor effort command1", command.effort)
      break
    if(now_position[0] >= 1.0 and (now_position[0] - before_position[0])<0):
      command.effort = feedback.effort + [effect_min[0]]
      group.send_command(command)
      print("Motor effort command2", command.effort)
      break
    if(now_position[0] < 1.0 and now_position[0] >= 0.0 and (now_position[0] - before_position[0])>=0):
      command.effort = feedback.effort + [10.0]
      group.send_command(command)
      print("Motor effort command3", command.effort)
      break
    if(now_position[0] < 1.0 and now_position[0] >= 0.0 and (now_position[0] - before_position[0])<0):
      command.effort = feedback.effort + [-10.0]
      group.send_command(command)
      print("Motor effort command4", command.effort)
      break
    if(now_position[0] < 0.0 and now_position[0] > -1.0 and (now_position[0] - before_position[0])>=0):
      command.effort = feedback.effort + [10.0]
      group.send_command(command)
      print("Motor effort command5", command.effort)
      break
    if(now_position[0] < 0.0 and now_position[0] > -1.0 and (now_position[0] - before_position[0])<0):
      command.effort = feedback.effort + [-10.0]
      group.send_command(command)
      print("Motor effort command6", command.effort)
      break
    if(now_position[0] <= -1.0 and (now_position[0] - before_position[0])<=0):
      command.effort = feedback.effort + [effect_max[0]]
      group.send_command(command)
      print("Motor effort command7", command.effort)
      break
    if(now_position[0] <= -1.0 and (now_position[0] - before_position[0])>0):
      command.effort = feedback.effort + [effect_max[0]]
      group.send_command(command)
      print("Motor effort command8", command.effort)
      break
  if group.get_next_feedback(reuse_fbk=feedback) is not None:
    before_position = feedback.position
  test+=1
  print(" ")
  sleep(0.50)

  # コマンド送信後、モーターが動く時間を確保
