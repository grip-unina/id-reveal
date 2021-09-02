---
layout: paper
paper: ID-Reveal&colon; Identity-aware DeepFake Video Detection
github_url: https://github.com/grip-unina/id-reveal
authors:  
  - name: Davide Cozzolino
    link: http://www.grip.unina.it/people/userprofile/davide_cozzolino.html
    index: 1
  - name: Andreas Rössler
    link: http://niessnerlab.org/members/andreas_roessler/profile.html
    index: 2
  - name: Justus Thies
    link: https://justusthies.github.io/
    index: 2 3
  - name: Matthias Nießner
    link: https://www.niessnerlab.org/members/matthias_niessner/profile.html
    index: 2
  - name: Luisa Verdoliva
    link: http://www.grip.unina.it/people/userprofile/vrdoliva.html
    index: 1
affiliations: 
  - name: University Federico II of Naples, Italy
    index: 1
  - name: Technical University of Munich
    index: 2
  - name: Max Planck Institute for Intelligent Systems, Tubingen
    index: 3
links:
    arxiv: https://arxiv.org/abs/2012.02512
    code: https://github.com/grip-unina/id-reveal
    video: https://www.youtube.com/watch?v=RsFxsOLvRdY
---

<center><img src="./header.jpg" alt="header" height="200" /></center>

A major challenge in DeepFake forgery detection is that state-of-the-art algorithms are mostly trained to detect a specific fake method. As a result, these approaches show poor generalization across different types of facial manipulations, e.g., from face swapping to facial reenactment. To this end, we introduce ID-Reveal, a new approach that learns temporal facial features, specific of how a person moves while talking, by means of metric learning coupled with an adversarial training strategy. The advantage is that we do not need any training data of fakes, but only train on real videos. Moreover, we utilize high-level semantic features, which enables robustness to widespread and disruptive forms of post-processing. We perform a thorough experimental analysis on several publicly available benchmarks. Compared to state of the art, our method improves generalization and is more robust to low-quality videos, that are usually spread over social networks. In particular, we obtain an average improvement of more than 15% in terms of accuracy for facial reenactment on high compressed videos.

### News

*   2021-08-17: Paper is accepted to The International Conference on Computer Vision (ICCV) 2021.

### Bibtex

```javascript
@article{Cozzolino2020_idreveal,
  title={ID-Reveal: Identity-aware DeepFake Video Detection},
  author={Cozzolino, Davide and R{\"o}ssler, Andreas and Thies, Justus and Nie{\ss}ner, Matthias and Verdoliva, Luisa},
  journal={arXiv preprint arXiv:2012.02512},
  year={2020}
}
```
