## ID-Reveal: Identity-aware Deepfake Video Detection
Davide Cozzolino, Andreas R&ouml;ssler, Justus Thies, Matthias Nie&szlig;ner, Luisa Verdoliva

[![ID-Reveal](https://img.shields.io/badge/WebPage-222222.svg?style=for-the-badge&logo=github)](https://grip-unina.github.io/id-reveal/)
[![Code](https://img.shields.io/badge/Code-ef8808.svg?style=for-the-badge)](https://github.com/grip-unina/poi-forensics/tree/main/app_code)
[![arXiv](https://img.shields.io/badge/-arXiv-B31B1B.svg?style=for-the-badge)](https://arxiv.org/abs/2012.02512)
[![Video](https://img.shields.io/badge/-Video-1BB31B.svg?style=for-the-badge)](https://www.youtube.com/watch?v=RsFxsOLvRdY)
[![GRIP](https://img.shields.io/badge/-GRIP-0888ef.svg?style=for-the-badge)](https://www.grip.unina.it)

<p align="center"> <img height="200" src="schema.jpg"> </p>
ID-Reveal is an identity-aware DeepFake video detection. Based on reference videos of a person, we estimate a temporal embedding which is used as a distance metric to detect fake videos. <br/>

<p align="center"> <img height="200" src="training_schema.jpg"> </p>
ID-Reveal relies on two neural networks, the Temporal ID Network as well as the 3DMM Generative Network, which interact with each other in an adversarial fashion. Using a three-dimensional morphable model (3DMM), we process videos of different identities on a frame-by-frame basis and train the Temporal ID Network to embed the extracted features such that they can be separated in the resulting embedding space based on their containing identity. In order to incentivize this network to focus on temporal aspects rather than visual cues, we jointly train the 3DMM Generative Network to transform extracted features to fool its discriminative counterpart.<br/>

### Bibtex

```javascript
@inproceedings{cozzolino2021reveal,
  title={Id-Reveal: Identity-aware deepfake video detection},
  author={Cozzolino, Davide and R{\"o}ssler, Andreas and Thies, Justus and Nie{\ss}ner, Matthias and Verdoliva, Luisa},
  booktitle={Proceedings of the IEEE/CVF International Conference on Computer Vision},
  pages={15108--15117},
  year={2021}
}
```

### Acknowledgments

We gratefully acknowledge the support of this research by a TUM-IAS Hans Fischer Senior Fellowship, a TUM-IAS Rudolf Moßbauer Fellowship and a Google Faculty Research Award.
In addition, this material is based on research sponsored by the Defense Advanced Research Projects Agency (DARPA) and the Air Force Research Laboratory (AFRL) under agreement number FA8750-20-2-1004. 
he U.S. Government is authorized to reproduce and distribute reprints for Governmental purposes notwithstanding any copyright notation thereon.
The views and conclusions contained herein are those of the authors and should not be interpreted as necessarily representing the official policies or endorsements, either expressed or implied, of DARPA and AFRL or the U.S. Government.

This work is also supported by the PREMIER project, funded by the Italian Ministry of Education, University, and Research within the PRIN 2017 program.
