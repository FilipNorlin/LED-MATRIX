from RTD import RTD
import numpy as np
import matplotlib.pyplot as plt

pt1000 = RTD(1000)
R1 = 1e3
Vcc = 3.3


def gain_offset(vin):
    R2 = 10e3
    R3 = 131e3
    R4 = 37.4e3

    return vin * (R3/R4 + R4/R2 + 1) - ((Vcc * R4) / R2)


vout = []
t_min = -40
t_max = 70
t_lst = []
pt1000_resistance = []
v_div = []

for t in range(t_min, t_max):
    pt1000.set_temperature(t)
    R2 = pt1000.get_resistance()
    pt1000_resistance.append(R2)
    T = R2 / (R1 + R2)
    v_div.append(Vcc * T)
    vout.append(gain_offset(Vcc * T))
    t_lst.append(t)


plt.figure()
plt.plot(t_lst, vout, label="OP")
plt.plot(t_lst, v_div, label="DIV")
plt.title("Voltage out")
plt.xlabel("Temp (°C)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid()
#plt.savefig(plot_folder + "Complete_Converter_Closed_Loop.png")
plt.show()

plt.figure()
plt.plot(t_lst, pt1000_resistance)
plt.title("PT1000 Resistance")
plt.xlabel("Temp ( )")
plt.ylabel("Resistance (V)")
plt.grid()
#plt.savefig(plot_folder + "Complete_Converter_Closed_Loop.png")
plt.show()


# while True:
#     pt1000.set_temperature(float(input("Temperature: ")))
#     print(pt1000.get_resistance())