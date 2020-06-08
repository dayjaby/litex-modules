from migen import *
from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform
from litex.soc.integration.soc_core import SoCMini
from litex.soc.integration.builder import Builder
from litex.soc.cores.uart import UARTWishboneBridge
from litex.soc.interconnect.csr import *
from litex_modules.hcsr04 import HCSR04

_io = [
    ("clk100", 0, Pins("P126"), IOStandard("LVCMOS33")),

    # for WishboneUARTBridge
    ("serial", 0,
        Subsignal("tx", Pins("P104"), IOStandard("LVCMOS33"), # GPIO-N21
                  Misc("SLEW=FAST")),
        Subsignal("rx", Pins("P101"), IOStandard("LVCMOS33"),  # GPIO-N20
                  Misc("SLEW=FAST"))),

    ("hcsr04", 0,
        Subsignal("echo", Pins("P100"), IOStandard("LVTTL")),    # GPIO-P21
        Subsignal("trigger", Pins("P102"), IOStandard("LVCMOS33"))  # GPIO-P20
    ),

    ("user_btn", 0, Pins("P124"), IOStandard("LVCMOS33"), Misc("PULLUP")),
]

class Platform(XilinxPlatform):
    name = "mimas"
    default_clk_name = "clk100"
    default_clk_period = 10

    def __init__(self):
        XilinxPlatform.__init__(self, "xc6slx9-tqg144", _io, toolchain="ise")

class BaseSoC(SoCMini):
    def __init__(self, platform, **kwargs):
        self.sys_clk_freq = int(100e6)
        SoCMini.__init__(self, platform, self.sys_clk_freq, csr_data_width=32,
            ident="My first LiteX System On Chip", ident_version=True)

        self.submodules.crg = CRG(platform.request("clk100"), ~platform.request("user_btn", 0))

        serial = platform.request("serial", 0)
        self.submodules.serial_bridge = UARTWishboneBridge(serial, self.sys_clk_freq)
        self.add_wb_master(self.serial_bridge.wishbone)

        self.submodules.hcsr04_0 = HCSR04(platform.request("hcsr04", 0), self.sys_clk_freq, samplerate=50)
        self.add_csr("hcsr04_0")

soc = BaseSoC(Platform())

builder = Builder(soc, output_dir="build", csr_csv="csr.csv")
builder.build(build_name="top")
