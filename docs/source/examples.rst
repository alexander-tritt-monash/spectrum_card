Examples
========

Basic example
-------------

This example generates a sine wave.
The following code can be found in :obj:`example_basic.py`.

.. code-block:: python

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

Verbose example
---------------

This example reads pretty much every possible parameter on the card.
The following code can be found in :obj:`example_verbose.py`.

.. code-block:: python

  import spectrum_card as sc

  # Create card
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
  print(f"Sample rate: {card.get_sample_rate()/1e6} M samples/s")
  print("Mode:", card.get_mode_information())
  print("Available modes:", card.get_available_modes_information())
  print("Enabled channels", card.get_channels_enable())

  print("")
  print("Triggers:")
  print(f"Trigger delay: {card.get_trigger_delay()} Sa")
  print(f"Maximum trigger delay: {card.get_max_trigger_delay()} Sa")
  print("Trigger impedance:", card.get_trigger_impedance())
  print("Trigger couplings:", card.get_trigger_coupling(0), ",", card.get_trigger_coupling(1))
  print("Available trigger modes (Trigger 0):", card.get_available_trigger_modes_information(0))
  print("Available trigger modes (Trigger 1):", card.get_available_trigger_modes_information(1))
  print("Trigger modes:", card.get_trigger_mode_information(0), ",", card.get_trigger_mode_information(1))
  print(f"Lower trigger thresholds from {card.get_lower_trigger_threshold_min()} V to {card.get_lower_trigger_threshold_max()} V in steps of {card.get_lower_trigger_threshold_step()} V")
  print(f"Upper trigger thresholds from {card.get_upper_trigger_threshold_min()} V to {card.get_upper_trigger_threshold_max()} V in steps of {card.get_upper_trigger_threshold_step()} V")
  print(f"Trigger 0 lower: {card.get_lower_trigger_threshold(0):.2f} V, upper: {card.get_upper_trigger_threshold(0):.2f} V.")
  print(f"Trigger 1 lower: {card.get_lower_trigger_threshold(1):.2f} V, upper: {card.get_upper_trigger_threshold(1):.2f} V.")

  print("")
  print("Trigger masks:")
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
  print("Sequencing:")
  print("Max number of segments:", card.get_max_number_of_segments())
  print("Max number of loops per step:", card.get_max_number_of_loops_per_sequence_step())
  print("Max number of steps:", card.get_max_number_of_sequence_steps())

  print("")
  print("IO:")
  print("X0 available modes:", card.get_available_io_modes_information(0))
  print("X1 available modes:", card.get_available_io_modes_information(1))
  print("X2 available modes:", card.get_available_io_modes_information(2))
  print("X0 mode:", card.get_io_mode_information(0))
  print("X1 mode:", card.get_io_mode_information(1))
  print("X2 mode:", card.get_io_mode_information(2))
  print("X0:", card.get_io_asynchronous(0))
  print("X1:", card.get_io_asynchronous(1))
  print("X2:", card.get_io_asynchronous(2))

  card.close()

Sequence example
----------------

This example generates a four channel sequence, with digital outputs.
The following code can be found in :obj:`example_sequence.py`.

.. code-block:: python

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

Full example code
-----------------

The code can be found in :obj:`__main__.py`

