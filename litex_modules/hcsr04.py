from migen import *
from litex.soc.interconnect.csr import CSR, CSRStatus, AutoCSR

class HCSR04(Module, AutoCSR):
    def __init__(self, pads, clk_freq, samplerate=1):
        self.enable = CSR()
        self.echo_width = CSRStatus(32)

        #trigger_width = int(clk_freq / 1e5) # 10us
        trigger_width = int(clk_freq / 5e4) # 10us
        period = int(clk_freq / samplerate)

        enable = Signal()
        count = Signal(32)
        echo_count = Signal(32)
        got_echo = Signal()

        self.sync += [
            If(self.enable.re,
                enable.eq(self.enable.r)
            ),
            If(enable,
                # trigger
                If(count < trigger_width,
                    pads.trigger.eq(1),
                ).Else(
                    pads.trigger.eq(0),
                ),
                # echo
                If(pads.echo,
                    got_echo.eq(1),
                    echo_count.eq(echo_count + 1)
                ).Elif(~pads.echo & got_echo,
                    self.echo_width.status.eq(echo_count),
                    got_echo.eq(0),
                    echo_count.eq(0)
                ),
                # counter
                If(count == period-1,
                    count.eq(0)
                ).Else(
                    count.eq(count+1)
                )
            ).Else(
                pads.trigger.eq(0)
            )
        ]
