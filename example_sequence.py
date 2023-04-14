import spectrum_card as sc

import time as tm
import numpy as np
import math

use_trigger = False # Do you want to use the hardware triggers, or force the trigger with software?
wait_time = 10      # How long before the stop command is sent

# Create signals to load onto card
signal_length = 512
signal_sine = np.sin(math.tau*np.arange(0, signal_length)/signal_length)
signal_square = np.sign(np.cos(math.tau*np.arange(0, signal_length)/signal_length))
signal_bipolar = 1*(np.arange(0, signal_length) >= signal_length//4) - 1*(np.arange(0, signal_length) < 3*signal_length//4)
signal_rectified = np.abs(np.cos((math.tau*np.arange(0, signal_length)/signal_length - math.pi/2)/2))
signal_aux = signal_sine >= 0

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

# Channel enable
card.set_channels_enable(channel_0 = True, channel_1 = True, channel_2 = True, channel_3 = True)
card.output_enable(0)
card.set_amplitude(0, 0.5)
card.output_enable(1)
card.set_amplitude(1, 0.5)
card.output_enable(2)
card.set_amplitude(2, 0.5)
card.output_enable(3)
card.set_amplitude(3, 0.5)

# Sequence setup
card.use_mode_sequence()
card.set_number_of_segments(4)
card.set_memory_size(card.get_number_of_segments()*signal_sine.size)

# Digital output setup
aux_data_channels = [{"Channel" : 1, "Bit" : 13, "Port": 2}]

# Transfer signals for each segment
card.array_to_device(
  [signal_sine, signal_square, signal_bipolar, signal_rectified],
  0,
  aux_data = [signal_aux],
  aux_data_channels = aux_data_channels
)
card.array_to_device(
  [signal_rectified, signal_sine, signal_square, signal_bipolar],
  1,
  aux_data = [signal_aux],
  aux_data_channels = aux_data_channels
)
card.array_to_device(
  [signal_bipolar, signal_rectified, signal_sine, signal_square],
  2,
  aux_data = [signal_aux],
  aux_data_channels = aux_data_channels
)
card.array_to_device(
  [signal_square, signal_bipolar, signal_rectified, signal_sine],
  3,
  aux_data = [signal_aux],
  aux_data_channels = aux_data_channels
)

# Add sequencer step instructions
number_of_loops = 100000
card.set_step_instruction(0, 0, number_of_loops)
card.set_step_instruction(1, 1, number_of_loops//2)
card.set_step_instruction(2, 2, number_of_loops*2)
card.set_step_instruction(3, 3, number_of_loops, next_step = 0)
card.set_start_step(0)

# Arm the card for triggering
card.arm()
if not use_trigger:
  card.force_trigger()

# Wait for some time and stop the card
tm.sleep(wait_time)
card.stop()
card.close()