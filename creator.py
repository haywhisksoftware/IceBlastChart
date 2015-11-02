def generate_grid(step_func):
  thresholds_no_scepter = [[], [], []]
  thresholds_with_scepter = [[], [], []]
  #for the shatter to take effect, the target hero needs to be lower than
  # 10/11/12% of their maximum HP. Ice Blast will deal xxx/yyy/zzz burst damage
  # and then a total of aaa/bbb/ccc (or ddd/eee/fff) damage-over-time
  shatter_thresholds = [0.10, 0.11, 0.12]
  burst_damages = [250, 350, 450]
  dps_duration = [8, 9, 10]
  dps_duration_scepter = [17, 17, 17]
  dps_damage = [12.5, 20, 32]
  level_indexes = [0, 1, 2]
  magic_resistance_multiplyer = 0.75 #25% magic damage reduction

  for max_hp in step_func():
    for level in level_indexes:
      total_damage = magic_resistance_multiplyer * (burst_damages[level] + dps_duration[level] * dps_damage[level])
      total_damage_scepter = magic_resistance_multiplyer * (burst_damages[level] + dps_duration_scepter[level] * dps_damage[level])
      hp_thresh = max_hp * shatter_thresholds[level]
      hp_no_scepter = hp_thresh + total_damage
      hp_with_scepter = hp_thresh + total_damage_scepter
      thresholds_no_scepter[level].append(hp_no_scepter)
      thresholds_with_scepter[level].append(hp_with_scepter)
  thresholds_no_scepter = zip(thresholds_no_scepter[0], thresholds_no_scepter[1], thresholds_no_scepter[2])
  thresholds_with_scepter = zip(thresholds_with_scepter[0], thresholds_with_scepter[1], thresholds_with_scepter[2])
  
  print thresholds_no_scepter
  print thresholds_with_scepter
  return thresholds_no_scepter, thresholds_with_scepter

def generate_html(without_scepter, with_scepter, step_func):
  format_string = "<tr><td>%(max_hp)d</td><td>%(l1hp)f</td><td>%(l2hp)f</td><td>%(l3hp)f</td></tr>"
  without_list = []
  with_list = []
  i = 0
  for step in step_func():
    this_step_with = with_scepter[i]
    this_step_without = without_scepter[i]
    without_dict = {'max_hp':step, 'l1hp':this_step_without[0], 'l2hp': this_step_without[1], 'l3hp': this_step_without[2]}
    with_dict = {'max_hp':step, 'l1hp':this_step_with[0], 'l2hp': this_step_with[1], 'l3hp': this_step_with[2]}
    
    without_string = format_string % without_dict
    with_string = format_string % with_dict
    
    without_list.append(without_string)
    with_list.append(with_string)
    i += 1
  
  return "\n".join(without_list), "\n".join(with_list)

def modify_html(without_scepter_rows, with_scepter_rows):
  without_scepter_line = "{{no_scepter}}"
  with_scepter_line = "{{with_scepter}}"
  with open("template.html", "r") as input_file:
    with open("index.html", "w") as output_file:
      for line in input_file:
        stripped_line = line.strip()
        if stripped_line == without_scepter_line:
          output_file.write(without_scepter_rows)
        elif stripped_line == with_scepter_line:
          output_file.write(with_scepter_rows)
        else:
          output_file.write(line)

if __name__ == "__main__":
  step_func = lambda: xrange(750, 4001, 250)
  thresholds_no_scepter, thresholds_with_scepter = generate_grid(step_func)


  without_string, with_string = generate_html(thresholds_no_scepter, thresholds_with_scepter, step_func)
  print without_string
  print with_string
  modify_html(without_string, with_string)
