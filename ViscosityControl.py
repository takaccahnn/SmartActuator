import matplotlib
import hebi
# HEBI RoboticsのPython APIをインポートします
import time
# sleep関数をインポートします

lookup = hebi.Lookup()
 # ネットワーク上のHEBIモジュールを検索するためのLookupオブジェクトを作成します
time.sleep(2)
 # モジュールがネットワークに登録されるのを待つために2秒間スリープします

group = lookup.get_group_from_names(["X8-9"], ["X-81102"]) 
# 特定のファミリ名と名前を持つモジュールからなるグループを取得します

if group is None: 
# グループが見つからない場合、エラーメッセージを表示してプログラムを終了します
  print("モジュールが見つかりません")
  exit(1)


# 初期設定
command = hebi.GroupCommand(group.size)
feedback = hebi.GroupFeedback(group.size)

# 粘性の係数を設定
viscosity = [1.0]
print("Viscosity set to", viscosity)
past_velocity = [0.0]

# 粘性の値を制御するプログラム
while True:
    if group.get_next_feedback(reuse_fbk=feedback) is None:
       print("通信が途中で切れました")
       break
    now_velocity = feedback.velocity
    effort = feedback.effort
    dif = (now_velocity - past_velocity) * 1000
    # command.effort = (effort - viscosity*dif) * (1.0)
    command.position = 0.0
    # print("velocity:", now_velocity, "command:", dif)
    print("now_velocity:", now_velocity, "past_velocity:", past_velocity)
    group.send_command(command)
    past_velocity = now_velocity
    # time.sleep(0.5)

# effortはトルクの現在の値を表している。従って、effortに渡すのは現在の速度の値になる、減少増加分ではなく。