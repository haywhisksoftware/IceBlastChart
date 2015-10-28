def generate_grid():
  steps = lambda: xrange(1000, 2000, 100)
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

  for max_hp in steps():
    for level in level_indexes:
      total_damage = magic_resistance_multiplyer * (burst_damages[level] + dps_duration[level] * dps_damage[level])
      total_damage_scepter = magic_resistance_multiplyer * (burst_damages[level] + dps_duration_scepter[level] * dps_damage[level])
      hp_thresh = max_hp * shatter_thresholds[level]
      hp_no_scepter = hp_thresh + total_damage
      hp_with_scepter = hp_thresh + total_damage_scepter
      thresholds_no_scepter[level].append(hp_no_scepter)
      thresholds_with_scepter[level].append(hp_with_scepter)

  print thresholds_no_scepter
  print thresholds_with_scepter

def generate_html():
  pass

if __name__ == "__main__":
  generate_grid()
