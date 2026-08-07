# Broadband Antennas Integrated with Radome Faces for Passive Detection of Clandestine or Anomalous RF Signals

**Literature review based on Consensus search results**  
**Date:** 6 August 2026

---

# Search method

This review used a **Decomposition framework** with five sub-areas:

1.  broadband antenna architectures and radome-face placement;
2.  electromagnetic effects and functional radomes;
3.  passive emitter detection, direction finding, and localization;
4.  clandestine, anomalous, and deviated-signal identification; and
5.  receiver integration, calibration, and operational validation.

The search comprised one reconnaissance query followed by a ten-query standard review: five sub-area searches, two review searches, two era-gated searches (through 2015 and from 2021 onward), and one follow-up centered on the most-cited paper. The available Consensus connector returned at most ten papers per query. Filters such as `human` and minimum sample size were inapplicable to this engineering topic; the connector did not expose SJR filtering. Only papers returned and fetched from Consensus during the session are cited here.

# Topic overview

The literature supports the feasibility of integrating broadband or ultra-wideband receiving antennas with conformal radomes for passive RF monitoring, but the evidence is divided into largely separate streams. The **antenna/radome literature** is comparatively mature, with measured prototypes evaluating impedance bandwidth, gain, insertion loss, angular stability, cavity resonances, and radar cross-section. The **passive detection literature** is also mature at the algorithmic level, particularly for spectrum sensing, direction of arrival (DOA), time difference of arrival (TDOA), frequency difference of arrival (FDOA), and specific-emitter identification. The sparse area is their end-to-end intersection: few returned studies jointly demonstrate a broadband conformal radome aperture, a calibrated multichannel receiver, detection of previously unknown emissions, emitter classification, and localization under realistic platform and propagation conditions. In particular, stealth-oriented frequency-selective-surface (FSS) radomes may deliberately reject out-of-band signals, creating a direct conflict with the objective of listening over the broadest possible spectrum [1](#ref-costa2012), [2](#ref-lv2021), [3](#ref-sheng2024), [4](#ref-xing2022).

The closest terminology for the combined topic is: **conformal ultra-wideband radio direction finder**, **passive emitter surveillance**, **ESM/ELINT receiving array**, **radome-integrated spectrum-monitoring aperture**, **specific emitter identification**, **open-set RF anomaly detection**, and **co-aperture passive direction-finding antenna**.

A crucial systems distinction is that **antenna coverage bandwidth** is not equivalent to **instantaneous receiver bandwidth**. A physically broadband antenna may span many octaves while the RF front end, ADC, channelizer, data transport, or processor observes only a much narrower portion at any instant [5](#ref-flak2022), [6](#ref-madanayake2024), [7](#ref-subbaraman2022).

# Start here: priority reading order

## 1. Closest review to the complete antenna problem

[**Wideband Antennas of Passive Seekers for Anti Radiation Missiles**](https://consensus.app/papers/details/04301748949257caa17485d3480352f2/?utm_source=chatgpt), Gupta et al. (2023), compares spiral, log-periodic, printed Vivaldi, and all-metal Vivaldi antennas and distinguishes concealed-behind-radome, flush-mounted, and conformal arrangements [8](#ref-gupta2023). It is the most direct returned overview of antenna placement for passive wideband reception. While reading, check whether its application-specific assumptions on size, frequency range, polarization, and angular coverage match the intended platform.

## 2. Seminal functional-radome paper

[**A Frequency Selective Radome With Wideband Absorbing Properties**](https://consensus.app/papers/details/1811b78b36fa5cc0840c16f9dd6f2a1b/?utm_source=chatgpt), Costa and Monorchio (2012), establishes an influential architecture combining an FSS passband with wideband out-of-band absorption [1](#ref-costa2012). The key design tension is that a radome advantageous for stealth may be inappropriate for broad-spectrum interception because out-of-band absorption removes potentially relevant emissions.

## 3. Foundational integrated conformal direction finder

[**Design and Full-Wave Analysis of Conformal Ultra-Wideband Radio Direction Finders**](https://consensus.app/papers/details/5f166a5e2c715f25a2cfa7d55f20749f/?utm_source=chatgpt), Caratelli, Liberal, and Yarovoy (2011), develops a conformal circular array covering 250 MHz–3.3 GHz and explicitly includes coupling compensation, array geometry, and ambiguity analysis [9](#ref-caratelli2011). Its main lesson is that calibration and manifold distortion are as important as nominal antenna bandwidth for reliable DOA estimation.

## 4. Broad orientation for emitter identity

[**A Comprehensive Survey on Radio Frequency Fingerprinting: Traditional Approaches, Deep Learning, and Open Challenges**](https://consensus.app/papers/details/85a1acc05180584992b4bd752a62599e/?utm_source=chatgpt), Jagannath, Jagannath, and Kumar (2022), connects SIGINT, RF fingerprinting, conventional features, deep learning, datasets, and security applications [10](#ref-jagannath2022). Pay particular attention to the difference between closed-set device classification and recognizing an emitter that was absent from training.

## 5. Current radome frontier

[**A Conformal Miniaturized Bandpass Frequency-Selective Surface With Stable Frequency Response for Radome Applications**](https://consensus.app/papers/details/6cb5b6043f755325b7abd988656c9afd/?utm_source=chatgpt), Sheng et al. (2024), reports measured stability for a curved X-band FSS, including large incidence angles and bending [3](#ref-sheng2024). Frequency stability alone, however, does not prove preservation of phase, group delay, or array-manifold accuracy required for direction finding.

## 6. Current open-set detection frontier

[**An Open-Set Supervised Anomaly Detection Method for Unauthorized Broadcasting Identification**](https://consensus.app/papers/details/66ce93d9ddd05433ac370321a0d58745/?utm_source=chatgpt), Zhang et al. (2025), directly addresses unauthorized broadcasting in an open-set setting using temporal representation learning and support-vector data description [11](#ref-zhang2025open). The central evaluation issue is whether performance remains stable across receivers, propagation channels, center-frequency changes, and truly unseen emitters.

## 7. Key controversy and vulnerability

[**Robustness of Deep Learning-Based Specific Emitter Identification under Adversarial Attacks**](https://consensus.app/papers/details/29ea0ff4b51857cca284e60d8c9c9d19/?utm_source=chatgpt), Sun et al. (2022), shows that small deliberately constructed perturbations can seriously degrade deep-learning-based specific-emitter identification, while adversarial training partially restores performance [12](#ref-sun2022). A classifier with high ordinary test accuracy is therefore not automatically suitable for detecting a deliberately camouflaged or deviated signal.

# Cross-search signals

## Repeat-hit papers

No paper met the strict criterion of appearing in three distinct sub-area searches. This is itself informative: the five branches remain weakly integrated.

The strongest repeat hits across the reconnaissance, sub-area, and review stages were:

- Gupta et al. (2023): three appearances overall [8](#ref-gupta2023).
- Gharat et al. (2026): three appearances overall [13](#ref-gharat2026).
- Costa and Monorchio (2012): functional-radome search and seminal-paper follow-up [1](#ref-costa2012).
- Soltanieh et al. (2020): anomaly/SEI search and review search [14](#ref-soltanieh2020).
- Xing et al. (2022): radome search and post-2021 era search [4](#ref-xing2022).
- Madanayake et al. (2024): integration search and post-2021 era search [6](#ref-madanayake2024).
- Tahseen et al. (2021): reconnaissance and radome-review search [15](#ref-tahseen2021).

These repetitions identify useful bridge papers, but they should not be interpreted as proof of foundational status by themselves.

## Citation velocity

Citation velocity was approximated as the Consensus citation count divided by `max(1, 2026 - publication year)`. It is descriptive only: recent survey articles are favored, and database citation counts can change.

| Paper                                              | Consensus citations | Approx. citations/year |
|----------------------------------------------------|--------------------:|-----------------------:|
| Jagannath et al. 2022 [10](#ref-jagannath2022) |                 263 |                   65.8 |
| Soltanieh et al. 2020 [14](#ref-soltanieh2020) |                 339 |                   56.5 |
| Costa and Monorchio 2012 [1](#ref-costa2012)   |                 678 |                   48.4 |
| Taherpour et al. 2010 [16](#ref-taherpour2010) |                 441 |                   27.6 |
| Sheng et al. 2024 [3](#ref-sheng2024)          |                  53 |                   26.5 |
| Lv et al. 2021 [2](#ref-lv2021)                |                  67 |                   13.4 |
| Xing et al. 2022 [4](#ref-xing2022)            |                  47 |                   11.8 |
| Omar and Shen 2018 [17](#ref-omar2018)         |                  77 |                    9.6 |

Normalized citation rate favors recent surveys, while total citations more clearly identify Costa–Monorchio and Taherpour et al. as long-standing reference points.

# How the field got here

The early literature treated passive RF direction finding largely as an array-design and estimation problem. By 2010–2012, researchers were integrating broadband conformal arrays with calibration methods and developing blind multiple-antenna spectrum detectors [9](#ref-caratelli2011), [16](#ref-taherpour2010), [18](#ref-liberal2011). During the same period, frequency-selective radomes evolved from protective dielectric covers into functional electromagnetic structures capable of transmitting selected bands while absorbing others [1](#ref-costa2012).

The next phase emphasized flush integration, cavity control, compact FSS structures, and low-RCS antenna–radome co-design [2](#ref-lv2021), [4](#ref-xing2022), [17](#ref-omar2018), [19](#ref-tianang2017). In parallel, **specific emitter identification** increasingly became known as **RF fingerprinting**, moving from handcrafted transient and spectrum features toward deep learning and open-set anomaly detection [10](#ref-jagannath2022), [11](#ref-zhang2025open), [14](#ref-soltanieh2020). Recent work adds real-time channelization, FPGA/SDR acceleration, and adaptive monitoring, but the hardware and signal-intelligence branches remain only partially integrated [5](#ref-flak2022), [6](#ref-madanayake2024), [13](#ref-gharat2026), [20](#ref-sorecau2026).

|      Year | Milestone                                                                                                                                                                            | Significance                                                                                   |
|----------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
|      2010 | Blind multiple-antenna spectrum sensing [16](#ref-taherpour2010)                                                                                                                 | Establishes detection under unknown channel, noise, and source parameters.                     |
|      2011 | Conformal UWB radio direction finders [9](#ref-caratelli2011), [18](#ref-liberal2011)                                                                                        | Integrates wideband elements, circular geometry, coupling analysis, and calibration.           |
|      2012 | Wideband absorptive frequency-selective radome [1](#ref-costa2012)                                                                                                               | Makes the radome an active part of spectral selectivity and signature control.                 |
|      2012 | Compact 70–3000 MHz DF antenna [21](#ref-bailey2012)                                                                                                                             | Demonstrates end-to-end receiver/antenna integration over a broad band.                        |
| 2017–2018 | Flush Vivaldi and thin conformal 3-D FSS systems [17](#ref-omar2018), [19](#ref-tianang2017)                                                                                 | Addresses cavity resonances, structural thickness, and curved integration.                     |
| 2020–2022 | RF fingerprinting surveys and deep-learning transition [10](#ref-jagannath2022), [14](#ref-soltanieh2020)                                                                    | Shifts identification from handcrafted features toward data-driven models.                     |
| 2021–2024 | Hybrid radomes and co-designed antenna–FSS structures [2](#ref-lv2021), [3](#ref-sheng2024), [4](#ref-xing2022)                                                          | Combines passband transmission, absorption, diffusion, conformality, and RCS control.          |
| 2024–2026 | Multichannel spectrum intelligence and open-set anomaly monitoring [6](#ref-madanayake2024), [11](#ref-zhang2025open), [13](#ref-gharat2026), [20](#ref-sorecau2026) | Moves toward real-time detection, directional channelization, and unknown-emitter recognition. |

## Terminology shifts

- **Radio direction finder / RDF** became **DOA estimation**, **passive emitter localization**, and **spectrum intelligence**.
- **Emitter recognition** became **specific emitter identification / SEI**, then **RF fingerprinting / RFF**.
- **Illegal radio monitoring** increasingly appears as **unauthorized broadcasting identification** and **open-set RF anomaly detection**.
- **Frequency-selective radome** expanded into **absorptive FSR**, **rasorber radome**, **absorptive-diffusive radome**, and **active/tunable FSS**.
- **Shared aperture** also appears as **co-aperture**, **common-radome**, and **multifunctional aperture**.

# Sub-area guide 1: broadband antenna architectures and radome-face placement

## What the research shows

Conformal elliptical dipoles, spirals, and Vivaldi/tapered-slot antennas are recurring candidates because they combine broad impedance bandwidth with geometries suitable for circular, cylindrical, or flush installation [8](#ref-gupta2023), [9](#ref-caratelli2011), [18](#ref-liberal2011), [19](#ref-tianang2017), [22](#ref-pi2025). Wideband DOA performance depends strongly on the calibrated array manifold: mutual coupling, structural scattering, element curvature, and radome effects can introduce angular bias even when return loss and gain appear acceptable [9](#ref-caratelli2011), [18](#ref-liberal2011).

Cavity-backed Vivaldi structures can deliver flush mounting, but cavity eigenmodes may produce severe in-band resonances unless explicitly suppressed [19](#ref-tianang2017). A recent co-aperture spiral concept proposes 2–40 GHz coverage under a common radome, but the returned work reports simulation rather than complete field validation [22](#ref-pi2025).

## Key papers

- [**Wideband Antennas of Passive Seekers for Anti Radiation Missiles**](https://consensus.app/papers/details/04301748949257caa17485d3480352f2/?utm_source=chatgpt), Gupta et al. (2023), Consensus citation count 1: best returned comparison of concealed, flush, and conformal passive-seeker arrangements [8](#ref-gupta2023).
- [**Design and Full-Wave Analysis of Conformal Ultra-Wideband Radio Direction Finders**](https://consensus.app/papers/details/5f166a5e2c715f25a2cfa7d55f20749f/?utm_source=chatgpt), Caratelli et al. (2011), 17 citations: integrates element, array, calibration, and DOA considerations [9](#ref-caratelli2011).
- [**Conformal Antenna Array for Ultra-Wideband Direction-of-Arrival Estimation**](https://consensus.app/papers/details/962901757e715c669ba9962b91c0b96b/?utm_source=chatgpt), Liberal et al. (2011), 9 citations: explicitly includes a protective radome and coupling compensation [18](#ref-liberal2011).
- [**Ultra-Wideband Lossless Cavity-Backed Vivaldi Antenna**](https://consensus.app/papers/details/747aac0a449e5797ad83ea444fb20680/?utm_source=chatgpt), Tianang et al. (2017), 42 citations: important treatment of cavity-induced resonances in flush arrays [19](#ref-tianang2017).
- [**A Compact Airborne Co-Aperture Cavity-Backed Spiral Antenna Design**](https://consensus.app/papers/details/7848c93584d354f19ce7554e9d95de54/?utm_source=chatgpt), Pi (2025), 0 citations: emerging common-radome concept spanning two bands over 2–40 GHz [22](#ref-pi2025).

## Search terms

conformal UWB antenna; passive seeker antenna; radio direction finder; cavity-backed Vivaldi; cavity-backed spiral; sinuous antenna; flush-mounted broadband array; co-aperture antenna; amplitude-tracking antenna set; phase-matched DF antenna.

## Boolean searches

``` text
("conformal antenna" OR "flush-mounted antenna" OR "embedded antenna")
AND ("ultra-wideband" OR wideband)
AND ("direction finding" OR "passive emitter" OR ESM OR ELINT)
```

``` text
(Vivaldi OR "tapered slot" OR spiral OR sinuous OR "log-periodic")
AND (radome OR "common aperture" OR "co-aperture")
AND (receive OR surveillance OR "direction finding")
```

# Sub-area guide 2: electromagnetic effects and functional radome technologies

## What the research shows

The radome must be treated as part of the receiving transfer function rather than merely as a mechanical cover. FSS and hybrid radomes can provide low-loss transmission windows together with out-of-band absorption or diffuse scattering [1](#ref-costa2012), [2](#ref-lv2021), [4](#ref-xing2022). Curved and conformal implementations increasingly demonstrate stable center frequency under oblique incidence, but most report insertion loss and radiation performance rather than phase-delay uniformity across an array aperture [3](#ref-sheng2024), [17](#ref-omar2018). A recent conformal-FSS mini-review also identifies materials, simulation, manufacturing, and practical implementation as continuing challenges [23](#ref-korkut2024).

For broad-spectrum monitoring, the design objective differs from that of a conventional stealth radome. A narrow FSS passband may protect an intended radar or communications band while making the system deaf to unauthorized emissions outside that window [1](#ref-costa2012), [15](#ref-tahseen2021). The radome therefore needs either a genuinely broad transparent region, multiple transparent windows, or a controllable transmission state.

## Key papers

- [**A Frequency Selective Radome With Wideband Absorbing Properties**](https://consensus.app/papers/details/1811b78b36fa5cc0840c16f9dd6f2a1b/?utm_source=chatgpt), Costa and Monorchio (2012), 678 citations: seminal passband-plus-absorber architecture [1](#ref-costa2012).
- [**Thin 3-D Bandpass Frequency-Selective Structure Based on Folded Substrate for Conformal Radome Applications**](https://consensus.app/papers/details/905ccf75368255a78a236f083a31e9ee/?utm_source=chatgpt), Omar and Shen (2018), 77 citations: fabricated semicylindrical FSS radome with broadband-horn integration [17](#ref-omar2018).
- [**Hybrid Absorptive-Diffusive Frequency Selective Radome**](https://consensus.app/papers/details/62fa6b42c0305286b6a3a4c60ea60a46/?utm_source=chatgpt), Lv et al. (2021), 67 citations: broad transmission window with absorption and diffusion sidebands [2](#ref-lv2021).
- [**A Low-RCS and Wideband Circularly Polarized Array Antenna Co-Designed With a High-Performance AMC-FSS Radome**](https://consensus.app/papers/details/7a9db905b6b953c3a6f429fe051d4096/?utm_source=chatgpt), Xing et al. (2022), 47 citations: measured co-design with less than 1 dB reported gain deterioration across its operating band [4](#ref-xing2022).
- [**A Conformal Miniaturized Bandpass Frequency-Selective Surface With Stable Frequency Response for Radome Applications**](https://consensus.app/papers/details/6cb5b6043f755325b7abd988656c9afd/?utm_source=chatgpt), Sheng et al. (2024), 53 citations: strong recent result on curved-FSS angular stability [3](#ref-sheng2024).

## Search terms

frequency-selective radome; FSS radome; rasorber; absorptive frequency-selective radome; transmitarray radome; radome insertion loss; radome boresight error; radome depolarization; radome group delay; active tunable radome.

## Boolean searches

``` text
(radome OR "antenna cover")
AND ("frequency selective surface" OR FSS OR rasorber OR metasurface)
AND (wideband OR broadband OR multiband)
AND ("insertion loss" OR "angular stability" OR "boresight error")
```

``` text
("conformal radome" OR "curved FSS")
AND (transmission OR passband)
AND (phase OR "group delay" OR depolarization OR aberration)
AND (array OR "direction finding")
```

# Sub-area guide 3: passive emitter detection, direction finding, and localization

## What the research shows

Blind multiple-antenna spectrum sensing can outperform conventional energy detection when channel gain, source statistics, and noise variance are uncertain [16](#ref-taherpour2010). Once a signal is detected, localization commonly uses AoA/DOA, TDOA, FDOA, or combinations of them. TDOA/FDOA methods can achieve strong accuracy, but receiver geometry, synchronization, platform motion, and computational load are central constraints [24](#ref-liu2019), [25](#ref-pine2021).

For radome-mounted arrays, calibration is not an optional post-processing refinement. Directional errors can create biased bearings or ghost emitter positions; joint localization and self-calibration methods attempt to correct those effects [26](#ref-zhang2023calibration). The older conformal-RDF literature already recognized mutual coupling and support-structure distortion as array-manifold problems [9](#ref-caratelli2011), [18](#ref-liberal2011).

## Key papers

- [**Multiple Antenna Spectrum Sensing in Cognitive Radios**](https://consensus.app/papers/details/dd361298468d58a9a3f6b6af0c34e977/?utm_source=chatgpt), Taherpour et al. (2010), 441 citations: foundational blind multiple-antenna detector under parameter uncertainty [16](#ref-taherpour2010).
- [**Design and Full-Wave Analysis of Conformal Ultra-Wideband Radio Direction Finders**](https://consensus.app/papers/details/5f166a5e2c715f25a2cfa7d55f20749f/?utm_source=chatgpt), Caratelli et al. (2011), 17 citations: connects antenna nonidealities directly to DOA performance [9](#ref-caratelli2011).
- [**Computationally Efficient TDOA and FDOA Estimation Algorithm in Passive Emitter Localisation**](https://consensus.app/papers/details/47ae35140d8e563486d4808c6acd8485/?utm_source=chatgpt), Liu et al. (2019), 14 citations: targets real-time feasibility and multi-emitter cross-term suppression [24](#ref-liu2019).
- [**The Geometry of Far-Field Passive Source Localization With TDOA and FDOA**](https://consensus.app/papers/details/035e2d1ded6e5316b49b04c2007445cb/?utm_source=chatgpt), Pine et al. (2021), 36 citations: clarifies when TDOA/FDOA measurements geometrically constrain far-field sources [25](#ref-pine2021).
- [**Passive Joint Emitter Localization with Sensor Self-Calibration**](https://consensus.app/papers/details/a785d6a4988c51bcb3d4c3b896010b09/?utm_source=chatgpt), Zhang et al. (2023), 8 citations: addresses calibration bias in distributed passive arrays [26](#ref-zhang2023calibration).

## Search terms

passive emitter localization; radio direction finding; angle of arrival; direction of arrival; amplitude-comparison DF; phase interferometer; TDOA/FDOA; direct position determination; array-manifold calibration; noncooperative emitter.

## Boolean searches

``` text
("passive emitter" OR "noncooperative emitter" OR "radio source")
AND (localization OR geolocation OR "direction finding")
AND (DOA OR AOA OR TDOA OR FDOA OR interferometry)
```

``` text
("wideband direction finding" OR "broadband direction finding")
AND (calibration OR "array manifold" OR coupling OR radome)
AND (multichannel OR array)
```

# Sub-area guide 4: clandestine, anomalous, and deviated-signal identification

## What the research shows

RF fingerprinting uses hardware-dependent imperfections to associate a received waveform with a device or emitter. Surveys show a progression from manually designed transient and modulation features to deep neural representations [10](#ref-jagannath2022), [14](#ref-soltanieh2020). Much of the literature, however, assumes a **closed set**, in which every emitter observed at test time belongs to a known training class.

Clandestine-signal detection usually requires an open-set or anomaly formulation. Illegal-FM monitoring has been demonstrated using specific-emitter features and outlier detection [27](#ref-guo2021), while recent work explicitly models unauthorized transmissions not fully represented in training [11](#ref-zhang2025open). Frequency-hopping emitters can also be fingerprinted [28](#ref-kang2021), but adversarial perturbations may make deep SEI systems unreliable against an adaptive opponent [12](#ref-sun2022).

## Key papers

- [**A Review of Radio Frequency Fingerprinting Techniques**](https://consensus.app/papers/details/1c3cd42586205e0280356e90cb7ab147/?utm_source=chatgpt), Soltanieh et al. (2020), 339 citations: core taxonomy of transient and modulated-signal fingerprints [14](#ref-soltanieh2020).
- [**A Comprehensive Survey on Radio Frequency Fingerprinting: Traditional Approaches, Deep Learning, and Open Challenges**](https://consensus.app/papers/details/85a1acc05180584992b4bd752a62599e/?utm_source=chatgpt), Jagannath et al. (2022), 263 citations: broad connection among SIGINT, datasets, ML, and RFF [10](#ref-jagannath2022).
- [**An SEI-Based Identification Scheme for Illegal FM Broadcast**](https://consensus.app/papers/details/b81586a8d9ee5753a4b48df60568f585/?utm_source=chatgpt), Guo et al. (2021), 7 citations: direct application to legal-versus-illegal FM emitters [27](#ref-guo2021).
- [**Robustness of Deep Learning-Based Specific Emitter Identification under Adversarial Attacks**](https://consensus.app/papers/details/29ea0ff4b51857cca284e60d8c9c9d19/?utm_source=chatgpt), Sun et al. (2022), 22 citations: demonstrates an important security weakness in neural SEI [12](#ref-sun2022).
- [**An Open-Set Supervised Anomaly Detection Method for Unauthorized Broadcasting Identification**](https://consensus.app/papers/details/66ce93d9ddd05433ac370321a0d58745/?utm_source=chatgpt), Zhang et al. (2025), 0 citations: closest direct match to unknown unauthorized-signal detection [11](#ref-zhang2025open).

## Search terms

specific emitter identification; SEI; radio-frequency fingerprinting; RF fingerprint; unauthorized broadcasting; illegal-emitter identification; open-set RF classification; unknown emitter; spectrum anomaly detection; low-probability-of-intercept signal; frequency-hopping emitter identification.

## Boolean searches

``` text
("specific emitter identification" OR "RF fingerprinting" OR "radio frequency fingerprint")
AND ("open set" OR unknown OR unauthorized OR illegal OR anomaly)
```

``` text
("clandestine signal" OR "unauthorized transmission" OR "illegal broadcast"
 OR "deceptive emitter" OR spoofing)
AND (detection OR identification OR classification)
AND (spectrum OR RF OR radio)
```

``` text
("frequency hopping" OR "low probability of intercept" OR burst)
AND ("emitter identification" OR "anomaly detection" OR fingerprinting)
```

# Sub-area guide 5: integration, calibration, and operational validation

## What the research shows

Antenna bandwidth does not determine how much spectrum can be observed simultaneously. SDR systems remain limited by ADC rate, RF-front-end linearity, host-transfer bandwidth, channelization complexity, storage, and processing [5](#ref-flak2022), [7](#ref-subbaraman2022). Fast sweeping increases frequency coverage but introduces blind time, creating a risk of missing short bursts or hopping signals.

Recent systems address this through FPGA acceleration, multichannel SDRs, directional sub-band processing, and adaptive high-resolution analysis [6](#ref-madanayake2024), [13](#ref-gharat2026), [20](#ref-sorecau2026). Receiver saturation and intermodulation are especially important for clandestine-signal detection because a weak unauthorized emitter may coexist with much stronger legitimate transmitters. The fetched Consensus record for the recent multipath RFSoC front end did not expose its abstract, so only its bibliographic metadata is used here [29](#ref-kovacs2025).

## Key papers

- [**Hardware-Accelerated Real-Time Spectrum Analyzer With a Broadband Fast Sweep Feature Based on the Cost-Effective SDR Platform**](https://consensus.app/papers/details/fe357d36f1dc5626b1f9d7fae0ff75a7/?utm_source=chatgpt), Flak (2022), 16 citations: quantifies real-time bandwidth and sweep-speed trade-offs [5](#ref-flak2022).
- [**Observing Wideband RF Spectrum with Low-Cost, Resource-Limited SDRs**](https://consensus.app/papers/details/f527168041d95e7ba00d1be0e2d79a21/?utm_source=chatgpt), Subbaraman et al. (2022), 0 citations: identifies backhaul and processing as barriers to real-time wideband observation [7](#ref-subbaraman2022).
- [**Design of Multichannel Spectrum Intelligence Systems Using Approximate DFT for Antenna-Array Spectrum Perception**](https://consensus.app/papers/details/1f33f743e5f75b38b47a1905f27c7a5f/?utm_source=chatgpt), Madanayake et al. (2024), 13 citations: integrates directional sensing, channelization, and adaptive spectral attention [6](#ref-madanayake2024).
- [**Wideband Monitoring System of Drone Emissions Based on SDR Technology with RFNoC Architecture**](https://consensus.app/papers/details/9d218ae20f9b5c1dae9b17a3583aece9/?utm_source=chatgpt), Sorecau et al. (2026), 3 citations: multichannel architecture intended to capture frequency-hopping drone emissions [20](#ref-sorecau2026).
- [**Real-Time Passive RF Spectrum Monitoring and Localization Using Adaptive Signal Analysis**](https://consensus.app/papers/details/6719301371565fb4bacbf2c123a0d12d/?utm_source=chatgpt), Gharat et al. (2026), 0 citations: combines adaptive anomaly thresholds and directional localization in a low-cost framework [13](#ref-gharat2026).

## Search terms

instantaneous RF bandwidth; wideband spectrum monitoring; SDR channelizer; RFSoC spectrum analyzer; multichannel digital receiver; receiver blind time; dynamic range; spurious-free dynamic range; array calibration; real-time spectrum intelligence.

## Boolean searches

``` text
("wideband spectrum monitoring" OR "spectrum intelligence")
AND (SDR OR RFSoC OR FPGA OR channelizer)
AND ("real time" OR multichannel)
```

``` text
("passive RF monitoring" OR "emitter surveillance")
AND ("dynamic range" OR linearity OR saturation OR "blind time")
AND (array OR antenna OR receiver)
```

# Key research groups

The returned Consensus metadata did not expose affiliations. Therefore, affiliations are deliberately not inferred or invented; they should be checked on the linked paper pages or publisher records.

## I. Liberal, D. Caratelli, and A. Yarovoy

Their recurring work covers conformal UWB arrays, radio direction finding, coupling compensation, and array-manifold calibration. Three closely related pre-2015 records appeared in the era-gated search. A representative paper is Caratelli et al. (2011) [9](#ref-caratelli2011).

## F. Costa, A. Monorchio, and G. Manara

This group recurs around frequency-selective surfaces, electromagnetic absorbers, equivalent-circuit modeling, and functional radomes. The representative paper in the returned set is Costa and Monorchio (2012) [1](#ref-costa2012).

## Zhongxiang Shen and collaborators

The returned papers cover conformal 3-D FSS structures, absorptive-diffusive radomes, wide-angle transmission, and RCS reduction. Recurring collaborators include A. Omar, Qihao Lv, and C. Jin. A representative paper is Lv et al. (2021) [2](#ref-lv2021).

## X. Sheng, Ning Liu, and collaborators

Their work centers on equivalent-circuit-based bandpass FSS design, conformal stability, wide rejection bands, and radome applications. A representative paper is Sheng et al. (2024) [3](#ref-sheng2024).

## M. Sorecau, E. Sorecau, P. Bechet, and collaborators

The returned work focuses on SDR spectrum monitoring, swept versus real-time observation, multichannel RFNoC architectures, and drone-emission detection. A representative paper is Sorecau et al. (2026) [20](#ref-sorecau2026).

# Open questions and gaps

## Methodological gaps

### Lack of end-to-end evaluation

Most antenna and radome papers terminate at S-parameters, gain, radiation patterns, RCS, or transmission coefficients. Detection papers generally begin with already digitized signals. Few returned studies measured the full chain

> radome -\> antenna array -\> RF front end -\> ADC/channelizer -\> detector -\> classifier -\> direction/localization output

under the same experimental conditions.

**Why it matters:** a radome may have acceptable average insertion loss while introducing frequency- and angle-dependent phase errors that degrade DOA or RF fingerprints.

### Closed-set and dataset-leakage risks

RF-fingerprinting studies often evaluate known devices under conditions similar to training [10](#ref-jagannath2022), [14](#ref-soltanieh2020). Open-set work is emerging [11](#ref-zhang2025open), but channel, receiver, and location effects can accidentally become part of the learned fingerprint.

**Why it matters:** a system may classify the laboratory channel or receiver chain rather than the clandestine transmitter.

### Insufficient adversarial testing

Sun et al. show that deliberately perturbed emissions can defeat deep SEI [12](#ref-sun2022). This issue is not routinely incorporated into antenna/radome or spectrum-monitoring validation.

**Why it matters:** a clandestine source may intentionally imitate an authorized waveform or suppress its hardware fingerprint.

### Inconsistent metrics

The branches use different outcome measures: VSWR, gain, insertion loss, and RCS for hardware; probability of detection and false alarm for sensing; angular RMSE for localization; and accuracy or AUC for classification.

**Why it matters:** there is no accepted system-level metric connecting radome loss and distortion to the probability of detecting and identifying a weak emitter.

## Population and context gaps

### No demonstrated seamless multi-octave system

The returned works cover useful but different ranges: 250 MHz–3.3 GHz [9](#ref-caratelli2011), [18](#ref-liberal2011), 1.5–7.5 GHz [19](#ref-tianang2017), X-band radomes [3](#ref-sheng2024), [15](#ref-tahseen2021), and a proposed 2–40 GHz co-aperture receiver [22](#ref-pi2025).

**Why it matters:** a single broad-spectrum radome face may require several sub-arrays and receiver paths rather than one universal element.

### Weak, short-duration, and frequency-hopping emitters

Real-time monitoring papers recognize hopping or transient signals [5](#ref-flak2022), [20](#ref-sorecau2026), but complete evaluation with weak emitters, strong adjacent transmitters, multipath, and platform motion is sparse.

**Why it matters:** sweep-based receivers can miss short transmissions, while wide instantaneous receivers may saturate or exceed processing capacity.

### Environmental and structural aging

The returned conformal-radome studies focus mostly on electromagnetic prototypes. Thermal gradients, moisture, vibration, erosion, manufacturing tolerances, and long-term dielectric changes are not integrated with classification and DOA calibration.

**Why it matters:** slow structural drift can look like a signal deviation or corrupt a stored emitter baseline.

### Airborne and curved-platform field datasets

Several papers target airborne or UAV platforms [8](#ref-gupta2023), [20](#ref-sorecau2026), [22](#ref-pi2025), but public, reproducible datasets combining curved arrays, radome distortion, and emitter identity appear sparse in the returned literature.

**Why it matters:** laboratory models may not transfer to a moving platform with changing orientation, polarization, and multipath.

## Conceptual and theoretical gaps

### Stealth radome versus listening radome

FSS radomes commonly suppress out-of-band exposure [1](#ref-costa2012), [2](#ref-lv2021), [4](#ref-xing2022). A surveillance system, by contrast, seeks sensitivity to signals outside the expected band.

**Why it matters:** optimizing for low RCS and optimizing for broad-spectrum listening can be contradictory objectives. A tunable, segmented, or deliberately wide-transmission radome may be required.

### Emitter identity versus signal deviation

RF fingerprinting asks, “Which physical transmitter produced this waveform?” Anomaly detection asks, “Does this observation differ from expected behavior?” These are related but not equivalent.

**Why it matters:** a known transmitter can change modulation or operating parameters without changing hardware, while a deceptive transmitter can imitate the nominal waveform but retain a different hardware fingerprint.

### Antenna bandwidth versus receiver observability

A 2–40 GHz antenna does not imply simultaneous 38 GHz observation. Receiver bandwidth, channelization, and data transport determine what is actually visible [5](#ref-flak2022), [6](#ref-madanayake2024), [7](#ref-subbaraman2022).

**Why it matters:** system specifications should separately state antenna coverage, instantaneous bandwidth, sweep revisit time, and probability of intercept.

### Propagation fingerprint versus emitter fingerprint

Radome response, antenna pattern, multipath, receiver nonlinearity, and transmitter hardware all affect the measured waveform.

**Why it matters:** without domain-invariant models or controlled calibration, a classifier can confuse location and channel changes with a new or deviating emitter.

# Recommended research architecture

The literature supports a modular research program rather than attempting a universal antenna immediately:

1.  Segment the desired spectrum into technically realistic sub-bands.
2.  Use conformal or flush broadband elements appropriate to each band, such as spiral or sinuous structures at lower bands and Vivaldi or tapered-slot elements at higher bands.
3.  Treat the radome as a calibrated complex transfer function $H(f,\theta,\phi,p)$, including amplitude, phase, polarization, and incidence angle.
4.  Use synchronized multichannel reception for DOA and a separate wideband or swept path for discovery.
5.  Separate the inference chain into signal-presence detection, waveform characterization, known-emitter matching, open-set anomaly detection, and localization.
6.  Evaluate the complete system using both ordinary and deliberately deceptive emitters while varying SNR, channel, orientation, temperature, and radome condition.

The most defensible thesis-level gap emerging from the returned literature is:

> **Joint co-design and experimental validation of a conformal broadband antenna–radome–receiver system for open-set passive emitter detection, specific-emitter identification, and direction finding, with explicit calibration of radome- and platform-induced distortions.**

# Limitations of this review

The review is bounded by the papers returned by Consensus in this session, the ten-results-per-query limit, and the metadata exposed by the connector. Citation counts are provisional and will change. Some technically relevant defense and industrial work may be classified, proprietary, poorly indexed, or published outside peer-reviewed venues. The exact-title follow-up for the most-cited radome paper returned only four results; no outside material was silently added.

# References

<a id="ref-costa2012"></a>

1. F. Costa and A. Monorchio, “A frequency selective radome with wideband absorbing properties,” *IEEE Transactions on Antennas and Propagation*, vol. 60, pp. 2740–2747, 2012, Available: <https://consensus.app/papers/details/1811b78b36fa5cc0840c16f9dd6f2a1b/?utm_source=chatgpt>

<a id="ref-lv2021"></a>

2. Q. Lv, C. Jin, B. Zhang, and Z. Shen, “Hybrid absorptive-diffusive frequency selective radome,” *IEEE Transactions on Antennas and Propagation*, vol. 69, pp. 3312–3321, 2021, Available: <https://consensus.app/papers/details/62fa6b42c0305286b6a3a4c60ea60a46/?utm_source=chatgpt>

<a id="ref-sheng2024"></a>

3. X. Sheng, H. Wang, N. Liu, and K. Wang, “A conformal miniaturized bandpass frequency-selective surface with stable frequency response for radome applications,” *IEEE Transactions on Antennas and Propagation*, vol. 72, pp. 2423–2433, 2024, Available: <https://consensus.app/papers/details/6cb5b6043f755325b7abd988656c9afd/?utm_source=chatgpt>

<a id="ref-xing2022"></a>

4. Z. Xing, F. Yang, P. Yang, and J. Yang, “A low-RCS and wideband circularly polarized array antenna co-designed with a high-performance AMC-FSS radome,” *IEEE Antennas and Wireless Propagation Letters*, vol. 21, pp. 1659–1663, 2022, Available: <https://consensus.app/papers/details/7a9db905b6b953c3a6f429fe051d4096/?utm_source=chatgpt>

<a id="ref-flak2022"></a>

5. P. Flak, “Hardware-accelerated real-time spectrum analyzer with a broadband fast sweep feature based on the cost-effective SDR platform,” *IEEE Access*, vol. 10, pp. 110934–110946, 2022, Available: <https://consensus.app/papers/details/fe357d36f1dc5626b1f9d7fae0ff75a7/?utm_source=chatgpt>

<a id="ref-madanayake2024"></a>

6. A. Madanayake *et al.*, “Design of multichannel spectrum intelligence systems using approximate discrete fourier transform algorithm for antenna array-based spectrum perception applications,” *Algorithms*, vol. 17, p. 338, 2024, Available: <https://consensus.app/papers/details/1f33f743e5f75b38b47a1905f27c7a5f/?utm_source=chatgpt>

<a id="ref-subbaraman2022"></a>

7. R. Subbaraman, N. Bhaskar, S. Crow, M. Khazraee, A. Schulman, and D. Bharadia, “Observing wideband RF spectrum with low-cost, resource-limited SDRs,” in *Proceedings of the 20th annual international conference on mobile systems, applications and services*, 2022. Available: <https://consensus.app/papers/details/f527168041d95e7ba00d1be0e2d79a21/?utm_source=chatgpt>

<a id="ref-gupta2023"></a>

8. A. Gupta, T. Jain, A. Kothari, and M. Chakravarthy, “Wideband antennas of passive seekers for anti radiation missiles,” *Defence Science Journal*, 2023, Available: <https://consensus.app/papers/details/04301748949257caa17485d3480352f2/?utm_source=chatgpt>

<a id="ref-caratelli2011"></a>

9. D. Caratelli, I. Liberal, and A. Yarovoy, “Design and full-wave analysis of conformal ultra-wideband radio direction finders,” *IET Microwaves, Antennas & Propagation*, vol. 5, pp. 1164–1174, 2011, Available: <https://consensus.app/papers/details/5f166a5e2c715f25a2cfa7d55f20749f/?utm_source=chatgpt>

<a id="ref-jagannath2022"></a>

10. A. Jagannath, J. Jagannath, and P. Kumar, “A comprehensive survey on radio frequency (RF) fingerprinting: Traditional approaches, deep learning, and open challenges,” *Computer Networks*, vol. 219, p. 109455, 2022, Available: <https://consensus.app/papers/details/85a1acc05180584992b4bd752a62599e/?utm_source=chatgpt>

<a id="ref-zhang2025open"></a>

11. B. Zhang, F. Zhou, R. Ding, M. Xu, Y. Yang, and Q. Wu, “An open-set supervised anomaly detection method for unauthorized broadcasting identification,” *IEEE Internet of Things Journal*, vol. 12, pp. 54150–54162, 2025, Available: <https://consensus.app/papers/details/66ce93d9ddd05433ac370321a0d58745/?utm_source=chatgpt>

<a id="ref-sun2022"></a>

12. L. Sun, D. Ke, X. Wang, Z. Huang, and K. Huang, “Robustness of deep learning-based specific emitter identification under adversarial attacks,” *Remote Sensing*, vol. 14, p. 4996, 2022, Available: <https://consensus.app/papers/details/29ea0ff4b51857cca284e60d8c9c9d19/?utm_source=chatgpt>

<a id="ref-gharat2026"></a>

13. N. N. Gharat, A. Shigam, K. Bari, and P. Parkar, “Real-time passive RF spectrum monitoring and localization using adaptive signal analysis,” in *2026 international conference on communication, computing and emerging technologies (IC3ET)*, 2026, pp. 199–202. Available: <https://consensus.app/papers/details/6719301371565fb4bacbf2c123a0d12d/?utm_source=chatgpt>

<a id="ref-soltanieh2020"></a>

14. N. Soltanieh, Y. Norouzi, Y. Yang, and N. Karmakar, “A review of radio frequency fingerprinting techniques,” *IEEE Journal of Radio Frequency Identification*, vol. 4, pp. 222–233, 2020, Available: <https://consensus.app/papers/details/1c3cd42586205e0280356e90cb7ab147/?utm_source=chatgpt>

<a id="ref-tahseen2021"></a>

15. H. Tahseen, L. Yang, and X. Zhou, “Design of FSS-antenna-radome system for airborne and ground applications,” *IET Communications*, vol. 15, pp. 1691–1699, 2021, Available: <https://consensus.app/papers/details/599f10722b705b9e8666fd6b2b14172a/?utm_source=chatgpt>

<a id="ref-taherpour2010"></a>

16. A. Taherpour, M. Nasiri-Kenari, and S. Gazor, “Multiple antenna spectrum sensing in cognitive radios,” *IEEE Transactions on Wireless Communications*, vol. 9, 2010, Available: <https://consensus.app/papers/details/dd361298468d58a9a3f6b6af0c34e977/?utm_source=chatgpt>

<a id="ref-omar2018"></a>

17. A. Omar and Z. Shen, “Thin 3-d bandpass frequency-selective structure based on folded substrate for conformal radome applications,” *IEEE Transactions on Antennas and Propagation*, vol. 67, pp. 282–290, 2018, Available: <https://consensus.app/papers/details/905ccf75368255a78a236f083a31e9ee/?utm_source=chatgpt>

<a id="ref-liberal2011"></a>

18. I. Liberal, D. Caratelli, and A. Yarovoy, “Conformal antenna array for ultra-wideband direction-of-arrival estimation,” *International Journal of Microwave and Wireless Technologies*, vol. 3, pp. 439–450, 2011, Available: <https://consensus.app/papers/details/962901757e715c669ba9962b91c0b96b/?utm_source=chatgpt>

<a id="ref-tianang2017"></a>

19. E. G. Tianang, M. Elmansouri, and D. Filipović, “Ultra-wideband lossless cavity-backed vivaldi antenna,” *IEEE Transactions on Antennas and Propagation*, vol. 66, pp. 115–124, 2017, Available: <https://consensus.app/papers/details/747aac0a449e5797ad83ea444fb20680/?utm_source=chatgpt>

<a id="ref-sorecau2026"></a>

20. M. Şorecău, E. Şorecău, and P. Bechet, “Wideband monitoring system of drone emissions based on SDR technology with RFNoC architecture,” *Drones*, 2026, Available: <https://consensus.app/papers/details/9d218ae20f9b5c1dae9b17a3583aece9/?utm_source=chatgpt>

<a id="ref-bailey2012"></a>

21. M. Bailey, T. Campbell, C. Reddy, R. Kellogg, and P. Nguyen, “Compact wideband direction-finding antenna,” *IEEE Antennas and Propagation Magazine*, vol. 54, pp. 44–68, 2012, Available: <https://consensus.app/papers/details/13b11a31b3ae54dc9a7728d5d7c0376e/?utm_source=chatgpt>

<a id="ref-pi2025"></a>

22. C. Pi, “A compact airborne co-aperture cavity-backed spiral antenna design,” vol. 13513. pp. 135130O-135130O-7, 2025. Available: <https://consensus.app/papers/details/7848c93584d354f19ce7554e9d95de54/?utm_source=chatgpt>

<a id="ref-korkut2024"></a>

23. N. A. Korkut, A. Kara, and F. E. Yardım, “Conformal frequency selective surfaces in radome design: A mini review,” *Savunma Bilimleri Dergisi*, 2024, Available: <https://consensus.app/papers/details/19096196ecb75562b0dae493c424791a/?utm_source=chatgpt>

<a id="ref-liu2019"></a>

24. Z. Liu, R. Wang, and Y. Zhao, “Computationally efficient TDOA and FDOA estimation algorithm in passive emitter localisation,” *IET Radar, Sonar & Navigation*, 2019, Available: <https://consensus.app/papers/details/47ae35140d8e563486d4808c6acd8485/?utm_source=chatgpt>

<a id="ref-pine2021"></a>

25. K. Pine, S. Pine, and M. Cheney, “The geometry of far-field passive source localization with TDOA and FDOA,” *IEEE Transactions on Aerospace and Electronic Systems*, vol. 57, pp. 3782–3790, 2021, Available: <https://consensus.app/papers/details/035e2d1ded6e5316b49b04c2007445cb/?utm_source=chatgpt>

<a id="ref-zhang2023calibration"></a>

26. G. Zhang, H. Liu, W. Dai, T. Huang, Y. Liu, and X. Wang, “Passive joint emitter localization with sensor self-calibration,” *Remote Sensing*, vol. 15, p. 671, 2023, Available: <https://consensus.app/papers/details/a785d6a4988c51bcb3d4c3b896010b09/?utm_source=chatgpt>

<a id="ref-guo2021"></a>

27. S. Guo, Y. Xu, W. Huang, and B. Liu, “An SEI-based identification scheme for illegal FM broadcast,” in *2021 IEEE HPCC/DSS/SmartCity/DependSys*, 2021, pp. 517–524. Available: <https://consensus.app/papers/details/b81586a8d9ee5753a4b48df60568f585/?utm_source=chatgpt>

<a id="ref-kang2021"></a>

28. J. Kang, Y. Shin, H. Lee, J. Park, and H. Lee, “Radio frequency fingerprinting for frequency hopping emitter identification,” *Applied Sciences*, 2021, Available: <https://consensus.app/papers/details/c4da4d86f8005c62aedc9d1f4e7b4720/?utm_source=chatgpt>

<a id="ref-kovacs2025"></a>

29. G. Kovacs *et al.*, “Design, implementation, and RFSoC-based validation of a multi-path RF front-end for wideband spectrum analysis,” *Results in Engineering*, 2025, Available: <https://consensus.app/papers/details/c280f2e930bb5680b7ad564afb5ec0eb/?utm_source=chatgpt>
