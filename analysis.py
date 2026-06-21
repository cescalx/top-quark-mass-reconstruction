# Top Quark Coursework Analysis
# This script loads simulated LHC collision data and performs a basic check
# of the dataset before reconstructing particle masses using four‑momentum.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # colour maps for nicer plots


# load the CSV dataset containing reconstructed particle four‑momenta
# each row represents one proton–proton collision event
data = pd.read_csv("datafile.csv")
data.columns = data.columns.str.strip()

# display the first few events to verify the dataset loaded correctly
print("First few events in the dataset:")
print(data.head())

# print the column names to identify the available particle four‑vector components
print("\nColumns in the dataset:")
print(data.columns)


# function to compute invariant mass using the relativistic relation
# m = sqrt(E^2 − px^2 − py^2 − pz^2)
def invariant_mass(E,px,py,pz):
    return np.sqrt(E**2 - px**2 - py**2 - pz**2)

# example calculation: compute the invariant mass of jet J1
# from the first collision event in the dataset

# Select the first event (row) from the dataset
row = data.iloc[0]

# Extract the four‑momentum components of jet J1
E = row["J1_E"]
px = row["J1_Px"]
py = row["J1_Py"]
pz = row["J1_Pz"]

# calculate the invariant mass using the function defined above
mass = invariant_mass(E, px, py, pz)

# convert from MeV to GeV (1 GeV = 1000 MeV) and print the result
print("\nInvariant mass of J1 (first event):", mass/1000,"GeV")

# calculate invariant masses of all light‑jet pairs
# one pair should correspond to the W boson decay
# J1 + J2
E = row["J1_E"] + row["J2_E"]
px = row["J1_Px"] + row["J2_Px"]
py = row["J1_Py"] + row["J2_Py"]
pz = row["J1_Pz"] + row["J2_Pz"]

m12 = invariant_mass(E, px, py, pz) / 1000

# J1 + J3
E = row["J1_E"] + row["J3_E"]
px = row["J1_Px"] + row["J3_Px"]
py = row["J1_Py"] + row["J3_Py"]
pz = row["J1_Pz"] + row["J3_Pz"]

m13 = invariant_mass(E, px, py, pz) / 1000

# J2 + J3
E = row["J2_E"] + row["J3_E"]
px = row["J2_Px"] + row["J3_Px"]
py = row["J2_Py"] + row["J3_Py"]
pz = row["J2_Pz"] + row["J3_Pz"]

m23 = invariant_mass(E, px, py, pz) / 1000

print("\nJet pair invariant masses (GeV):")
print("J1 + J2:", m12)
print("J1 + J3:", m13)
print("J2 + J3:", m23)

# reconstruct possible top quark masses
# combine the W candidate jets with each b‑jet
# option 1: B1 + J2 + J3
E = row["B1_E"] + row["J2_E"] + row["J3_E"]
px = row["B1_Px"] + row["J2_Px"] + row["J3_Px"]
py = row["B1_Py"] + row["J2_Py"] + row["J3_Py"]
pz = row["B1_Pz"] + row["J2_Pz"] + row["J3_Pz"]

top1 = invariant_mass(E, px, py, pz) / 1000

# option 2: B2 + J2 + J3
E = row["B2_E"] + row["J2_E"] + row["J3_E"]
px = row["B2_Px"] + row["J2_Px"] + row["J3_Px"]
py = row["B2_Py"] + row["J2_Py"] + row["J3_Py"]
pz = row["B2_Pz"] + row["J2_Pz"] + row["J3_Pz"]

top2 = invariant_mass(E, px, py, pz) / 1000

print("\nPossible top masses (GeV):")
print("B1 + J2 + J3:", top1)
print("B2 + J2 + J3:", top2)

# ------------------------------------------------------------
# Next step: repeat the reconstruction for all events
# We will loop through every collision event in the dataset
# and store the reconstructed top mass values
# ------------------------------------------------------------

 # store reconstructed masses
w_masses = []
top_masses = []

