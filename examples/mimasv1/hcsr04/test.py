from litex import RemoteClient
import time

wb = RemoteClient()
wb.open()

class HCSR04:
    def __init__(self, regs, nr):
        self._enable = getattr(regs, f"hcsr04_{nr}_enable")
        self._echo_width = getattr(regs, f"hcsr04_{nr}_echo_width")

    def enable(self):
        self._enable.write(1)

    def disable(self,):
        self._enable.write(0)

    def enabled(self):
        return self._enable.read()

    def read(self):
        return self._echo_width.read()
            
sonar = HCSR04(wb.regs, 0)
sonar.enable()
print(sonar.enabled())
for i in range(100):
    time.sleep(0.1)
    print(sonar.read() * 343.0 / 2.0 / 100e6)
sonar.disable()

wb.close()
