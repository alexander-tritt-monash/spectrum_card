import spectrum_card as sc

import time as tm
import numpy as np
import math

if __name__ == "__main__":
  do_sequence = True
  do_double = False

  signal_length = 512
  signal_sine = np.sin(math.tau*np.arange(0, signal_length)/signal_length)
  signal_square = np.sign(np.cos(math.tau*np.arange(0, signal_length)/signal_length))
  signal_bipolar = 1*(np.arange(0, signal_length) >= signal_length//4) - 1*(np.arange(0, signal_length) < 3*signal_length//4)
  signal_rectified = np.abs(np.cos((math.tau*np.arange(0, signal_length)/signal_length - math.pi/2)/2))

  card = sc.Card()
  card.reset()
  
  print("")
  print("Card identity:")
  print("Device name:", card.get_name())
  print("Serial number:", card.get_serial_number())
  print("Series:", card.get_series_information())
  print("Production date:", card.get_production_date_information())
  print("Calibration date:", card.get_calibration_date_information())
  print(f"Max sample rate: {card.get_max_sample_rate()/1e6} MHz")
  print(f"Memory: {card.get_max_memory_size()/(2**30)} GiB")
  print("Is demo:", card.get_is_demo_card() != 0)
  print("Modifications:", card.get_modifications_information())

  print("")
  print("Card information:")
  print("Front end modules:", card.get_number_of_front_end_modules())
  print("Channels per front end module:", card.get_number_of_channels_per_front_end_module())
  print(f"Resolution: {card.get_sample_resolution()} B = {card.get_sample_resolution_bits()} b")
  print("ADC scale:", card.get_adc_full_scale())
  print(f"External clock: {card.get_min_external_clock()/1e6} MHz to {card.get_max_external_clock()/1e6} MHz")
  print(f"External reference clock: {card.get_min_external_reference_clock()/1e6} MHz to {card.get_max_external_reference_clock()/1e6} MHz")

  print("")
  print("Temperature:")
  print(f"FPGA: {card.get_temperature_base()} degC")
  print(f"Amplifier: {card.get_temperature_module_1()} degC")

  print("")
  print("Driver information:")
  print("Driver:", card.get_driver_information())
  print("Version:", card.get_driver_version_information())
  print("Kernel version:", card.get_kernel_version_information())

  print("")
  print("Features and functions:")
  print("Features:", card.get_features_information())
  print("Functions:", card.get_functions_information())

  print("")
  print("Hardware versions:")
  print("PCI version:", card.get_pci_information())
  print("PCB version:", card.get_base_pcb_information())

  print("")
  print("Firmware versions:")
  print("Control FPGA:", card.get_firmware_version_control_information())
  print("Control FPGA golden:", card.get_firmware_version_control_golden_information())
  print("Control FPGA active:", card.get_firmware_version_control_active_information())
  print("Clock distribution:", card.get_firmware_version_clock_information())
  print("Configuration controller:", card.get_firmware_version_configuration_information())
  print("Front end module A:", card.get_firmware_version_module_a_information())
  print("Front end module B:", card.get_firmware_version_module_b_information())
  print("Star hub module:", card.get_firmware_version_module_star_information())
  print("Power controller:", card.get_firmware_version_power_information())

  print("")
  print("Clock information:")
  print("Available clock modes:", card.get_available_clock_modes())
  print("Clock mode:", card.get_clock_mode_information())
  print(f"Output frequency {card.get_clock_output_frequency()/1e6} MHz")
  print(f"External reference frequency {card.get_external_reference_frequency()/1e6} MHz")

  print("")
  print("Channels etc:")
  print(f"Sample rate: {card.get_sample_rate()/1e6} MHz")
  print("Resetting sample rate...")
  if card.get_series_information() in ["M4i", "M4i Express"]:
    card.set_sample_rate(50, "M")
  else:
    card.set_sample_rate(1, "M")
  print(f"Sample rate: {card.get_sample_rate()/1e6} MHz")
  print("Mode:", card.get_mode_information())
  print("Available modes:", card.get_available_modes_information())
  card.clock_output_disable()
  print("Enabled channels", card.get_channels_enable())

  print("")
  print("Triggers:")
  card.set_sufficient_triggers(software = True)
  card.set_channels_for_sufficient_triggers(channel_0 = True, channel_1 = True, channel_2 = True)
  print(f"Number of active channels: {card.get_number_of_active_channels()}")
  print(f"Sample resolution: {card.get_sample_resolution()} B")
  print("Available sufficient triggers:", card.get_available_sufficient_triggers())
  print("Sufficient triggers:", card.get_sufficient_triggers())
  print("Available channels for sufficient triggers:", card.get_available_channels_for_sufficient_triggers())
  print("Channels for sufficient triggers:", card.get_channels_for_sufficient_triggers())
  print("Available necessary triggers:", card.get_available_necessary_triggers())
  print("Necessary triggers:", card.get_necessary_triggers())
  print("Available channels for necessary triggers:", card.get_available_channels_for_necessary_triggers())
  print("Channels for necessary triggers:", card.get_channels_for_necessary_triggers())

  print("")
  print("Sequencing")
  print("Max number of segments:", card.get_max_number_of_segments())
  print("Max number of loops per step:", card.get_max_number_of_loops_per_sequence_step())
  print("Max number of steps:", card.get_max_number_of_sequence_steps())

  card.identification_led_enable()
  if do_sequence:
    print("")
    print("Sequence routine:")

    card.set_channels_enable(channel_0 = True, channel_1 = True, channel_2 = True, channel_3 = True)
    card.output_enable(0)
    card.set_amplitude(0, 500)
    card.output_enable(1)
    card.set_amplitude(1, 500)
    card.output_enable(2)
    card.set_amplitude(2, 500)
    card.output_enable(3)
    card.set_amplitude(3, 500)

    card.set_mode_sequence()
    card.set_number_of_segments(4)

    card.set_memory_size(card.get_number_of_segments()*signal_sine.size)

    card.set_segment_length(0, signal_length)
    card.array_to_device([signal_sine, signal_square, signal_bipolar, signal_rectified], 0)
    card.set_segment_length(1, signal_length)
    card.array_to_device([signal_rectified, signal_sine, signal_square, signal_bipolar], 1)
    card.set_segment_length(2, signal_length)
    card.array_to_device([signal_bipolar, signal_rectified, signal_sine, signal_square], 2)
    card.set_segment_length(3, signal_length)
    card.array_to_device([signal_square, signal_bipolar, signal_rectified, signal_sine], 3)

    number_of_loops = 100000
    card.set_step_instruction(step = 0, segment = 0, number_of_loops = number_of_loops)
    card.set_step_instruction(step = 1, segment = 1, number_of_loops = number_of_loops//2)
    card.set_step_instruction(step = 2, segment = 2, number_of_loops = number_of_loops*2)
    card.set_step_instruction(step = 3, segment = 3, number_of_loops = number_of_loops, next_step = 0)
    # card.set_step_instruction(step = 4, segment = 0, number_of_loops = number_of_loops)
    # card.set_step_instruction(step = 5, segment = 1, number_of_loops = number_of_loops//2)
    # card.set_step_instruction(step = 6, segment = 2, number_of_loops = number_of_loops*2)
    # card.set_step_instruction(step = 7, segment = 3, number_of_loops = number_of_loops)
    # card.set_step_instruction(step = 8, segment = 0, number_of_loops = number_of_loops)
    # card.set_step_instruction(step = 9, segment = 1, number_of_loops = number_of_loops//2)
    # card.set_step_instruction(step = 10, segment = 2, number_of_loops = number_of_loops*2)
    # card.set_step_instruction(step = 11, segment = 3, number_of_loops = number_of_loops, end_of_sequence = True)

    card.set_channel_stop_level(0, low = True)
    card.set_channel_stop_level(1, high = True)
    card.set_channel_stop_level(2, hold_last = True)
    card.set_channel_stop_level(3, custom_value = -0.5)

    print("Channel 0 stop level:", card.get_channel_stop_level(0))
    print("Channel 1 stop level:", card.get_channel_stop_level(1))
    print("Channel 2 stop level:", card.get_channel_stop_level(2))
    print("Channel 3 stop level:", card.get_channel_stop_level(3))

    card.set_start_step(0)
    
    print("Channel 0 enabled:", card.get_output_enable(0) == 1)
    print("Channel 1 enabled:", card.get_output_enable(1) == 1)
    print("Channel 2 enabled:", card.get_output_enable(2) == 1)
    print("Channel 3 enabled:", card.get_output_enable(3) == 1)

    # card.array_to_device([signal_sine, signal_square, signal_bipolar, signal_rectified], signal_sine.size)

    print("Status:", card.get_status_information())
    print("")
    card.execute_commands(start = True, enable_trigger = True, force_trigger = True)
    print("Started.")
    print("")
    tm.sleep(20)
    card.stop()
    print("Stopped.")
    print("")

  if do_double:
    print("")
    print("Double routine:")

    card.set_mode_single()
    card.set_number_of_loops(0)

    card.set_channels_enable(channel_0 = True, channel_2 = True)
    card.differential_enable(0)
    card.double_enable(2)

    card.output_enable(0)
    card.set_amplitude(0, 500)
    card.output_enable(1)
    card.set_amplitude(1, 500)
    card.output_enable(2)
    card.set_amplitude(2, 500)
    card.output_enable(3)
    card.set_amplitude(3, 500)

    card.set_memory_size(signal_sine.size)
    card.array_to_device([signal_rectified, signal_bipolar])

    card.execute_commands(start = True, enable_trigger = True, force_trigger = True)
    print("Started.")
    print("")
    tm.sleep(10)
    card.stop()
    print("Stopped.")
    print("")

  print("Status:", card.get_status_information())
  card.reset()
  card.close()