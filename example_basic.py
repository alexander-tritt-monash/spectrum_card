import spectrum_card as sc

import time as tm
import numpy as np
import math

use_trigger = False # Do you want to use the hardware triggers, or force the trigger with software?
wait_time = 10      # How long before the stop command is sent

# Create signal to load onto card
signal_length = 512
signal_sine = np.sin(math.tau*np.arange(0, signal_length)/signal_length)

# Create card
card = sc.Card()
card.reset()

# Card setup
if card.get_series_information() in ["M4i", "M4i Express"]:
  card.set_sample_rate(50, "M")
else:
  card.set_sample_rate(1, "M")
card.clock_output_disable()

# Trigger setup
if use_trigger:
  card.trigger_coupling_use_dc(0)
  card.use_trigger_positive_edge(0, 2.5, re_arm_threshold = 1)

# Enable one channel
card.set_channels_enable(channel_0 = True)
card.output_enable(0)
card.set_amplitude(0, 0.5)

# Send signal to card memory
card.set_memory_size(signal_sine.size)
card.array_to_device([signal_sine])

# Arm card for triggering, and (possibly) trigger by software
card.arm()
if not use_trigger:
  card.force_trigger()

# After some time, stop the card
tm.sleep(wait_time)
card.stop()
card.close()