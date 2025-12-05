import time
import struct
from smbus2 import SMBus

# ==========================================
# 4路电机驱动板 I2C 控制协议
# ==========================================

# I2C 总线号
BUS_NUM = 5
# 设备地址 (根据文档为0x26)
DEVICE_ADDR = 0x26

# 寄存器地址 (根据文档)
REG_MOTOR_TYPE = 0x01      # 电机类型配置 (只写)
REG_DEADZONE = 0x02        # 死区配置 (只写)
REG_MAGNETIC_LINES = 0x03  # 磁环线数 (只写)
REG_REDUCTION_RATIO = 0x04 # 减速比 (只写)
REG_WHEEL_DIAMETER = 0x05  # 轮子直径 (只写)
REG_SPEED_CONTROL = 0x06   # 速度控制 (只写)
REG_PWM_CONTROL = 0x07     # PWM控制 (只写)
REG_BATTERY_VOLTAGE = 0x08 # 读取电池电量 (只读)
REG_M1_ENCODER = 0x10      # 读取M1编码器数据 (只读)

def main():
    print(f"正在打开 I2C Bus {BUS_NUM}...")
    try:
        bus = SMBus(BUS_NUM)
    except Exception as e:
        print(f"无法打开总线: {e}")
        return

    print("开始测试：向 0x26 发送4路电机驱动板协议指令...")
    
    # 先读取电池电量测试I2C读取功能
    def read_battery_voltage():
        try:
            # 读取电池电量寄存器 (0x08)
            # 根据文档：data = (buf[0] <<8|buf[1](@ref)/10
            data = bus.read_i2c_block_data(DEVICE_ADDR, REG_BATTERY_VOLTAGE, 2)
            if len(data) >= 2:
                voltage = (data[0] << 8 | data[1](@ref) / 10.0
                print(f"电池电压: {voltage:.2f}V")
                return voltage
            else:
                print("读取电池电量失败：数据长度不足")
                return None
        except OSError as e:
            print(f"读取电池电量失败: {e}")
            return None
    
    # 读取M1编码器数据
    def read_m1_encoder():
        try:
            # 读取M1编码器寄存器 (0x10)
            # 根据文档：data = buf[0] <<8|buf
            data = bus.read_i2c_block_data(DEVICE_ADDR, REG_M1_ENCODER, 2)
            if len(data) >= 2:
                encoder_value = (data[0] << 8 | data[1](@ref)
                # 处理有符号数（如果最高位是1，则为负数）
                if encoder_value & 0x8000:
                    encoder_value = encoder_value - 0x10000
                print(f"M1编码器值: {encoder_value}")
                return encoder_value
            else:
                print("读取编码器失败：数据长度不足")
                return None
        except OSError as e:
            print(f"读取编码器失败: {e}")
            return None

    # 定义发送电机速度的函数
    def set_motor_speeds(speed_m1, speed_m2, speed_m3, speed_m4):
        # 限制速度范围: -1000 到 1000
        speeds = [speed_m1, speed_m2, speed_m3, speed_m4]
        for i in range(4):
            if speeds[i] > 1000: speeds[i] = 1000
            if speeds[i] < -1000: speeds[i] = -1000
        
        # 转换为大端模式的int16_t数组
        data_bytes = bytearray()
        for speed in speeds:
            speed_int = int(speed)
            data_bytes.extend(struct.pack('>h', speed_int))
        
        try:
            # 写入速度控制寄存器 (0x06)
            bus.write_i2c_block_data(DEVICE_ADDR, REG_SPEED_CONTROL, list(data_bytes))
            print(f"设置速度: M1={speed_m1}, M2={speed_m2}, M3={speed_m3}, M4={speed_m4}")
            return True
        except OSError as e:
            print(f"I2C 写入失败: {e}")
            return False

    # 定义发送PWM控制的函数
    def set_motor_pwm(pwm_m1, pwm_m2, pwm_m3, pwm_m4):
        # 限制PWM范围: -3600 到 3600
        pwms = [pwm_m1, pwm_m2, pwm_m3, pwm_m4]
        for i in range(4):
            if pwms[i] > 3600: pwms[i] = 3600
            if pwms[i] < -3600: pwms[i] = -3600
        
        # 转换为大端模式的int16_t数组
        data_bytes = bytearray()
        for pwm in pwms:
            pwm_int = int(pwm)
            data_bytes.extend(struct.pack('>h', pwm_int))
        
        try:
            # 写入PWM控制寄存器 (0x07)
            bus.write_i2c_block_data(DEVICE_ADDR, REG_PWM_CONTROL, list(data_bytes))
            print(f"设置PWM: M1={pwm_m1}, M2={pwm_m2}, M3={pwm_m3}, M4={pwm_m4}")
            return True
        except OSError as e:
            print(f"I2C 写入失败: {e}")
            return False

    try:
        print("=== 测试开始 ===")
        
        # 1. 先读取电池电量，确认I2C通信正常
        print("\n1. 读取电池电量...")
        voltage = read_battery_voltage()
        if voltage is None:
            print("警告：无法读取电池电量，但继续测试...")
        
        # 2. 读取编码器数据（如果电机有编码器）
        print("\n2. 读取M1编码器数据...")
        encoder_value = read_m1_encoder()
        
        # 3. 测试PWM控制（对所有电机都有效）
        print("\n3. PWM控制测试 - 前进")
        # 您的电机连接：M2=左轮，M4=右轮
        if set_motor_pwm(0, 1000, 0, 1000):
            print("PWM控制发送成功")
            time.sleep(2)
        else:
            print("PWM控制发送失败")
        
        print("\n4. PWM控制测试 - 停止")
        set_motor_pwm(0, 0, 0, 0)
        time.sleep(1)
        
        print("\n5. PWM控制测试 - 后退")
        set_motor_pwm(0, -1000, 0, -1000)
        time.sleep(2)
        
        print("\n6. PWM控制测试 - 停止")
        set_motor_pwm(0, 0, 0, 0)
        time.sleep(1)
        
        # 4. 测试速度控制（只对带编码器的电机有效）
        print("\n7. 速度控制测试 - 前进")
        # 如果电机带编码器，使用速度控制
        if set_motor_speeds(0, 500, 0, 500):
            print("速度控制发送成功")
            time.sleep(2)
        else:
            print("速度控制发送失败，可能寄存器地址错误")
        
        print("\n8. 速度控制测试 - 停止")
        set_motor_speeds(0, 0, 0, 0)
        time.sleep(1)
        
        # 再次读取编码器数据看是否有变化
        print("\n9. 再次读取M1编码器数据...")
        read_m1_encoder()
        
        print("\n=== 测试结束 ===")
        
    except KeyboardInterrupt:
        # 紧急停止
        print("\n紧急停止所有电机...")
        set_motor_pwm(0, 0, 0, 0)
        set_motor_speeds(0, 0, 0, 0)
        print("已停止所有电机")

if __name__ == "__main__":
    main()