.. code-block:: python

  # Choose which examples to run
  do_basic      = True    # One channel of sine wave
  do_sequence   = True    # A four channel sequenced routine with digital output
  do_double     = True    # Showing off the double output mode
  do_verbose    = True    # Reads just about every information register
  do_stop_level = True    # Sets custom stop levels for each channel

  # Do you want to use the hardware triggers, or force the trigger with software?
  use_trigger = False

  # How long before the stop command is sent
  wait_time = 10

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

  if use_trigger:
    card.trigger_coupling_use_dc(0)
    card.use_trigger_positive_edge(0, 2.5, re_arm_threshold = 1)
  
  if do_verbose:
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
    print(f"Sample rate: {card.get_sample_rate()/1e6} M samples/s")
    print("Mode:", card.get_mode_information())
    print("Available modes:", card.get_available_modes_information())
    print("Enabled channels", card.get_channels_enable())

    print("")
    print("Triggers:")
    print(f"Trigger delay: {card.get_trigger_delay()} Sa")
    print(f"Maximum trigger delay: {card.get_max_trigger_delay()} Sa")
    print("Trigger impedance:", card.get_trigger_impedance())
    print("Trigger couplings:", card.get_trigger_coupling(0), ",", card.get_trigger_coupling(1))
    print("Available trigger modes (Trigger 0):", card.get_available_trigger_modes_information(0))
    print("Available trigger modes (Trigger 1):", card.get_available_trigger_modes_information(1))
    print("Trigger modes:", card.get_trigger_mode_information(0), ",", card.get_trigger_mode_information(1))
    print(f"Lower trigger thresholds from {card.get_lower_trigger_threshold_min()} V to {card.get_lower_trigger_threshold_max()} V in steps of {card.get_lower_trigger_threshold_step()} V")
    print(f"Upper trigger thresholds from {card.get_upper_trigger_threshold_min()} V to {card.get_upper_trigger_threshold_max()} V in steps of {card.get_upper_trigger_threshold_step()} V")
    print(f"Trigger 0 lower: {card.get_lower_trigger_threshold(0):.2f} V, upper: {card.get_upper_trigger_threshold(0):.2f} V.")
    print(f"Trigger 1 lower: {card.get_lower_trigger_threshold(1):.2f} V, upper: {card.get_upper_trigger_threshold(1):.2f} V.")

    print("")
    print("Trigger masks:")
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
    print("Sequencing:")
    print("Max number of segments:", card.get_max_number_of_segments())
    print("Max number of loops per step:", card.get_max_number_of_loops_per_sequence_step())
    print("Max number of steps:", card.get_max_number_of_sequence_steps())

    print("")
    print("IO:")
    
    card.use_io_mode_asynchronous_input(0)
    card.use_io_mode_asynchronous_output(1)
    card.use_io_mode_asynchronous_output(2)
    card.set_io_asynchronous(1, False)
    card.set_io_asynchronous(2, False)
    card.set_io_asynchronous(1, 1)

    print("X0 available modes:", card.get_available_io_modes_information(0))
    print("X1 available modes:", card.get_available_io_modes_information(1))
    print("X2 available modes:", card.get_available_io_modes_information(2))
    print("X0 mode:", card.get_io_mode_information(0))
    print("X1 mode:", card.get_io_mode_information(1))
    print("X2 mode:", card.get_io_mode_information(2))
    print("X0:", card.get_io_asynchronous(0))
    print("X1:", card.get_io_asynchronous(1))
    print("X2:", card.get_io_asynchronous(2))

    card.identification_led_enable()
  
  if do_stop_level:
    card.set_channel_stop_level(0, low = True)
    card.set_channel_stop_level(1, high = True)
    card.set_channel_stop_level(2, hold_last = True)
    card.set_channel_stop_level(3, custom_value = -0.5)

  if do_basic:
    print("")
    print("Basic routine:")
    card.set_channels_enable(channel_0 = True)
    card.output_enable(0)
    card.set_amplitude(0, 0.5)
    card.set_memory_size(signal_sine.size)

    card.array_to_device([signal_sine])

    card.arm()
    if not use_trigger:
      card.force_trigger()

    if do_verbose:
      print("Started.")
      print("")

    tm.sleep(wait_time)
    card.stop()
    
    if do_verbose:
      print("Stopped.")
      print("")

  if do_sequence:
    print("")
    print("Sequence routine:")

    card.set_channels_enable(channel_0 = True, channel_1 = True, channel_2 = True, channel_3 = True)
    card.output_enable(0)
    card.set_amplitude(0, 0.5)
    card.output_enable(1)
    card.set_amplitude(1, 0.5)
    card.output_enable(2)
    card.set_amplitude(2, 0.5)
    card.output_enable(3)
    card.set_amplitude(3, 0.5)

    card.use_mode_sequence()
    card.set_number_of_segments(4)

    card.set_memory_size(card.get_number_of_segments()*signal_sine.size)

    aux_data_channels = [{"Channel" : 1, "Bit" : 13, "Port": 2}]
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

    if do_verbose:
      print("X2 mode:", card.get_io_mode_information(2))

    number_of_loops = 100000
    card.set_step_instruction(0, 0, number_of_loops)
    card.set_step_instruction(1, 1, number_of_loops//2)
    card.set_step_instruction(2, 2, number_of_loops*2)
    card.set_step_instruction(3, 3, number_of_loops, next_step = 0)

    if do_verbose:
      print("Step instruction 0:", card.get_step_instruction(0))
      print("Step instruction 3:", card.get_step_instruction(3))

      print("Channel 0 stop level:", card.get_channel_stop_level(0))
      print("Channel 1 stop level:", card.get_channel_stop_level(1))
      print("Channel 2 stop level:", card.get_channel_stop_level(2))
      print("Channel 3 stop level:", card.get_channel_stop_level(3))

    card.set_start_step(0)
    
    if do_verbose:
      print("Channel 0 enabled:", card.get_output_enable(0) == 1)
      print("Channel 1 enabled:", card.get_output_enable(1) == 1)
      print("Channel 2 enabled:", card.get_output_enable(2) == 1)
      print("Channel 3 enabled:", card.get_output_enable(3) == 1)

      print("Status:", card.get_status_information())
      print("")
    
    card.arm()
    if not use_trigger:
      card.force_trigger()
    
    if do_verbose:
      print("Started.")
      print("")

    tm.sleep(wait_time)
    card.stop()

    if do_verbose:
      print("Stopped.")
      print("")

  if do_double:
    print("")
    print("Double routine:")

    card.use_mode_single()
    card.set_number_of_loops(0)

    card.set_channels_enable(channel_0 = True, channel_2 = True)
    card.differential_enable(0)
    card.double_enable(2)

    card.output_enable(0)
    card.set_amplitude(0, 0.5)
    card.output_enable(1)
    card.set_amplitude(1, 0.5)
    card.output_enable(2)
    card.set_amplitude(2, 0.5)
    card.output_enable(3)
    card.set_amplitude(3, 0.5)

    card.set_memory_size(signal_sine.size)
    card.array_to_device([signal_rectified, signal_bipolar])

    card.arm()
    if not use_trigger:
      card.force_trigger()
    if do_verbose:
      print("Started.")
      print("")
    tm.sleep(wait_time)
    card.stop()
    if do_verbose:
      print("Stopped.")
      print("")

  if do_verbose:
    print("Status:", card.get_status_information())
  card.reset()
  card.close()