for _, row in data.iterrows():

    # compute invariant masses of all light‑jet pairs
    E = row["J1_E"] + row["J2_E"]
    px = row["J1_Px"] + row["J2_Px"]
    py = row["J1_Py"] + row["J2_Py"]
    pz = row["J1_Pz"] + row["J2_Pz"]
    m12 = invariant_mass(E, px, py, pz) / 1000

    E = row["J1_E"] + row["J3_E"]
    px = row["J1_Px"] + row["J3_Px"]
    py = row["J1_Py"] + row["J3_Py"]
    pz = row["J1_Pz"] + row["J3_Pz"]
    m13 = invariant_mass(E, px, py, pz) / 1000

    E = row["J2_E"] + row["J3_E"]
    px = row["J2_Px"] + row["J3_Px"]
    py = row["J2_Py"] + row["J3_Py"]
    pz = row["J2_Pz"] + row["J3_Pz"]
    m23 = invariant_mass(E, px, py, pz) / 1000

    # choose the jet pair closest to the W boson mass (~80 GeV)
    pairs = {"J1J2": m12, "J1J3": m13, "J2J3": m23}
    best_pair = min(pairs, key=lambda x: abs(pairs[x] - 80))

    # store the invariant mass of the selected jet pair (W candidate)
    w_masses.append(pairs[best_pair])

    if best_pair == "J1J2":
        jA, jB = "J1", "J2"
    elif best_pair == "J1J3":
        jA, jB = "J1", "J3"
    else:
        jA, jB = "J2", "J3"

    # reconstruct top candidates using both b‑jets
    E = row["B1_E"] + row[f"{jA}_E"] + row[f"{jB}_E"]
    px = row["B1_Px"] + row[f"{jA}_Px"] + row[f"{jB}_Px"]
    py = row["B1_Py"] + row[f"{jA}_Py"] + row[f"{jB}_Py"]
    pz = row["B1_Pz"] + row[f"{jA}_Pz"] + row[f"{jB}_Pz"]
    top1 = invariant_mass(E, px, py, pz) / 1000

    E = row["B2_E"] + row[f"{jA}_E"] + row[f"{jB}_E"]
    px = row["B2_Px"] + row[f"{jA}_Px"] + row[f"{jB}_Px"]
    py = row["B2_Py"] + row[f"{jA}_Py"] + row[f"{jB}_Py"]
    pz = row["B2_Pz"] + row[f"{jA}_Pz"] + row[f"{jB}_Pz"]
    top2 = invariant_mass(E, px, py, pz) / 1000

    candidate = min(top1, top2)

    # apply physics cut (removes unphysical large masses)
    if candidate < 250:
        top_masses.append(float(candidate))

print("\nTotal reconstructed top candidates:", len(top_masses))
print("Example reconstructed masses:", top_masses[:10])


# Histogram of reconstructed top quark masses
# This plots the distribution of the reconstructed top masses

plt.figure()

# create histogram with bin edges aligned to the axis scale

plt.hist(top_masses, bins=np.arange(0, 501, 10), color="#F5A9FF", edgecolor="black")

# --- Gaussian fit for top mass peak ---
from scipy.optimize import curve_fit

# use filtered masses (cleaner data)
filtered_masses = [m for m in top_masses if 50 <= m <= 300]

# histogram for fitting (same binning)
counts, bins = np.histogram(filtered_masses, bins=np.arange(50, 301, 10))
bin_centers = (bins[:-1] + bins[1:]) / 2

# restrict to peak region
fit_mask = (bin_centers > 130) & (bin_centers < 200)
x_fit = bin_centers[fit_mask]
y_fit = counts[fit_mask]

# Gaussian function
def gaussian_top(x, A, mu, sigma):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

# initial guesses
A_guess = max(y_fit)
mu_guess = bin_centers[np.argmax(counts)]
sigma_guess = 20

# fit
params, _ = curve_fit(gaussian_top, x_fit, y_fit, p0=[A_guess, mu_guess, sigma_guess])
A_fit, mu_fit, sigma_fit = params

# plot fit
x_smooth = np.linspace(50, 300, 1000)
y_smooth = gaussian_top(x_smooth, A_fit, mu_fit, sigma_fit)
plt.plot(x_smooth, y_smooth, linewidth=2, color="#9D00FF")  # custom blue

