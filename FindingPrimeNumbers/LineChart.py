import matplotlib.pyplot as plt # reinstall this shit
import numpy as np
from scipy.interpolate import spline

# https://www.youtube.com/watch?v=uSB8UBrbMfk smooth line

y = np.array(['1','1','1', '1', '15', '40', '444' ])
x = np.array(['\n42459479','225149933','\n4074339571', '417901915699', '\n902359098441667', '24276700508335600', '\n975062898293547000'])

x_smooth = np.linspace(x.min(), x.max(), 300)
y_smooth = spline(x, y, x_smooth)


plt.plot(x_smooth, y_smooth)
plt.ylabel("Tijd (in sec)")
plt.xlabel("N")
plt.show()

