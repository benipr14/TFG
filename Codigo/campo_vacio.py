import matplotlib.pyplot as plt
from mplsoccer import Pitch

fig, ax = plt.subplots(figsize=(16, 9))
pitch = Pitch(pitch_type='opta')
pitch.draw(ax=ax)
plt.show()