print(f"Top mass from Gaussian fit: {mu_fit:.1f} ± {sigma_fit:.1f} GeV")


# estimate the top mass using histogram peak (more robust than mean)
filtered_masses = [m for m in top_masses if 50 <= m <= 300]

# use finer bins and take bin CENTER (not edge)
counts, bins = np.histogram(filtered_masses, bins=np.arange(0, 501, 5))
bin_centers = (bins[:-1] + bins[1:]) / 2
top_mass_estimate = bin_centers[np.argmax(counts)]

# estimate uncertainty from central peak region (robust)
central_region = [m for m in filtered_masses if 130 <= m <= 200]
# use standard error (smaller, more precise uncertainty)
uncertainty = np.std(central_region) / np.sqrt(len(central_region))

print(f"Estimated top mass from peak: {top_mass_estimate:.1f} GeV")
print(f"Estimated uncertainty (std dev): ±{uncertainty:.1f} GeV")

# draw dashed line at the estimated mass from the filtered data
plt.axvline(top_mass_estimate, linestyle="--", color="#2D0048",
            label=f"Peak = {top_mass_estimate:.1f} ± {uncertainty:.1f} GeV")

# label the plot
plt.xlabel("Reconstructed Top Mass (GeV)")
plt.ylabel("Number of Events")
plt.title("Reconstructed Top Quark Mass Distribution")

#small edits
plt.xlim(50, 300)  # focus on physically relevant region
plt.xticks(np.arange(50, 301, 25))  # cleaner tick spacing for zoomed range
plt.grid(axis="y", alpha=0.3)  # horizontal grid only to avoid vertical lines confusing bin alignment
plt.legend()


# display the histogram
plt.show()

# ------------------------------------------------------------
# Histogram of invariant mass of the selected light‑jet pairs
# This should show a peak near the W boson mass (~80 GeV)
# ------------------------------------------------------------

plt.figure()

plt.hist(w_masses, bins=np.arange(0, 201, 10), color="#FFD2EC", edgecolor="black")

# --- Gaussian fit for W mass peak ---
from scipy.optimize import curve_fit

# histogram for fitting (use same binning)
counts, bins = np.histogram(w_masses, bins=np.arange(0, 201, 10))
bin_centers = (bins[:-1] + bins[1:]) / 2

# restrict to peak region
fit_mask = (bin_centers > 60) & (bin_centers < 100)
x_fit = bin_centers[fit_mask]
y_fit = counts[fit_mask]

# Gaussian function
def gaussian(x, A, mu, sigma):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

# initial guesses
A_guess = max(y_fit)
mu_guess = 80
sigma_guess = 10

# fit
params, _ = curve_fit(gaussian, x_fit, y_fit, p0=[A_guess, mu_guess, sigma_guess])
A_fit, mu_fit, sigma_fit = params

# estimate uncertainty using standard error of central region
central_region_w = [m for m in w_masses if 60 <= m <= 100]
uncertainty_w = np.std(central_region_w) / np.sqrt(len(central_region_w))

# plot fit
x_smooth = np.linspace(0, 200, 1000)
y_smooth = gaussian(x_smooth, A_fit, mu_fit, sigma_fit)
plt.plot(x_smooth, y_smooth, linewidth=2, color="#ff00aa")  # custom blue

print(f"W mass from Gaussian fit: {mu_fit:.1f} ± {sigma_fit:.1f} GeV")
print(f"W mass uncertainty (standard error): ±{uncertainty_w:.1f} GeV")

 # reference line for the W boson mass
plt.axvline(mu_fit, linestyle="--", color="#920042",
            label=f"W = {mu_fit:.1f} ± {uncertainty_w:.1f} GeV")
plt.legend()

plt.xlabel("Invariant Mass of Selected Jet Pair (GeV)")
plt.ylabel("Number of Events")
plt.title("Invariant Mass of Light‑Jet Pairs (W Candidates)")

plt.xlim(0,200)
plt.xticks(np.arange(0, 201, 20))
plt.grid(axis="y", alpha=0.3)

plt.show()
