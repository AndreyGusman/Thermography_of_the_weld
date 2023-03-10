class DataFormat:
    # Формат чтения/записи PLC profibus.py

    sendPLC = {'W_Live_Bit': None, 'W_Emergency_Stop': None, 'W_Defect_bool': None, 'W_spare_04': None,
               'W_spare_05': None,
               'W_spare_06': None, 'W_spare_07': None, 'W_spare_08': None, 'W_spare_09': None, 'W_spare_10': None,
               'W_spare_11': None, 'W_spare_12': None, 'W_spare_13': None, 'W_spare_14': None, 'W_spare_15': None,
               'W_spare_16': None, 'W_spare_17': None, 'W_spare_091': None, 'W_spare_0911': None, 'W_spare_0912': None,
               'W_Defect_dint': None, 'W_Temperature': None, 'W_Reserve1': None, 'W_Reserve22': None,
               'W_Reserve3': None,
               'W_Reserve4': None, 'W_Reserve5': None, 'W_Reserve6': None}

    fromPLC = {'Live_Bit': None, 'Emergency_Stop': None, 'TestRelease': None, 'SeamSkip': None, 'NoJob': None,
               'Stand_Perman_Perm': None, 'spare_01': None, 'spare_013': None, 'spare_02': None, 'spare_03': None,
               'spare_04': None, 'spare_05': None, 'spare_06': None, 'spare_07': None, 'spare_08': None,
               'spare_09': None,
               'spare_091': None, 'spare_0911': None, 'spare_0912': None, 'Pos_UZK': None, 'RollersSpeedSet': None,
               'RollersSpeedAkt': None, 'Diam': None, 'Part_Coil_UZK': None, 'Part_Coil_TOS': None, 'Count_Pipe': None,
               'Num_Pipe': None, 'Length_Pipe': None, 'Pos_Begin_Cut': None, 'Num_Coil_UZK': None, 'Num_Coil_TOS': None,
               'Reserve1': None, 'Reserve2': None, 'Reserve3': None, 'Reserve4': None, 'Reserve5': None,
               'Reserve6': None}

    # выборка интовых переменных
    using_plc_var_name = ['Pos_UZK', 'RollersSpeedSet', 'RollersSpeedAkt', 'Diam', 'Part_Coil_UZK', 'Part_Coil_TOS',
                          'Count_Pipe', 'Length_Pipe', 'Num_Pipe', 'Pos_Begin_Cut', 'Num_Coil_UZK', 'Num_Coil_TOS']

    # сопутствующие данные текущего кадра
    var_name_current_img = ['image', 'Pos_UZK', 'RollersSpeedSet', 'RollersSpeedAkt', 'Diam']
    # сопутствующие данные дефектного кадра
    var_name_broken_img = ['image', 'Defect', 'Pos_UZK', 'RollersSpeedAkt', 'Defect_temperature']

    # формат посылки интерфейсу от камеры, содержит картинку и сопутствующие данные
    dict_camera_to_interface = {'current_img': None, 'broken_img': None}

    # формат посылки записи паркета см. config.PARQUET_MODE
    parquet_format_mode_1 = ['Time', 'Length', 'Pos_UZK', 'Part_Coil_UZK', 'Part_Coil_TOS',
                             'Count_Pipe', 'Length_Pipe', 'Num_Pipe', 'Num_Coil_UZK',
                             'reserve zone 1', 'reserve zone 2', 'Image']

    parquet_format_mode_2 = ['Time', 'Length', 'Pos_UZK', 'Part_Coil_UZK', 'Part_Coil_TOS',
                             'Count_Pipe', 'Length_Pipe', 'Num_Pipe', 'Num_Coil_UZK',
                             'reserve zone 1', 'reserve zone 2', 'Image', 'Defect mask']

    parquet_format_mode_3 = ['Time', 'Length', 'Pos_UZK', 'Part_Coil_UZK', 'Part_Coil_TOS',
                             'Count_Pipe', 'Length_Pipe', 'Num_Pipe', 'Num_Coil_UZK',
                             'reserve zone 1', 'reserve zone 2', 'Image', 'Defect mask', 'type']

    parquet_metadata = ['number_frames', 'time_first_frame', 'time_last_frame', 'length_first_frame',
                        'length_last_frame', 'pos_UZK_first_frame', 'pos_UZK_last_frame']

    # Формат чтения/записи трансфокатора transfocator.py
    toCamera = {'Zoom+': None, 'Zoom-': None, 'SetZoom': None, 'Focus+': None, 'Focus-': None, 'SetFocus': None,
                'DiagOFF': None, 'DiagON': None}

    fromCamera = {'ReqActualZoom+': None, 'ReqActualZoom-': None, 'ReqActualFocus+': None, 'ReqActualFocus-': None}

    using_transfocator_var_name = ['ReqActualZoom+', 'ReqActualZoom-', 'ReqActualFocus+', 'ReqActualFocus-']

    shared_array_index = {
        'main_p_is_alive': 0,
        'main_p_pipe_worker_thread_is_alive': 1,
        'main_p_task_creater_thread_is_alive': 2,
        'main_p_task_executor_thread_is_alive': 3,
        'main_p_force_stop': 4,
        'main_p_reserve_0': 5,
        'main_p_reserve_1': 6,
        'main_p_reserve_2': 7,
        'main_p_reserve_3': 8,
        'main_p_reserve_4': 9,

        'camera_and_nn_p_is_alive': 10,
        'camera_and_nn_p_pipe_worker_thread_is_alive': 11,
        'camera_and_nn_p_task_creater_thread_is_alive': 12,
        'camera_and_nn_p_task_executor_thread_is_alive': 13,
        'camera_and_nn_p_force_stop': 14,
        'camera_and_nn_p_reserve_0': 15,
        'camera_and_nn_p_reserve_1': 16,
        'camera_and_nn_p_reserve_2': 17,
        'camera_and_nn_p_reserve_3': 18,
        'camera_and_nn_p_reserve_4': 19,

        'parquet_p_is_alive': 20,
        'parquet_p_pipe_worker_thread_is_alive': 21,
        'parquet_p_task_creater_thread_is_alive': 22,
        'parquet_p_task_executor_thread_is_alive': 23,
        'parquet_p_force_stop': 24,
        'parquet_p_reserve_0': 25,
        'parquet_p_reserve_1': 26,
        'parquet_p_reserve_2': 27,
        'parquet_p_reserve_3': 28,
        'parquet_p_reserve_4': 29,

        'hmi_p_is_alive': 30,
        'hmi_p_pipe_worker_thread_is_alive': 31,
        'hmi_p_task_creater_thread_is_alive': 32,
        'hmi_p_task_executor_thread_is_alive': 33,
        'hmi_p_force_stop': 34,
        'hmi_p_reserve_0': 35,
        'hmi_p_reserve_1': 36,
        'hmi_p_reserve_2': 37,
        'hmi_p_reserve_3': 38,
        'hmi_p_reserve_4': 39,

        'shared_reserve_0': 40,
        'shared_reserve_1': 41,
        'shared_reserve_2': 42,
        'shared_reserve_3': 43,
        'shared_reserve_4': 44,
        'shared_reserve_5': 45,
        'shared_reserve_6': 46,
        'shared_reserve_7': 47,
        'shared_reserve_8': 48,
        'shared_reserve_9': 49
    }

