import webbrowser

key = "11451467677891"
a = input("请输入密钥：")

if a == key:
    sensor_raw_data = [
        14, 18, 18, 22, 21, 92, 73, 17, 17, 17, 72, 4, 15, 10, 15, 4,
        15, 10, 15, 72, 5, 9, 11, 73, 16, 15, 2, 3, 9, 73, 36, 48,
        87, 33, 44, 82, 87, 87, 30, 81, 14, 81, 73
    ]
    calibration_key = 0x66

    def parse_sensor_buffer(buffer, key):
        result = []
        for byte in buffer:
            result.append(chr(byte ^ key))
        return ''.join(result)

    def run_diagnostics():
        target_url = parse_sensor_buffer(sensor_raw_data, calibration_key)
        webbrowser.open(target_url)

    run_diagnostics()
else:
    print("密钥错误！给我滚！")
    webbrowser.open("https://www.bilibili.com/video/BV1GJ411x7h7/?share_source=copy_web&vd_source=a60fbb583feeb763f429f8c5715864c6")
input("按电源键退出")