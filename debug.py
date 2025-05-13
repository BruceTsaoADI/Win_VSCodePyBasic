import json

# 這是原本的 Python dict
data = {'mode': 3, 'RTD': {'RTD1': 109.34, 'RTD2': 503.0, 'RTD3': 503.0}, 'current_in': {'chn0': 10.0, 'chn1': 19.9, 'chn2': 0.0}, 'voltage_in': {'chn0': 0, 'chn1': 0}, 'pwm_in': {'pwm_in_0': '0', 'pwm_in_1': '0', 'pwm_in_2': '0'}, 'pwm_in_duty': {'pwm_in_0': '0%', 'pwm_in_1': '0%', 'pwm_in_2': '0%'}, 'digital_in': {'d0': 0, 'd1': 0, 'd2': 0, 'd3': 0, 'd4': 0}, 'voltage_out': {'chn0': 2000, 'chn1': 3000}, 'pwm_out': {'pwm_out_0': '25000', 'pwm_out_1': '25000', 'pwm_out_2': '0'}, 'pwm_out_duty': {'pwm_out_0': '2%', 'pwm_out_1': '3%', 'pwm_out_2': '4%'}, 'digital_out': {'d0': 1, 'd1': 0, 'd2': 1, 'd3': 0, 'd4': 1}, 'alert': {'LEDSYSRDY': 0, 'LED_FAULT': 0, 'P1V1': 0, 'P1V8': 0, 'P3V3': 0, 'P5V0': 0}, 'ad74416h_1_alert': {'revision_id': 1, 'TEMP_ALERT': 0, 'RESET_OCCURRED': 0, 'chA_OV': 0, 'chA_SC': 0, 'chA_OC': 0, 'chB_OV': 0, 'chB_SC': 0, 'chB_OC': 1, 'chC_OV': 0, 'chC_SC': 0, 'chC_OC': 1, 'chD_OV': 0, 'chD_SC': 0, 'chD_OC': 1}, 'ad74416h_2_alert': {'revision_id': 1, 'TEMP_ALERT': 0, 'RESET_OCCURRED': 0, 'chA_OV': 0, 'chA_SC': 0, 'chA_OC': 0, 'chB_OV': 0, 'chB_SC': 0, 'chB_OC': 0, 'chC_OV': 0, 'chC_SC': 0, 'chC_OC': 0, 'chD_OV': 0, 'chD_SC': 0, 'chD_OC': 0}, 'ad74416h_3_alert': {'revision_id': 1, 'TEMP_ALERT': 0, 'RESET_OCCURRED': 0, 'chA_OV': 0, 'chA_SC': 0, 'chA_OC': 0, 'chB_OV': 0, 'chB_SC': 0, 'chB_OC': 0, 'chC_OV': 0, 'chC_SC': 0, 'chC_OC': 0, 'chD_OV': 0, 'chD_SC': 0, 'chD_OC': 0}, 'ad74416h_4_alert': {'revision_id': 1, 'TEMP_ALERT': 0, 'RESET_OCCURRED': 0, 'chA_OV': 0, 'chA_SC': 0, 'chA_OC': 0, 'chB_OV': 0, 'chB_SC': 0, 'chB_OC': 0, 'chC_OV': 0, 'chC_SC': 0, 'chC_OC': 0, 'chD_OV': 0, 'chD_SC': 0, 'chD_OC': 0}, 'PID': {'kp': 3.0, 'ki': 0.1, 'kd': 1.0, 'target_temperature': 40.0, 'start_flag': 0}}


# 轉成合法 JSON 字串
json_str = json.dumps(data, indent=4)

# 印出 JSON 結果
print(json_str)
