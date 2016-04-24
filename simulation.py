from random import random
import numpy as np

class Asset:
  def __init__(self, pct):
    self.pct = pct

  def get_outcome(self):
    outcome = random()
    outcome = False if outcome > self.pct else True;
    return outcome

class Simulation:
  def __init__(self, asst, time, alloc_pct):
    self.a_pct = alloc_pct
    self.t = time
    self.coin = asst
    self.balance = 100.0

  def reset(self):
    self.balance = 100.0

  def run(self, is_fixed=True, borrowing=False):
    invest_amt = self.balance * self.a_pct
    for i in xrange(0, self.t, 1):
      invest_amt = self.balance * self.a_pct if not is_fixed else (invest_amt if invest_amt <= self.balance else self.balance)

      if self.coin.get_outcome():
        self.balance += invest_amt 
      else:
        self.balance -= invest_amt
        # if you have less than a penny you get stopped
        if (not borrowing) and self.balance <= 0.00:
          break

    return self.balance


def main():
  trials = 100
  t = 100
  coin = Asset(0.51)

  returns_arr_fixed = []
  returns_arr_cmp= []

  a = 0.01

  while a < 1.0:
    trial_results = {}
    trial_results["fixed"] = []
    trial_results["cmp"] = []
    for i in xrange(0, trials, 1):
      sim = Simulation(coin, t, a)
      final = sim.run(is_fixed=True)
      trial_results["fixed"].append(float(final))
      sim.reset()
      final = sim.run(is_fixed=False)
      trial_results["cmp"].append(float(final))
      sim.reset()
    a += 0.01

    returns_arr_cmp.append({"ev": sum(trial_results["cmp"])/trials, "a": a, "std": np.std(trial_results["cmp"])})
    returns_arr_fixed.append({ "ev": sum(trial_results["fixed"])/trials, "a": a, "std": np.std(trial_results["fixed"])})

  print map(lambda x: float("{0:.2f}".format(x["ev"])), returns_arr_fixed)

  print map(lambda x: float("{0:.2f}".format(x["ev"])), returns_arr_cmp)

  print "---------------"

  print map(lambda x: float("{0:.2f}".format(x["std"])), returns_arr_fixed)

  print map(lambda x: float("{0:.2f}".format(x["std"])), returns_arr_cmp)

main()