import hebi
from time import sleep
import numpy as np
# HEBIモジュールを検索
lookup = hebi.Lookup()

Family = "X8-9"
Name = "X-81102"

# HEBIモジュールを検索
lookup = hebi.Lookup()
group = lookup.get_group_from_names([Family], [Name])


if group is None:
    print('Group not found!')
    exit(1)

# Start logging in the background
group.start_log('logs', mkdirs=True)


group_feedback = hebi.GroupFeedback(group.size)
group_command = hebi.GroupCommand(group.size)




while True:
    group.get_next_feedback(reuse_fbk=group_feedback)
    effort = -group_feedback.position*6
    
    #if group_feedback.position+1.15 < position_ran and group_feedback.position+1.15 > -position_ran  :
    effort[group_feedback.position > 0] *= 1
    effort[group_feedback.position < 0] *= 1
    
    group_command.effort = effort
    group.send_command(group_command)

# Stop logging. `log_file` contains the contents of the file
log_file = group.stop_log()

if log_file is not None:
    hebi.util.plot_logs(log_file, 'position', figure_spec=101)
    hebi.util.plot_logs(log_file, 'velocity', figure_spec=102)
    hebi.util.plot_logs(log_file, 'effort', figure_spec=103)